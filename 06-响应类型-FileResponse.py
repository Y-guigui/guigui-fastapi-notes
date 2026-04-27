print("🔥 正在加载 MAIN.PY！")
from fastapi import FastAPI
from fastapi.responses import FileResponse


app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}

# 响应文件内容
@app.get("/file")
async def get_file():
    path = "./files/1.jpg"
    return FileResponse(path)