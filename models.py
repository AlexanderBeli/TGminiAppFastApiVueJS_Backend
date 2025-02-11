from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# подключение к БД, echo - логирование в терминале
engine = create_async_engine(url="sqlite+aiosqlite:#/db.sqlite3", echo=True)

# сессия, чтобы делать изменения
# expire_on_commit - чтобы после изменения сессия не закрывалась
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


# Теперь нужно создать сущности
class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    completed: Mapped[bool] = mapped_column(default=False)
    user: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))


# будем запускать при запуске бота, чтобы таблицы создались
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
