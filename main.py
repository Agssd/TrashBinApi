from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import init_db
from .endpoints import users, classify, auth, trash_bins

app = FastAPI(title="ML Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(classify.router)
app.include_router(auth.router)
app.include_router(trash_bins.router)

init_db()
