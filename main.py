from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from cviceni import Tridy, Lekce, Operand1, Operand2, Vysledek, ParametryBinarni, ParametryPosl

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


@app.get("/matematika/test")
def read_test():
    return {"zadani": [1, "+", 2, "=", 3], "neznama": 4}

@app.get("/matematika/seznam_tridy")
def seznam_tridy():
    return Tridy().seznam()

@app.get("/matematika/seznam_cviceni/{id_trida}")
def seznam_cviceni(id_trida):
    return Lekce().seznam(int(id_trida))

@app.get("/matematika/{id_trida}/{id_cviceni}")
def priklad(id_trida, id_cviceni):
    priklad = Lekce().get_priklad(int(id_trida), int(id_cviceni))
    if isinstance(priklad.parametry, ParametryBinarni):
        if priklad.zadani.typ is Operand1: neznama = 0
        elif priklad.zadani.typ is Operand2: neznama = 2
        else: neznama = 4
        return {"zadani": [priklad.parametry.a, priklad.zadani.op_text, priklad.parametry.b, "=", priklad.parametry.c], "neznama": neznama}
    elif isinstance(priklad.parametry, ParametryPosl):
        zadani = []
        for i in range(len(priklad.parametry.a)):
            n = priklad.parametry.a[i]
            if i == 0:
                zadani.append(n)
            else:
                zadani.append("+" if 0 <= n else "–")
                zadani.append(abs(n))
        zadani.append("=")
        zadani.append(priklad.parametry.b)
        return {"zadani": zadani, "neznama": 2 * priklad.zadani.neznama}
    else:
        raise TypeError('Unsupported type ' + type(priklad.parametry))
