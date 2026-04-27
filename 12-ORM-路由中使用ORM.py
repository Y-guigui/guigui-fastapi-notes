from datetime import datetime

from sqlalchemy import DateTime, func, Integer, String, Float, select

print("🔥 正在加载 MAIN.PY！")
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
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


# 查询功能： 查询功能接口，查询图书--依赖注入:创建依赖项获取数据库对话 + Depends 注入路由处理函数
AsyncSessionLocal = async_sessionmaker(
    bind = async_engine, # 绑定数据库引擎
    class_ = AsyncSession, # 指定会话类
    expire_on_commit = False, # 提交后会话不过期，不会重新查询数据库
)

# 依赖项
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session # 返回数据库会话---给路由处理函数
            await session.commit() # 提交事务
        except Exception:
            await session.rollback() # 出现异常，回滚
            raise
        finally:
            await session.close() # 关闭会话

@app.get("/book/books")
async def get_books_list(db: AsyncSession = Depends(get_db)):
    # 查询
    result = await db.execute(select(Book))
    book = result.scalars().all()
    return book
