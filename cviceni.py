import functools
from random import random, randint


class Cviceni:
    def __init__(self, zadani, pocetPrikladu=10):
        self.zadani = zadani
        self.pocetPrikladu = pocetPrikladu
        self.priklady = []

    def vyrob(self):
        dup_zbyva = 100
        while len(self.priklady) < self.pocetPrikladu:
            priklad = self.zadani.vyrob_priklad()

            # Odstranit duplicity
            if priklad in self.priklady and 0 < dup_zbyva:
                dup_zbyva -= 1
                continue

            self.priklady.append(priklad)

    def tisk(self):
        print(self.priklady[0].zadani.nadpis)  # Vypis nadpis prvniho prikladu
        for priklad in self.priklady:
            priklad.tisk()


class Priklad:
    def __init__(self, zadani, parametry):
        self.zadani = zadani
        self.parametry = parametry

    def tisk(self):
        self.zadani.tisk(self.parametry)

    def __eq__(self, item):
        if self.zadani != item.zadani:
            return False
        if self.parametry != item.parametry:
            return False
        return True


class Zadani:
    def __init__(self, nadpis):
        self.nadpis = nadpis

    def vyrob_priklad(self):
        while True:
            try:
                parametry = self.vstup_nahodny()
                self.spocitej(parametry)
                if self.over_vysledek(parametry):
                    break
            except:
                continue
        return Priklad(self, parametry)

    def vstup_nahodny(self):
        raise NotImplementedError()

    def spocitej(self, parametry):
        raise NotImplementedError()

    def over_vysledek(self, parametry):
        return True

    def tisk(self, parametry):
        raise NotImplementedError()


class Parametry:
    pass


# Binarni

class ZadaniBinarni(Zadani):
    def __init__(self, od, do, typ):
        # Sestav nadpis
        nadpis = self.nadpis
        if do <= 10:
            if od != 0:
                nadpis += " od %d" % od
        nadpis += " do %d" % do
        if typ.nadpis != "":
            nadpis += ", %s" % typ.nadpis
        super().__init__(nadpis)

        self.od = od
        self.do = do
        self.typ = typ

    def vstup_nahodny(self):
        parmametry = ParametryBinarni()
        parmametry.a = randint(self.od, self.do)
        parmametry.b = randint(self.od, self.do)
        return parmametry

    def spocitej(self, parametry):
        return self.operator.spocitej(parametry)

    def over_vysledek(self, parametry):
        if trivialni(parametry):
            hranice = 1 - self.do * self.do
            if random() < hranice:
                return False

        return self.od <= parametry.c <= self.do

    def tisk(self, parametry):
        s = ""
        s += str(parametry.a) if self.typ is not Operand1 else "…"
        s += " "
        s += self.op_text
        s += " "
        s += str(parametry.b) if self.typ is not Operand2 else "…"
        s += " = "
        s += str(parametry.c) if self.typ is not Vysledek else "…"
        print(s)

    def __eq__(self, item):
        if self.__class__ != item.__class__:
            return False
        return True


class ParametryBinarni(Parametry):
    a = None
    b = None
    c = None

    def __eq__(self, item):
        if self.__class__ != item.__class__:
            return False
        if self.a != item.a:
            return False
        if self.b != item.b:
            return False
        return True


class Scitani(ZadaniBinarni):
    nadpis = "Sčítání"
    op_text = "+"

    def spocitej(self, parametry):
        parametry.c = parametry.a + parametry.b


class Odcitani(ZadaniBinarni):
    nadpis = "Odčítání"
    op_text = "–"

    def spocitej(self, parametry):
        parametry.c = parametry.a - parametry.b


class Nasobeni(ZadaniBinarni):
    nadpis = "Násobení"
    op_text = "·"

    def spocitej(self, parametry):
        parametry.c = parametry.a * parametry.b


class Deleni(ZadaniBinarni):
    nadpis = "Dělení"
    op_text = ":"

    def spocitej(self, parametry):
        parametry.c = parametry.a / parametry.b

    def over_vysledek(self, parametry):
        # Konverze na cele cislo
        if int(parametry.c) != parametry.c:
            return False
        parametry.c = int(parametry.c)

        return super().over_vysledek(parametry)


def trivialni(parametry):
    if parametry.a in [0, 1]:
        return True
    if parametry.b in [0, 1]:
        return True
    if parametry.c in [0, 1]:
        return True
    return False


class OdcitaniSeZapornymi(Odcitani):
    nadpis = "Odčítání se zápornými čísly"

    def over_vysledek(self, parametry):
        if parametry.b < 0:
            return False
        if 0 <= parametry.c:
            return False

        return super().over_vysledek(parametry)


class ScitaniSeZapornymi(Scitani):
    nadpis = "Sčítání se zápornými čísly"

    def over_vysledek(self, parametry):
        if 0 <= parametry.a and 0 <= parametry.b:
            return False

        return super().over_vysledek(parametry)


class Clen():
    pass


class Operand1(Clen):
    nadpis = "doplň první operand"


class Operand2(Clen):
    nadpis = "doplň druhý operand"


class Vysledek(Clen):
    nadpis = ""


def vytvor2(operator, od, do, dopln=Vysledek, pocet=20):
    c = Cviceni(operator(od, do, dopln), pocet)
    c.vyrob()
    c.tisk()


def vytvor(operator, do, dopln=Vysledek, pocet=20):
    vytvor2(operator, 0, do, dopln, pocet)


# vytvor(Scitani, 10)
# vytvor(Odcitani, 10)
# vytvor(Nasobeni, 10)
# vytvor(Deleni, 10)

vytvor2(Scitani, 1, 5)
vytvor2(Scitani, 1, 10)
vytvor(Scitani, 10)

