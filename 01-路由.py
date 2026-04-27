print("🔥 正在加载 MAIN.PY！")
from fastapi import FastAPI,Path,Query
from pydantic import BaseModel, Field
from fastapi.responses import HTMLResponse


app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}

