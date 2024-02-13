import asyncio

from config.config import STOP_WORDS
from database.crud import get_target_chat_ids, get_donor_chat_ids


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


async def get_target_chat_id(donor_chat_id: int):
    """Возвращает целевые id каналов"""
    ids = await get_target_chat_ids(donor_chat_id)
    return [canal_id.target_chat_id for canal_id in ids]


async def get_target_chats_ids(donor_chat_id):
    target_chat_ids = await get_target_chat_id(donor_chat_id)  # noqa
    if not target_chat_ids:  # закрытый канал
        donor_chat_id = int(f"-100{donor_chat_id}")
        target_chat_ids = await get_target_chat_id(donor_chat_id)  # noqa
    return target_chat_ids, donor_chat_id


def is_contain_stop_words(text: str) -> bool:
    if text.find("@") != -1:
        return True
    for word in text.split(" "):
        if word in STOP_WORDS:
            return True
    return False


@singleton
class Donors:
    __donor_ids = []

    @classmethod
    def get_donor_ids(cls):
        return cls.__donor_ids

    @classmethod
    async def update_donor_ids(cls):
        print(cls.__donor_ids)
        cls.__donor_ids = await get_donor_chat_ids()
        print(cls.__donor_ids)
