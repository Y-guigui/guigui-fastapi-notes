print("🔥 正在加载 MAIN.PY！")
from fastapi import FastAPI,Response
from pydantic import BaseModel

app = FastAPI()


'''
在fastapi里面设置响应类型：
1、在装饰器   @app.get("",response_class=HTMLResponse)--在这里面设置响应类
2、在最后返回响应对象  return FileResponse(path)
'''


class News(BaseModel):
    id : int
    title: str
    content: str

@app.get("/news/{id}", response_model=News)
async def get_news(id: int):
    return {
        "id": id,
        "title": f"这是{id}本书",
        "content": f"xxxxxxxxxxxxx",
    }