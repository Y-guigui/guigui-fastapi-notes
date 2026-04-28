from datetime import datetime

from sqlalchemy import DateTime, func, Integer, String, Float, select

print("🔥 正在加载 MAIN.PY！")
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pydantic import BaseModel

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


# 添加图书信息
# 用户输入  --  参数 -- 请求体
class BookBase(BaseModel):
    id: int
    bookname: str
    author: str
    price: float
    publisher: str


@app.post("/book/add_book")
async def add_book(
        # 数据接收
        book: BookBase,
        db: AsyncSession = Depends(get_db)
):
    # ORM对象--add--commit

    # book.__dict__把接收到的数据变成一个字典--{"id": 1, "bookname": "三体", ...}
    # **解包，把字典里的键值对拆开，作为参数塞进 Book() 里。
    # book_obj = Book(**book.__dict__)
    book_obj = Book(**book.model_dump())
    db.add(book_obj)
    await db.commit()
    return book_obj