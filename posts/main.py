from fastapi import FastAPI
#from posts import models, config
#from posts.database import engine
from posts.routers import user, post, auth, vote
from fastapi.middleware.cors import CORSMiddleware
# after alembic integration this command not needed any more
# models.Base.metadata.create_all(bind=engine)


app = FastAPI()


origins = [
    'https://www.google.com'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello World"}
