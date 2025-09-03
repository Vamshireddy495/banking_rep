from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
from contextlib import asynccontextmanager
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
#routers
from app.api import auth as auth_router
from app.api import user as user_router
from app.api import transaction as transaction_router
from app.api import account as account_router

from app.api import pages as pages_router

#Database / models <imports modesl so they are registered with SQLAlchemy md>
from app.core.database import Base, engine

import app.models.user
import app.models.account
import app.models.transaction

logger = logging.getLogger("uvicorn.error")

app = FastAPI(title="Banking App ", version="0.1.0")

app.include_router(user_router.router, prefix="/users", tags=["users"])
app.include_router(transaction_router.router, prefix="/transactions", tags=["transactions"])
app.include_router(account_router.router, prefix="/accounts", tags=["accounts"])
app.include_router(auth_router.router, prefix="/auth", tags=["auth"])
app.include_router(pages_router.router, tags=["pages"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

templates = Jinja2Templates(directory="app/templates")

app.mount("/static", StaticFiles(directory="app/static"), name = "static")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html",{"request":request})


# @asynccontextmanager
# async def lifespan(app:FastAPI):
#     Base.metadata.create_all(bind=engine)
#       yield
# | Aspect         | Data Analysis Libraries                       | Data Extraction / API Libraries          |
# | -------------- | --------------------------------------------- | ---------------------------------------- |
# | **Used for**   | Analyzing, transforming, and visualizing data | Retrieving data from DBs, APIs, services |
# | **Examples**   | `pandas`, `matplotlib`, `scikit-learn`        | `SQLAlchemy`, `FastAPI`, `Requests`      |
# | **Stage**      | Post-data retrieval                           | Pre-data analysis                        |
# | **Tech Focus** | Data science, statistics, ML                  | Web dev, backend, APIs, data I/O         |
# | **Role**       | Analyst / Data Scientist                      | Backend Dev / Data Engineer              |



@app.get("/")
def root():
    return {"message": "Welcome to Banking API"}



if __name__ == "__main__":
    uvicorn.run("app.main:app", host="localhost", port=8000, reload=True)














# import logging

# logging.basicConfig(
#     level=logging.DEBUG,  # <- allows DEBUG logs to appear
#     format="%(asctime)s - %(levelname)s - %(message)s"
# )
