import uvicorn
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware

from app_config import origins, title, description, servers
from app_config import api_root_path # for development leave this line in comment
from authentication.login import token_router
from authentication.registration import registration_router
from routes import all_routes, special_routes

app = FastAPI(
    title=title,
    description=description,
    servers=servers,
    root_path=api_root_path # for development leave this line in comment
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(token_router)
app.include_router(registration_router)
app.include_router(all_routes.router)
app.include_router(special_routes.router)

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)
