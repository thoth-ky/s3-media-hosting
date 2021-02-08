from fastapi import FastAPI
from typing import Optional

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "I'm up!!"}
