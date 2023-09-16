import os.path
import uuid
from pathlib import Path
import markdown
from ..config import settings
from .settings import DISCORD_WEBHOOK, DOMAIN

from discord_webhook import DiscordWebhook,  DiscordEmbed

def openfile(filename):
    filepath = os.path.join("app/pages/", filename)
    with open(filepath, "r", encoding="utf-8") as input_file:
        text = input_file.read()

    html = markdown.markdown(text)
    data = {
        "text": html
    }
    return data


def create_workspace():
    """
    Return workspace path
    """
    # base directory
    work_dir = Path(settings.work_dir)
    # UUID to prevent file overwrite
    request_id = Path(str(uuid.uuid4())[:8])
    # path concat instead of work_dir + '/' + request_id
    workspace = work_dir / request_id
    if not os.path.exists(workspace):
        # recursively create workdir/unique_id
        os.makedirs(workspace)

    return workspace

def send_webhook(file_path: str, filename: str = None, title: str="File was uploaded"):
    webhook = DiscordWebhook(url= DISCORD_WEBHOOK, username="Fileuploader")

    if filename != None:
        with open(file_path, "rb") as f:
            webhook.add_file(file=f.read(), filename=filename)

    url = DOMAIN + "/" + file_path

    embed = DiscordEmbed(title=title, description=url, color='03b2f8')

    webhook.add_embed(embed)
    response = webhook.execute()
    