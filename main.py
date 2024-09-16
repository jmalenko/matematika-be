from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import random
from cviceni import Lekce, Operand1, Operand2, Vysledek

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


@app.get("/test")
def read_test():
    return {"zadani": [1, "+", 2, "=", 3], "neznama": 4}

@app.get("/matematika/seznam")
def read_seznam_lekci():
    return Lekce().seznam()

@app.get("/matematika/{id}")
def read_priklad(id):
    priklad = Lekce().get_priklad(int(id))
    if priklad.zadani.typ is Operand1: neznama = 0
    elif priklad.zadani.typ is Operand2: neznama = 2
    else: neznama = 4
    return {"zadani": [priklad.parametry.a, priklad.zadani.op_text, priklad.parametry.b, "=", priklad.parametry.c], "neznama": neznama}
