print("🔥 正在加载 MAIN.PY！")
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}


@app.get("/news/{id}")
async def get_news(id: int ):
    id_list = [1, 2, 3, 4, 5, 6]
    if id in id_list:
        return {"message": "Hello, FastAPI!"}
    else:
        raise HTTPException(status_code=404, detail="id不在1-6中")
