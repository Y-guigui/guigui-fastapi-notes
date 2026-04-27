import uvicorn

if __name__ == "__main__":
    # 运行 main.py 中的 app 实例
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True  # 开启热更新，修改代码后会自动重启
    )