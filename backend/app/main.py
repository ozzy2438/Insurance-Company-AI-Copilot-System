from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import router
from .database import SessionLocal
from .seed import seed_database

app = FastAPI(title="Member Operations Copilot Sandbox API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def bootstrap_database() -> None:
    with SessionLocal() as session:
        seed_database(session)


@app.get("/health")
def healthcheck():
    return {"status": "ok"}


app.include_router(router)
