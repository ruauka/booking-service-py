import uvicorn
from fastapi import FastAPI

from app.router.user import router as router_user
from app.router.auth.handlers import router as router_auth

app = FastAPI()

app.include_router(router_auth)
app.include_router(router_user)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    # PYTHONPATH=$PWD python main.py
    # uvicorn main:app --reload
