print("🔥 正在加载 MAIN.PY！")
from fastapi import FastAPI, Depends, Query #2、导入Depends

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}

# 分页项参数共用   新闻列表-用户列表
# 1、依赖项
async def common_parameters(
        skip: int = Query(0, ge=0),
        limit: int = Query(8, le=100),
):
    return {"skip": skip, "limit": limit}

@app.get("/news/news_list")
async def get_news_list(common = Depends(common_parameters)):
    return common

@app.get("/user/user_list")
async def get_user_list(common = Depends(common_parameters)):
    return common



