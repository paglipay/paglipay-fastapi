from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(post.router)
# app.include_router(user.router)
# app.include_router(auth.router)
# app.include_router(vote.router)


@app.get("/")
def root():
    lucky_num = random.randint(1,1000)
    return {"message": f"Hello World pushing out to ubuntu. Your lucky number for today is {lucky_num}"}