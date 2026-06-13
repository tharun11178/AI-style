from __future__ import annotations

import sys
from pathlib import Path

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.config import ALLOWED_ORIGINS, APP_TITLE
from app.database import create_schema
from app.routers import admin, analysis, auth, recommendations, users


app = FastAPI(title=APP_TITLE)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(ALLOWED_ORIGINS),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_private_network_header(request, call_next):
    origin = request.headers.get("origin")
    private_network = request.headers.get("access-control-request-private-network")
    if request.method == "OPTIONS" and private_network == "true" and origin in ALLOWED_ORIGINS:
        response = Response("OK", status_code=200)
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT"
        response.headers["Access-Control-Allow-Headers"] = request.headers.get(
            "access-control-request-headers",
            "authorization, content-type",
        )
        response.headers["Access-Control-Allow-Private-Network"] = "true"
        response.headers["Vary"] = "Origin"
        return response

    response = await call_next(request)
    response.headers["Access-Control-Allow-Private-Network"] = "true"
    return response


@app.on_event("startup")
def on_startup() -> None:
    create_schema()


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "AI Personal Style & Wellness Advisor API is running"}


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "style-wellness-advisor"}


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(analysis.router)
app.include_router(recommendations.router)
app.include_router(admin.router)
