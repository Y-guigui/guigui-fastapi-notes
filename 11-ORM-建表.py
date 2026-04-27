from datetime import datetime

from sqlalchemy import DateTime, func, Integer, String, Float

print("🔥 正在加载 MAIN.PY！")
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

app = FastAPI()


ASYNC_DATABASE_URL = "mysql+aiomysql://root:123@localhost:3306/FastAPI_first?charset=utf8"
# 1、创建异步引擎
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo = True, # 输出sql日志
    pool_size = 10, # 设置运行连接池活跃的连接数
    max_overflow = 20, # 允许额外的连接数量
)

# 2、定义模型类： 基类 + 表对应的模型类
class Base(DeclarativeBase):
    created_time : Mapped[datetime] = mapped_column(
        DateTime,
        insert_default=func.now(),
        default=func.now(),
        comment="创建时间"
    )
    update_time : Mapped[datetime] = mapped_column(
        DateTime,
        insert_default=func.now(),
        default=func.now(),
        onupdate=func.now(),
        comment="修改时间")

class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True, comment="书籍id")
    bookname: Mapped[str] = mapped_column(String(255), comment="书名")
    author: Mapped[str] = mapped_column(String(255), comment="作者")
    price: Mapped[float] = mapped_column(Float, default=0.0, comment="价格")
    publisher: Mapped[str] = mapped_column(String(255), comment="出版社")

# 3、建表： FastAPI启动的时候调用建表函数
async def create_tables():
    # 获取异步引擎， 创建事务， 建表
    async with async_engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all) # Base 模型类的元数据创建

@app.on_event("startup")
async def startup_event():
    await create_tables()


@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}


