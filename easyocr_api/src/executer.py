easyocr = None


class EasyOCRMissingException(ImportError):
    def __init__(self, msg: str = "Missing EasyOCR dependency!"):
        super().__init__(msg)


try:
    import easyocr
except ImportError:
    raise EasyOCRMissingException


from Shimarin.client.events import Event, EventPolling, EventsHandlers

import os
import asyncio
from base64 import b64decode

ev = EventsHandlers()
reader = easyocr.Reader(['en','en'])


@ev.new("captcha")
async def process_captcha(event: Event):
    print("New event:", event.identifier)
    img = event.payload
    if img == "":
        return event.reply("Image is empty!")
    img_decoded = b64decode(img.encode())
    processed_text = reader.readtext(img_decoded)
    if len(processed_text) < 1:
        return await event.reply({
            "ok": False,
            "text": "Failed to process captcha"
        })
    return await event.reply({
        "ok": True,
        "text": processed_text[0][1],
        "precision": processed_text[0][2]
    })


async def start_client():
    username = os.getenv("SHIMARIN_USERNAME")
    password = os.getenv("SHIMARIN_PASSWORD")
    async with EventPolling(ev) as poller:
        await poller.start(0.3, 
                           server_endpoint=os.getenv("SERVER_ENDPOINT", "http://localhost:2222"), 
                           custom_headers={"username": username, "password": password}
        )


def main():
    asyncio.run(start_client())