vytvor2(OdcitaniSeZapornymi, -10, 10)
vytvor2(ScitaniSeZapornymi, -10, 10)

for do in [10, 13, 20, 30]:
    vytvor(Scitani, do)
    vytvor(Scitani, do, Operand1)
    vytvor(Scitani, do, Operand2)

    vytvor(Odcitani, do)
    vytvor(Odcitani, do, Operand1)
    vytvor(Odcitani, do, Operand2)

    vytvor(Nasobeni, do)
    vytvor(Nasobeni, do, Operand1)
    vytvor(Nasobeni, do, Operand2)

    vytvor(Deleni, do)
    vytvor(Deleni, do, Operand1)
    vytvor(Deleni, do, Operand2)

print("zaporna")

print("posloupnosti")

print("ciselna osa")

exit()


class OdcitaniDoDesetiOdectiMeneNezPet(OdcitaniDoDeseti):
    def __init__(self):
        super().__init__("Odčítání do deseti, odečti méně než pět")

    def over_vysledek(self):
        return super().over_vysledek() and self.b < 5


class OdcitaniDoDesetiOdectiViceNezPet(OdcitaniDoDeseti):
    def __init__(self):
        super().__init__("Odčítání do deseti, odečti více než pět (včetně)")

    def over_vysledek(self):
        return super().over_vysledek() and 5 <= self.b


class Posloupnost(Priklad):
    """
A1 + A2 + ... + An = B
pro každé i: Ai < max
    """

    def __init__(self, nadpis="", N=3, max=5, neznama=None):
        if nadpis == "":
            nadpis = "Posloupnost operací"
        if neznama == None:
            neznama = N
        super().__init__(nadpis)
        self.N = N
        self.max = max
        self.neznama = neznama

    def vstup_nahodny(self):
        self.a = []
        for i in range(self.N):
            if i == 0:
                n = randint(1, self.max)  # Zjednoduseni
            else:
                n = randint(-self.max, self.max)
            self.a.append(n)

    def over_vysledek(self):
        return self.b <= 2 * abs(self.max)

    def spocitej(self):
        self.b = functools.reduce(lambda x, y: x + y, self.a)

    def tisk(self):
        for i in range(len(self.a)):
            n = self.a[i]
            if i == self.neznama:
                if i == 0:
                    print("…", end="")
                else:
                    print(" + …", end="")
            else:
                if i == 0:
                    print(n, end="")
                else:
                    print(" + " if 0 <= n else " – ", end="")
                    print(abs(n), end="")
        print(" = ", end="")
        if self.N == self.neznama:
            print("…", end="")
        else:
            print(self.b, end="")
        print("")


class PosloupnostTriScitance(Posloupnost):
    def __init__(self, nadpis=""):
        if nadpis == "":
            nadpis = "Tři sčítance"
        super().__init__(nadpis)

    def vstup_nahodny(self):
        self.a = []
        for i in range(self.N):
            n = randint(1, self.max)
            self.a.append(n)


c = Cviceni(PosloupnostTriScitance, 20)
c.vyrob()
c.tisk()


class PosloupnostCtyriScitance(Posloupnost):
    def __init__(self, nadpis=""):
        if nadpis == "":
            nadpis = "Čtyři sčítance"
        super().__init__(nadpis, N=4)

    def vstup_nahodny(self):
        self.a = []
        for i in range(self.N):
            n = randint(1, self.max)
            self.a.append(n)


c = Cviceni(PosloupnostCtyriScitance, 20)
c.vyrob()
c.tisk()


class PosloupnostTriScitanceNeznama2(PosloupnostTriScitance):
    def __init__(self, nadpis=""):
        super().__init__(nadpis)
        self.neznama = 2


c = Cviceni(PosloupnostTriScitanceNeznama2, 20)
c.vyrob()
c.tisk()


class PosloupnostTriScitanceNeznama1(PosloupnostTriScitance):
    def __init__(self, nadpis=""):
        super().__init__(nadpis)
        self.neznama = 1


c = Cviceni(PosloupnostTriScitanceNeznama1, 20)
c.vyrob()
c.tisk()


class PosloupnostTriScitanceNeznama0(PosloupnostTriScitance):
    def __init__(self, nadpis=""):
        super().__init__(nadpis)
        self.neznama = 0


c = Cviceni(PosloupnostTriScitanceNeznama0, 20)
c.vyrob()
c.tisk()


class PosloupnostTri(Posloupnost):
    def __init__(self, nadpis=""):
        if nadpis == "":
            nadpis = "Tři čísla, ruzné operace"
        super().__init__(nadpis)

    def over_vysledek(self):
        return super().over_vysledek() \
               and functools.reduce(lambda a1, a2: a1 and a2,  # pro každé i: Ai >= 0
                                    map(lambda a1: 0 <= a1, self.a)  # B >= 0
                                    ) \
               and 0 <= self.b  # positive b


c = Cviceni(PosloupnostTri, 20)
c.vyrob()
c.tisk()


class ZapornaCislaOdcitani(Odcitani):
    def __init__(self, nadpis=""):
        super().__init__("Záporná čísla, odečti do záporného")

    def vstup_nahodny(self):
        self.a = randint(1, 5)
        self.b = randint(1, 9)

    def over_vysledek(self):
        return self.c < 0


c = Cviceni(ZapornaCislaOdcitani, 20)
c.vyrob()
c.tisk()


class ZapornaCislaScitani(Scitani):
    def __init__(self, nadpis=""):
        super().__init__("Záporná čísla, přičti k zápornému")

    def vstup_nahodny(self):
        self.a = randint(-5, -1)
        self.b = randint(1, 9)

    def over_vysledek(self):
        return 0 < self.c


c = Cviceni(ZapornaCislaScitani, 20)
c.vyrob()
c.tisk()
