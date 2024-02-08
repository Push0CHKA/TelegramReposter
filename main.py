from telethon import TelegramClient, events, types

from config.config import (
    API_ID,
    API_HASH,
    FUTURES_DONOR_ID,
    WORKING_DIR,
    SPOT_DONOR_ID,
)
from database.crud import add_ids, get_target_id, get_target_ids
from mods.common import get_target_chat_id
from mods.media import crop_img


client = TelegramClient(
    session="client",
    api_id=API_ID,
    api_hash=API_HASH,
)


@client.on(events.NewMessage(chats=[FUTURES_DONOR_ID, SPOT_DONOR_ID]))
async def futures_new_message_handler(message: types.Message):
    """Обработчик новых постов с приваток"""
    target_chat_id = get_target_chat_id(
        donor_chat_id=message.message.peer_id.channel_id  # noqa
    )
    # проверяем есть ли ответ на сообщение
    if hasattr(message.reply_to, "reply_to_msg_id"):
        reply_msg_id = await get_target_id(
            donor_id=message.reply_to.reply_to_msg_id
        )
    else:
        reply_msg_id = None

    if hasattr(message.media, "photo"):  # проверка на изображение
        await client.download_media(
            message.media.photo,  # noqa
            f"{WORKING_DIR}/files/{message.id}.png"
        )
        crop_img(f"{WORKING_DIR}/files/{message.id}.png")
        msg = await client.send_file(
            entity=target_chat_id,
            file=f"{WORKING_DIR}/files/{message.id}.png",
            caption=message.message.text,  # noqa
            reply_to=reply_msg_id,
        )
    elif hasattr(message.media, "video"):
        msg = await client.send_file(
            entity=target_chat_id,
            file=message.media,
            caption=message.message.text,  # noqa
            reply_to=reply_msg_id,
        )
    else:
        msg = await client.send_message(
            entity=target_chat_id,
            message=message.message.text,  # noqa
            reply_to=reply_msg_id,
        )
    await add_ids(donor_id=message.id, target_id=msg.id)


@client.on(events.MessageEdited(chats=[FUTURES_DONOR_ID, SPOT_DONOR_ID]))
async def futures_new_message_handler(message: types.Message):
    """Обработчик измененных сообщений"""
    target_chat_id = get_target_chat_id(
        donor_chat_id=message.message.peer_id.channel_id  # noqa
    )
    target_msg_id = await get_target_id(message.id)
    if not target_msg_id:
        return
    if hasattr(message.media, "photo"):  # проверка на изображение
        await client.download_media(
            message.media.photo,  # noqa
            f"{WORKING_DIR}/files/{message.id}.png"
        )
        crop_img(f"{WORKING_DIR}/files/{message.id}.png")
        await client.edit_message(
            entity=target_chat_id,
            message=target_msg_id,
            file=f"{WORKING_DIR}/files/{message.id}.png",
            text=message.message.text  # noqa
        )
    elif hasattr(message.media, "video"):
        await client.edit_message(
            entity=target_chat_id,
            message=target_msg_id,
            file=message.media,
            text=message.message.text  # noqa
        )
    else:
        await client.edit_message(
            entity=target_chat_id,
            message=target_msg_id,
            text=message.message.text  # noqa
        )


@client.on(events.MessageDeleted(chats=[FUTURES_DONOR_ID, SPOT_DONOR_ID]))
async def futures_new_message_handler(messages: types.UpdateDeleteMessages):
    """Обработчик удаления постов"""
    target_chat_id = get_target_chat_id(
        donor_chat_id=messages.original_update.channel_id  # noqa
    )
    target_msg_ids = await get_target_ids(
        donor_ids=messages.original_update.messages  # noqa
    )
    if not target_msg_ids:
        return
    await client.delete_messages(
        entity=target_chat_id,
        message_ids=target_msg_ids
    )


client.start()
client.run_until_disconnected()
