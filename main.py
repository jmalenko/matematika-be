from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import os
import sys

project_root = os.path.dirname(__file__)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from cviceni import Tridy, Cviceni, Operand1, Operand2, Vysledek, ParametryBinarni, ParametryPosl, SadaPrikladu

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/matematika/test")
def read_test():
    return {"zadani": [1, "+", 2, "=", 3], "neznama": 4}

@app.get("/api/seznam")
def seznam_vse():
    tridy = Tridy().seznam()
    dict_tridy = {}
    for id_trida, nazev_trida in tridy.items():
        seznam = Cviceni().seznam(id_trida)
        dict_zadani = {}
        for id_zadani, nazev_zadani in seznam.items():
            dict_zadani[id_zadani] = {
                "nazev_zadani": nazev_zadani
            }
        dict_tridy[id_trida] = {
            "nazev_trida": nazev_trida,
            "cviceni" : dict_zadani
        }
    seznam = {}
    seznam["matematika"] = {
        "nazev_predmet": "Matematika",
        "tridy": dict_tridy
    }
    return seznam

@app.get("/api/matematika/seznam_tridy")
def seznam_tridy():
    return Tridy().seznam()

@app.get("/api/matematika/seznam_cviceni/{id_trida}")
def seznam_cviceni(id_trida):
    return Cviceni().seznam(int(id_trida))

@app.get("/api/matematika/dalsi_cviceni/{id_trida}/{id_cviceni}")
def priklad_next(id_trida, id_cviceni):
    seznam = Cviceni().seznam(int(id_trida))
    found = False
    for id_zadani, nazev_zadani in seznam.items():
        if found:
            return {"id": id_zadani, "nazev":nazev_zadani, "end": False}
        if str(id_zadani) == str(id_cviceni):
            found = True
    return {"end": True}

@app.get("/api/matematika/info_cviceni/{id_trida}/{id_cviceni}")
def priklad_current(id_trida, id_cviceni):
    seznam = Cviceni().seznam(int(id_trida))
    cviceni_nazev = seznam[int(id_cviceni)]
    return {
        "nazev_predmet": "Matematika",
        "id_trida": id_trida,
        "nazev_trida": Tridy().seznam()[int(id_trida)],
        "id_cviceni": id_cviceni,
        "nazev_cviceni": cviceni_nazev,
        "next_cviceni": priklad_next(id_trida, id_cviceni)}

@app.get("/api/matematika/{id_trida}/{id_cviceni}")
def priklad(id_trida, id_cviceni):
    priklad = Cviceni().get_priklad(int(id_trida), int(id_cviceni))
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

@app.get("/api/matematika/{id_trida}/{id_cviceni}/tisk")
def priklad_tisk(id_trida, id_cviceni):
    zadani = Cviceni().get_zadani(int(id_trida), int(id_cviceni))
    sada = SadaPrikladu(zadani, 20)
    sada.vyrob()

    response = {}
    response["nazev_cviceni"] = zadani.nadpis

    response["priklady"] = []
    for priklad in sada.priklady:
        if priklad.zadani.typ is Operand1: neznama = 0
        elif priklad.zadani.typ is Operand2: neznama = 2
        else: neznama = 4
        response["priklady"].append(
                {"zadani": [priklad.parametry.a, priklad.zadani.op_text, priklad.parametry.b, "=", priklad.parametry.c], "neznama": neznama}
            )

    return response
