import os

from telethon import TelegramClient, events, types

from config.config import (
    API_ID,
    API_HASH,
    TMP_DIR, ADMIN_CHAT_ID, DONOR_CHATS_IDS,
)
from database.crud import get_target_msg_id, get_target_msg_ids, insert_data
from database.db_schema import DonorTargetMsgID
from mods.common import get_target_chats_ids, is_contain_stop_words
from mods.media import crop_img


client = TelegramClient(
    session="client",
    api_id=API_ID,
    api_hash=API_HASH,
)


@client.on(events.NewMessage(chats=DONOR_CHATS_IDS))
async def futures_new_message_handler(message: types.Message):
    """Обработчик новых постов с приваток"""
    if is_contain_stop_words(message.message.text):  # noqa
        return
    # открытый канал
    target_chat_ids, donor_chat_id = await get_target_chats_ids(
        message.message.peer_id.channel_id  # noqa
    )
    reply_msg_ids = dict()
    # проверяем есть ли ответ на сообщение
    if hasattr(message.reply_to, "reply_to_msg_id"):
        for target_chat_id in target_chat_ids:
            reply_msg_ids[target_chat_id] = await get_target_msg_id(
                donor_msg_id=message.reply_to.reply_to_msg_id,
                donor_chat_id=donor_chat_id,
                target_chat_id=target_chat_id,
            )
    else:
        for target_chat_id in target_chat_ids:
            reply_msg_ids[target_chat_id] = None

    msgs = list()
    if hasattr(message.media, "photo"):  # проверка на изображение
        await client.download_media(
            message.media.photo,  # noqa
            f"/tmp/reposter/{message.id}.png"
        )
        crop_img(f"{TMP_DIR}/{message.id}.png")
        for target_chat_id in target_chat_ids:
            msg = await client.send_file(
                entity=target_chat_id,
                file=f"{TMP_DIR}/{message.id}.png",
                caption=message.message.text,  # noqa
                reply_to=reply_msg_ids[target_chat_id],
            )
            msgs.append(
                DonorTargetMsgID(
                    donor_chat_id=donor_chat_id,
                    target_chat_id=target_chat_id,
                    donor_msg_id=message.id,
                    target_msg_id=msg.id,
                )
            )
        os.remove(f"{TMP_DIR}/{message.id}.png")
    elif hasattr(message.media, "video"):
        for target_chat_id in target_chat_ids:
            msg = await client.send_file(
                entity=target_chat_id,
                file=message.media,
                caption=message.message.text,  # noqa
                reply_to=reply_msg_ids[target_chat_id],
            )
            msgs.append(
                DonorTargetMsgID(
                    donor_chat_id=donor_chat_id,
                    target_chat_id=target_chat_id,
                    donor_msg_id=message.id,
                    target_msg_id=msg.id,
                )
            )
    else:
        for target_chat_id in target_chat_ids:
            msg = await client.send_message(
                entity=target_chat_id,
                message=message.message.text,  # noqa
                reply_to=reply_msg_ids[target_chat_id],
            )
            msgs.append(
                DonorTargetMsgID(
                    donor_chat_id=donor_chat_id,
                    target_chat_id=target_chat_id,
                    donor_msg_id=message.id,
                    target_msg_id=msg.id,
                )
            )
    await insert_data(msgs)


@client.on(events.MessageEdited(chats=DONOR_CHATS_IDS))
async def futures_new_message_handler(message: types.Message):
    """Обработчик измененных сообщений"""
    target_chat_ids, donor_chat_id = await get_target_chats_ids(
        message.message.peer_id.channel_id  # noqa
    )
    target_msg_ids = dict()
    for target_chat_id in target_chat_ids:
        target_msg_ids[target_chat_id] = await get_target_msg_id(
            target_chat_id=target_chat_id,
            donor_chat_id=donor_chat_id,
            donor_msg_id=message.id,
        )
    if not target_msg_ids:
        return
    if hasattr(message.media, "photo"):  # проверка на изображение
        await client.download_media(
            message.media.photo,  # noqa
            f"{TMP_DIR}/{message.id}.png"
        )
        crop_img(f"{TMP_DIR}/{message.id}.png")
        for target_chat_id in target_chat_ids:
            await client.edit_message(
                entity=target_chat_id,
                message=target_msg_ids[target_chat_id],
                file=f"{TMP_DIR}/{message.id}.png",
                text=message.message.text  # noqa
            )
    elif hasattr(message.media, "video"):
        for target_chat_id in target_chat_ids:
            await client.edit_message(
                entity=target_chat_id,
                message=target_msg_ids[target_chat_id],
                file=message.media,
                text=message.message.text  # noqa
            )
    else:
        for target_chat_id in target_chat_ids:
            await client.edit_message(
                entity=target_chat_id,
                message=target_msg_ids[target_chat_id],
                text=message.message.text  # noqa
            )


@client.on(events.MessageDeleted(chats=DONOR_CHATS_IDS))
async def futures_new_message_handler(messages: types.UpdateDeleteMessages):
    """Обработчик удаления постов"""
    target_chat_ids, donor_chat_id = await get_target_chats_ids(
        messages.original_update.channel_id  # noqa
    )
    target_msg_ids = dict()
    for target_chat_id in target_chat_ids:
        target_msg_ids[target_chat_id] = await get_target_msg_ids(
            target_chat_id=target_chat_id,
            donor_chat_id=donor_chat_id,
            donor_msg_ids=messages.original_update.messages  # noqa
        )
    if not target_msg_ids:
        return
    for target_chat_id in target_chat_ids:
        await client.delete_messages(
            entity=target_chat_id,
            message_ids=target_msg_ids[target_chat_id]
        )


@client.on(events.NewMessage(chats=[ADMIN_CHAT_ID], pattern=r"/start"))
async def start_handler(_):
    await client.send_message(
        entity=ADMIN_CHAT_ID,
        message="Список команд:\n"
                "/list - список каналов "
                "(<strong>донор</strong>:<strong>целевой</strong>)\n",
        parse_mode="html"
    )


def main():
    if not os.path.isdir(TMP_DIR):
        os.mkdir(TMP_DIR)
    client.start()
    client.run_until_disconnected()


if __name__ == "__main__":
    main()

# from database.database import create_db
# asyncio.run(create_db())

