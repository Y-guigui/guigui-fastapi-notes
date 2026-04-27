print("🔥 正在加载 MAIN.PY！")
from fastapi import FastAPI,Path,Query
from pydantic import BaseModel, Field
from fastapi.responses import HTMLResponse


app = FastAPI()

'''
它们没有出现在装饰器的路由路径中（例如 @app.get("/news/news_list") 中没有 {} 占位符）。

在函数定义中，使用了 Query() 来进行声明、设置默认值和校验。
'''

@app.get("/news/news_list")
async def get_news_list(
        skip: int = Query(0,description="跳过的记录数", gt=0, lt=100),
        limit: int = Query(10, description="返回的记录数"),
):
    return {"skip":skip, "limit":limit}

@app.get("/get/getitem")
async def get_getitem(
        category: str = Query("Python开发",min_length=5, max_length=255, description="图书分类"),
        price: float = Query(..., ge=50, le=100, description="图书价格")
):
    return {
        "message": "查询成功！",
        "查询的分类": category,
        "查询的价格": price
    }