import mimetypes
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .library.helpers import openfile
from app.routers import upload

mimetypes.init()

app = FastAPI()

templates = Jinja2Templates(directory="templates")

mimetypes.add_type('application/javascript', '.js')
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(upload.router)

@app.get("/", response_class=RedirectResponse)
async def home(request: Request):
    #data = openfile("home.md")
    #return templates.TemplateResponse("page.html", {"request": request, "data": data})
    response = RedirectResponse(url='/upload')