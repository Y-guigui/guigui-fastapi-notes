print("🔥 正在加载 MAIN.PY！")
from fastapi import FastAPI,Path,Query
from pydantic import BaseModel, Field
from fastapi.responses import HTMLResponse


app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}

'''
1. 它出现在了装饰器的路由路径中，被大括号包裹着："/author/{name}"。
2. 在函数定义中，显式地使用了 Path() 来声明和校验。
'''

@app.get("/book/{id}")
async def get_book(id: int = Path(..., gt=0, lt=10, description="范围0-9")):
    return {"id": f"this is id: {id}"}

@app.get("/author/{name}")
async def get_name(name: str = Path(..., max_length=50, min_length=2, description="姓名2-50")):
    return {"msg": f"这是:{name}"}