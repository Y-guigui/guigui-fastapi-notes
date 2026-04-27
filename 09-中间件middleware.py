print("🔥 正在加载 MAIN.PY！")
from fastapi import FastAPI, HTTPException

app = FastAPI()

'''
中间件： 为每一个请求添加统一的处理逻辑（记录日志、身份认证、跨域、设置响应头、性能监控等）
装饰器@app.middleware("http")
执行顺序：自下而上
'''


@app.middleware("http")
async def middleware1(request, call_next):
    print("start-middleware1")
    response = await call_next(request)
    print("end-middleware1")
    return response

@app.middleware("http")
async def middleware2(request, call_next):
    print("start-middleware2")
    response = await call_next(request)
    print("end-middleware2")
    return response

@app.middleware("http")
async def middleware3(request, call_next):
    print("start-middleware3")
    response = await call_next(request)
    print("end-middleware3")
    return response


@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}



