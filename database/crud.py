from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database.database import SessionLocal
from database.db_schema import DonorTargetID


async def add_ids(donor_id: int, target_id: int):
    try:
        async with SessionLocal() as db:
            db.add(DonorTargetID(
                donor_id=donor_id,
                target_id=target_id
            ))
            await db.commit()
    except SQLAlchemyError:
        await db.rollback()


async def get_target_id(donor_id: int):
    try:
        async with SessionLocal() as db:
            target_id = await db.execute(
                select(DonorTargetID.target_id)
                .where(DonorTargetID.donor_id == donor_id)
            )
            target_id = target_id.scalars().one()
        return target_id
    except SQLAlchemyError:
        ...


async def get_target_ids(donor_ids: list) -> list[int]:
    try:
        async with SessionLocal() as db:
            target_id = await db.execute(
                select(DonorTargetID.target_id)
                .where(DonorTargetID.donor_id.in_(donor_ids))
            )
            target_id = target_id.scalars().all()
        return target_id
    except SQLAlchemyError:
        ...
