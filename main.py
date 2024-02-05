from telethon import TelegramClient, events, types
from PIL import Image

from config import (
    API_ID,
    API_HASH,
    FUTURES_DONOR_ID,
    FUTURES_ID,
    WORKING_DIR,
    SPOT_DONOR_ID,
    SPOT_ID,
)

client = TelegramClient(
    session="client",
    api_id=API_ID,
    api_hash=API_HASH,
)


def crop_img(path: str):
    """Обрезка изображений"""
    im = Image.open(path)
    im = im.crop((0,
                  30,
                  im.width,
                  im.height - 30))
    im.save(path)


@client.on(events.NewMessage(chats=[FUTURES_DONOR_ID, SPOT_DONOR_ID]))
async def futures_new_message_handler(message: types.Message):
    """Воруем посты с приваток в свою"""
    if message.message.peer_id.channel_id == FUTURES_DONOR_ID:
        send_id = FUTURES_ID
    else:
        send_id = SPOT_ID
    try:  # проверка на изображение
        _ = message.media.photo
        await client.download_media(
            message.media.photo,  # noqa
            f"{WORKING_DIR}/files/{message.id}.png"
        )
        crop_img(f"{WORKING_DIR}/files/{message.id}.png")
        is_photo = True
    except AttributeError:
        is_photo = False
    if is_photo:
        await client.send_file(
            entity=send_id,
            file=f"{WORKING_DIR}/files/{message.id}.png",
            caption=message.message.message  # noqa
        )
    else:
        await client.send_message(
            entity=send_id,
            message=message.message.message  # noqa
        )


client.start()
client.run_until_disconnected()
