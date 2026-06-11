from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from . import models, schemas


async def get_cameras(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Camera).offset(skip).limit(limit))
    return result.scalars().all()


async def create_camera(db: AsyncSession, camera: schemas.CameraCreate):
    db_camera = models.Camera(**camera.dict())
    db.add(db_camera)
    await db.commit()
    await db.refresh(db_camera)
    return db_camera


async def create_user(db: AsyncSession, user: schemas.UserCreate):
    # In a real app, hash the password here
    db_user = models.User(
        username=user.username, email=user.email, hashed_password=user.password
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
