import uvicorn
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from app_config import origins, title, description
from authentication.login import token_router
# from routes import get, post, patch, delete
# from routes import get1, post1, patch1, delete1 #, test
from routes import all_routes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

app = FastAPI(
    title=title,
    description=description,
    root_path="/api"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(token_router)
# app.include_router(user.registration)
# app.include_router(post.router)
# app.include_router(get.router)
# app.include_router(patch.router)
# app.include_router(delete.router)
# app.include_router(test.router)
app.include_router(all_routes.router)


@app.get("/")
def home(token: str = Depends(oauth2_scheme)):
    return {"token": token}


# if __name__ == "__main__":
    # uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)
