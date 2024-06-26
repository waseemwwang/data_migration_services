# crud.py
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.chatbot_auth import ChatbotUser
from utils.logger import log


async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(ChatbotUser).filter(ChatbotUser.id == user_id))
    return result.scalars().first()
