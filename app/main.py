from fastapi import FastAPI
from routers import user
from routers import task


app = FastAPI()


@app.get("/")
async def welcome():
    return {"message": "Welcome to Taskmanager"}


if __name__ == "__main__":
    import uvicorn
    app.include_router(task.router)
    app.include_router(user.router)
    uvicorn.run(app, host="192.168.5.70", port=80)
