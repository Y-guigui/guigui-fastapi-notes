print("🔥 正在加载 MAIN.PY！")
from fastapi import FastAPI,Path,Query
from pydantic import BaseModel, Field
from fastapi.responses import HTMLResponse


app = FastAPI()


class User(BaseModel):
    username: str = Field(description="用户名-----2-10个字", min_length=2, max_length=10)
    password: str = Field(description="密码-----", min_length=5, max_length=50)


@app.post("/user")
async def create_user(user: User):
    return {"username": user.username, "password": user.password}

# 接口6------Field

class Book(BaseModel):
 name: str = Field(min_length=2, max_length=20)
 author: str = Field(min_length=2, max_length=10)
 publisher: str = Field(default="XX出版社")
 price: float = Field(gt = 0)

@app.post("/book")
async def create_book(book: Book):
 return {"name":book.name,"author":book.author, "publisher":book.publisher, "price":book.price}