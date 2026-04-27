print("🔥 正在加载 MAIN.PY！")
from fastapi import FastAPI,Path,Query
from pydantic import BaseModel, Field
from fastapi.responses import HTMLResponse


app = FastAPI()



@app.get("/html", response_class=HTMLResponse)
async def get_html():
    # 返回一段 HTML 字符串
    html_content = """
        <html>
            <head>
                <title>FastAPI HTML 响应</title>
            </head>
            <body>
                <h1>🔥 这是一个 HTML 页面！</h1>
                <p>你可以直接在这里写前端代码，或者读取一个 .html 文件的内容返回。</p>
            </body>
        </html>
        """
    return HTMLResponse(content=html_content, status_code=200)