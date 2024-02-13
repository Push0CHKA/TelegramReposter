from sqlalchemy import select, and_, distinct
from sqlalchemy.exc import SQLAlchemyError

from database.database import SessionLocal
from database.db_schema import DonorTargetMsgID, DonorTargetChatID


async def insert_data(data: list):
    try:
        async with SessionLocal() as db:
            db.add_all(data)
            await db.commit()
    except SQLAlchemyError:
        await db.rollback()


async def get_target_msg_id(
        target_chat_id: int, donor_chat_id: int, donor_msg_id: int
):
    try:
        async with SessionLocal() as db:
            target_id = await db.execute(
                select(DonorTargetMsgID.target_msg_id)
                .where(and_(
                    DonorTargetMsgID.donor_chat_id == donor_chat_id,
                    DonorTargetMsgID.target_chat_id == target_chat_id,
                    DonorTargetMsgID.donor_msg_id == donor_msg_id,
                )
                )
            )
            target_id = target_id.scalars().one()
        return target_id
    except SQLAlchemyError:
        ...


async def get_target_msg_ids(
        target_chat_id: int, donor_chat_id: int, donor_msg_ids: list
) -> list[int]:
    try:
        async with SessionLocal() as db:
            target_msg_ids = await db.execute(
                select(DonorTargetMsgID.target_msg_id)
                .where(and_(
                    DonorTargetMsgID.donor_msg_id.in_(donor_msg_ids),
                    DonorTargetMsgID.target_chat_id == target_chat_id,
                    DonorTargetMsgID.donor_chat_id == donor_chat_id,
                )
                )
            )
            target_msg_ids = target_msg_ids.scalars().all()
        return target_msg_ids
    except SQLAlchemyError:
        ...


async def get_target_chat_ids(donor_chat_id: int) -> list[DonorTargetChatID]:
    try:
        async with SessionLocal() as db:
            target_ids = await db.execute(
                select(DonorTargetChatID)
                .where(DonorTargetChatID.donor_chat_id == donor_chat_id)
            )
            target_ids = target_ids.scalars().all()
        return target_ids
    except SQLAlchemyError:
        ...


async def get_donor_chat_ids() -> list[DonorTargetChatID.donor_chat_id]:
    try:
        async with SessionLocal() as db:
            target_ids = await db.execute(
                select(distinct(DonorTargetChatID.donor_chat_id))
            )
            target_ids = target_ids.scalars().all()
        return target_ids
    except SQLAlchemyError:
        ...



