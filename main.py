from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import random
import matematika

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/test")
def read_test():
    a = random.randrange(80)
    return {"zadani": [a, "+", 2, "=", a + 2], "neznama": 2}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/matematika")
def read_matematika():
    c = matematika.Cviceni(matematika.Scitani(6, 20, matematika.Vysledek), 1)
    c.vyrob()
    priklad = c.priklady[0]
    return {"zadani": [priklad.parametry.a, priklad.zadani.op_text, priklad.parametry.b, "=", priklad.parametry.c], "neznama": 2}
