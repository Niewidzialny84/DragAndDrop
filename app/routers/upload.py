from fastapi import Request, APIRouter, File, UploadFile, Depends, status,  HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from ..library.helpers import *
from ..library.settings import LOGIN, PASSWORD

import secrets

router = APIRouter(prefix='/api/v1')

security = HTTPBasic()

templates = Jinja2Templates(directory="templates/")

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = LOGIN
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = PASSWORD
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@router.get("/upload", response_class=HTMLResponse, dependencies=[Depends(get_current_username)])
def get_upload(request: Request):
    return templates.TemplateResponse('upload.html', context={'request': request})


@router.post("/upload/new/", dependencies=[Depends(get_current_username)])
async def post_upload(imgdata: tuple, file: UploadFile = File(...)):
    print(imgdata)

    # create the directory path
    workspace = create_workspace()
    # filename
    file_name = Path(file.filename)
    # image full path
    img_full_path = workspace / file_name

    with open(str(img_full_path), 'wb') as myfile:
        contents = await file.read()
        myfile.write(contents)

        myfile.seek(0, os.SEEK_END)
        size = myfile.tell()

        if size < 8000000:
            send_webhook(file_path=str(img_full_path), filename=str(file_name))
        else:
            send_webhook(file_path=str(img_full_path), filename=None)
    
    data = {
        "img_path": img_full_path,
        "thumb_path": file_name
    }
    return data
