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
        zadani = self.priklady[0].zadani

        # Vypis nadpis prvniho prikladu
        print("Cvičení: %s" % zadani.nadpis)

        # Vypis ciselnou osu
        if isinstance(zadani, ZadaniBinarni):
            if zadani.do <= 20:
                osa = "Číselná osa   "
                for i in range(zadani.od, zadani.do + 1):
                    if osa != "":
                        osa += " "
                    osa += str(i)
                print(osa)

        for zadani in self.priklady:
            zadani.tisk()


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

    def over_vysledek(self, parametry):
        if self.nezajimave(parametry):
            hranice = 1 - (1 / self.do)
            if random() < hranice:
                return False

        return self.od <= parametry.c <= self.do

    def nezajimave(self, parametry):
        # Nezajimave prametry jsou:
        # 1) trivialni nebo
        # 2) jednoduche (nedostatecne velka cisla)
        return self.trivialni(parametry) or self.jednoduche(parametry)

    def trivialni(self, parametry):
        if self.do <= 10:
            return False
        if parametry.a in [0, 1]:
            return True
        if parametry.b in [0, 1]:
            return True
        if parametry.c in [0, 1]:
            return True
        return False

    def jednoduche(self, parametry):
        if self.do <= 20:
            return False
        hranice = 0.6 * self.do
        if parametry.a < hranice and parametry.b < hranice and parametry.c < hranice:
            return True
        return False

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


class OdcitaniOdectiMeneNezPet(Odcitani):
    nadpis = "Odčítání (odečti méně nez pět)"

    def over_vysledek(self, parametry):
        if 5 < parametry.b:
            return False

        return super().over_vysledek(parametry)


class OdcitaniOdectiViceNezPet(Odcitani):
    nadpis = "Odčítání (odečti více nez pět)"

    def over_vysledek(self, parametry):
        if parametry.b <= 5:
            return False

        return super().over_vysledek(parametry)


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

def ciselna_osa_svisle():
    osa = "Číselná osa\n"
    for i in range(20, -11, -1):
        osa += "%3d\n" % i
    print(osa, end="")


ciselna_osa_svisle()

vytvor2(Scitani, 1, 5)
vytvor2(Scitani, 1, 10)
vytvor(Scitani, 10)

vytvor(OdcitaniOdectiMeneNezPet, 10)
vytvor(OdcitaniOdectiViceNezPet, 10)

vytvor2(OdcitaniSeZapornymi, -10, 10)
vytvor2(ScitaniSeZapornymi, -10, 10)

for do in [10, 13, 20, 30, 50]:
    vytvor(Scitani, do)
    vytvor(Scitani, do, Operand1)
    vytvor(Scitani, do, Operand2)

    vytvor(Odcitani, do)
    vytvor(Odcitani, do, Operand1)
    vytvor(Odcitani, do, Operand2)

    if do % 10 != 0:  # Priklady na nasobeni a deleni nepotrebuji mezikroky
        continue

    vytvor(Nasobeni, do)
    vytvor(Nasobeni, do, Operand1)
    vytvor(Nasobeni, do, Operand2)

    vytvor(Deleni, do)
    vytvor(Deleni, do, Operand1)
    vytvor(Deleni, do, Operand2)


class Posloupnost(Zadani):
    """
A0 + A1 + ... + An-1 = B
pro každé i: od <= Ai <= do
    """

    def __init__(self, N, od, do, neznama=None):
        # Sestav nadpis
        nadpis = "Posloupnost operací"
        nadpis += " délky %d" % N
        nadpis += ", čísla od %d do %d" % (od, do)
        if neznama != None:
            nadpis += ", doplň %d. číslo" % neznama
        super().__init__(nadpis)

        if neznama == None:
            neznama = N

        self.N = N
        self.od = od
        self.do = do
        self.neznama = neznama

    def vstup_nahodny(self):
        parmametry = ParametryPosl()
        parmametry.a = []
        for i in range(self.N):
            n = randint(self.od, self.do)
            parmametry.a.append(n)
        return parmametry

    def spocitej(self, parametry):
        parametry.b = functools.reduce(lambda x, y: x + y, parametry.a)

    def tisk(self, parametry):
        s = ""
        for i in range(len(parametry.a)):
            n = parametry.a[i]
            if i == self.neznama:
                if i != 0:
                    s += " + "
                s += "…"
            else:
                if i == 0:
                    s += str(n)
                else:
                    s += " + " if 0 <= n else " – "
                    s += str(abs(n))
        s += " = "
        s += str(parametry.b) if self.N != self.neznama else "…"
        print(s)

    def __eq__(self, item):
        if self.__class__ != item.__class__:
            return False
        if self.N != item.N:
            return False
        if self.od != item.od:
            return False
        if self.do != item.do:
            return False
        return True


class ParametryPosl(Parametry):
    a = None
    b = None

    def __eq__(self, item):
        if self.__class__ != item.__class__:
            return False
        if len(self.a) != len(item.a):
            return False
        for i in range(len(self.a)):
            if self.a[i] != item.a[i]:
                return False
        if self.b != item.b:
            return False
        return True


def vytvorPosl(N, od, do, neznama=None, pocet=20):
    c = Cviceni(Posloupnost(N, od, do, neznama), pocet)
    c.vyrob()
    c.tisk()


vytvorPosl(3, 1, 5)
vytvorPosl(3, 1, 5, 0)
vytvorPosl(3, 1, 5, 1)
vytvorPosl(3, 1, 5, 2)

vytvorPosl(4, 1, 5)
vytvorPosl(4, 1, 5, 0)
vytvorPosl(4, 1, 5, 1)
vytvorPosl(4, 1, 5, 2)
vytvorPosl(4, 1, 5, 3)

# Vcetne zapornych cisel

vytvorPosl(3, -5, 5)
vytvorPosl(3, -5, 5, 0)
vytvorPosl(3, -5, 5, 1)
vytvorPosl(3, -5, 5, 2)

vytvorPosl(4, -5, 5)
vytvorPosl(4, -5, 5, 0)
vytvorPosl(4, -5, 5, 1)
vytvorPosl(4, -5, 5, 2)
vytvorPosl(4, -5, 5, 3)

# Velka cisla
vytvorPosl(3, -20, 20)
vytvorPosl(3, -20, 20, 0)
vytvorPosl(3, -20, 20, 1)
vytvorPosl(3, -20, 20, 2)
