from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_connection import Base, async_session


class BaseOperation:
    def __init__(self, session=async_session):
        self.session = session()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            await self.session.commit()
        except exc_type:
            await self.session.rollback()
        finally:
            await self.session.close()

    async def _save_object(self, object: Base):
        self.session.add(object)
        await self.session.commit()
        await self.session.refresh(object)
