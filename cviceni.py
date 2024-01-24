import functools
from random import randint


class Cviceni:
    def __init__(self, zadani, pocetPrikladu=10):
        self.zadani = zadani
        self.pocetPrikladu = pocetPrikladu
        self.priklady = []

    def vyrob(self):
        dup_zbyva = 10
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
            parametry = self.vstup_nahodny()
            self.spocitej(parametry)
            if self.over_vysledek(parametry):
                break
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
    op_text = None

    def __init__(self, operator, od, do, typ):
        # Sestav nadpis
        nadpis = operator.nadpis
        if do <= 10:
            if od != 1:
                nadpis += " od %d" % od
        nadpis += " do %d" % do
        if typ.nadpis != "":
            nadpis += ", %s" % typ.nadpis
        super().__init__(nadpis)

        self.operator = operator
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
        return self.od <= parametry.c <= self.do

    def tisk(self, parametry):
        s = ""
        s += str(parametry.a) if self.typ is not Operand1 else "…"
        s += " "
        s += self.operator.op_text
        s += " "
        s += str(parametry.b) if self.typ is not Operand2 else "…"
        s += " = "
        s += str(parametry.c) if self.typ is not Vysledek else "…"
        print(s)

    def __eq__(self, item):
        if self.__class__ != item.__class__:
            return False
        if self.operator != item.operator:
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

    def spocitej(parametry):
        parametry.c = parametry.a + parametry.b


class Odcitani(ZadaniBinarni):
    nadpis = "Odčítání"
    op_text = "–"

    def spocitej(parametry):
        parametry.c = parametry.a - parametry.b


# class Nasobeni(ZadaniBinarni):
#     nadpis = "Násobení"
#     op_text = "·"
#
#     def spocitej(parametry):
#         parametry.c = parametry.a * parametry.b
#
# class Deleni(ZadaniBinarni):
#     nadpis = "Dělení"
#     op_text = ":"
#
#     def spocitej(parametry):
#         parametry.c = parametry.a / parametry.b
#
#     def over_vysledek(self, parametry):
#         if not super.over_vysledek(parametry):
#             return False
#
#         if not int(parametry.c) == parametry.c:
#             return False
#         parametry.c = int(parametry.c)
#
#         return self.od <= parametry.c <= self.do


class Clen():
    pass


class Operand1(Clen):
    nadpis = "doplň prvního činitele"


class Operand2(Clen):
    nadpis = "doplň druhého činitele"


class Vysledek(Clen):
    nadpis = ""


def vytvor2(operator, od, do, dopln=Vysledek, pocet=20):
    c = Cviceni(ZadaniBinarni(operator, od, do, dopln), pocet)
    c.vyrob()
    c.tisk()


def vytvor(operator, do, dopln=Vysledek, pocet=20):
    vytvor2(operator, 0, do, dopln, pocet)


vytvor2(Scitani, 1, 5)
vytvor2(Scitani, 1, 10)
vytvor(Scitani, 10)

for do in [10, 13, 20, 30]:
    vytvor(Scitani, do)
    vytvor(Scitani, do, Operand1)
    vytvor(Scitani, do, Operand2)

    vytvor(Odcitani, do)
    vytvor(Odcitani, do, Operand1)
    vytvor(Odcitani, do, Operand2)

    # vytvor(Nasobeni, do)
    # vytvor(Nasobeni, do, Operand1)
    # vytvor(Nasobeni, do, Operand2)
    #
    # vytvor(Deleni, do)
    # vytvor(Deleni, do, Operand1)
    # vytvor(Deleni, do, Operand2)

print("zaporna")
print("posloupnosti")
print("nasobeni")
print("deleni")

print("ciselna osa")

exit()



class ScitaniDo(Scitani):
    def __init__(self, max, nadpis=""):
        if nadpis == "":
            nadpis = "Sčítání do %d" % (max)
        super().__init__(nadpis)
        self.max = max

    def vstup_nahodny(self):
        self.a = randint(0, self.max)
        self.b = randint(0, self.max)

    def over_vysledek(self):
        return 0 <= self.c <= self.max


class ScitaniDoDeseti(ScitaniDo):
    def __init__(self, nadpis=""):
        if nadpis == "":
            nadpis = "Sčítání do deseti"
        super().__init__(10, nadpis)


class ScitaniDoDesetiPresPet(ScitaniDoDeseti):
    def __init__(self):
        super().__init__("Sčítání do deseti přes pět")

    def over_vysledek(self):
        return super().over_vysledek() and 6 <= self.c


class ScitaniDoplnPrvnihoCinitele(Scitani):
    def __init__(self, nadpis=""):
        if nadpis == "":
            nadpis = "Doplň prvního činitele"
        super().__init__(nadpis)

    def tisk(self):
        print("… + %d = %d" % (self.a, self.c))


class ScitaniDoplnDruhehoCinitele(Scitani):
    def __init__(self, nadpis=""):
        if nadpis == "":
            nadpis = "Doplň prvního činitele"
        super().__init__(nadpis)

    def tisk(self):
        print("%d + … = %d" % (self.a, self.c))


class ScitaniDoDesetiDoplnPrvnihoCinitele(ScitaniDoDeseti, ScitaniDoplnPrvnihoCinitele):
    def __init__(self):
        super(ScitaniDoDesetiDoplnPrvnihoCinitele, self).__init__("Sčítání do deseti, doplň prvního činitele")

    def tisk(self):
        ScitaniDoplnPrvnihoCinitele.tisk(self)


class ScitaniDoDesetiDoplnDruhehoCinitele(ScitaniDoDeseti, ScitaniDoplnDruhehoCinitele):
    def __init__(self):
        super(ScitaniDoDesetiDoplnDruhehoCinitele, self).__init__("Sčítání do deseti, doplň druhého činitele")

    def tisk(self):
        ScitaniDoplnDruhehoCinitele.tisk(self)


# p = ScitaniDo(20)
# p = ScitaniDoDeseti()
# p = ScitaniDoDesetiPresPet()
# p = ScitaniDoDesetiDoplnPrvnihoCinitele()
# p = ScitaniDoDesetiDoplnDruhehoCinitele()
# p.vyrob()
# p.tisk()


c = Cviceni(ScitaniDoDeseti, 20)
c.vyrob()
c.tisk()


class ScitaniDoDvaceti(ScitaniDo):
    def __init__(self, nadpis=""):
        super().__init__(20, nadpis)

    def over_vysledek(self):
        return super().over_vysledek() and 10 <= self.c


c = Cviceni(ScitaniDoDvaceti, 20)
c.vyrob()
c.tisk()


class ScitaniDoDvacetiDoplnPrvnihoCinitele(ScitaniDoDeseti, ScitaniDoplnPrvnihoCinitele):
    def __init__(self, nadpis=""):
        super(ScitaniDoDvacetiDoplnPrvnihoCinitele, self).__init__("Sčítání do 10, doplň prvního činitele")

    def tisk(self):
        ScitaniDoplnPrvnihoCinitele.tisk(self)


class ScitaniDoDvacetiDoplnDruhehoCinitele(ScitaniDoDeseti, ScitaniDoplnDruhehoCinitele):
    def __init__(self, nadpis=""):
        super(ScitaniDoDvacetiDoplnDruhehoCinitele, self).__init__("Sčítání do 10, doplň druhého činitele")

    def tisk(self):
        ScitaniDoplnDruhehoCinitele.tisk(self)


c = Cviceni(ScitaniDoDvacetiDoplnDruhehoCinitele, 20)
c.vyrob()
c.tisk()

c = Cviceni(ScitaniDoDvacetiDoplnPrvnihoCinitele, 20)
c.vyrob()
c.tisk()


# ====

class Odcitani(Priklad):
    """
A - B = C
    """

    def __init__(self, nadpis=""):
        if nadpis == "":
            nadpis = "Odčítání"
        super().__init__(nadpis)

    def spocitej(self):
        self.c = self.a - self.b

    def tisk(self):
        print("%d – %d = …" % (self.a, self.b))


class OdcitaniDo(Odcitani):
    def __init__(self, max, nadpis=""):
        if nadpis == "":
            nadpis = "Odčítání do %d" % (max)
        super().__init__(nadpis)
        self.max = max

    def vstup_nahodny(self):
        self.a = randint(0, self.max)
        self.b = randint(0, self.max)

    def over_vysledek(self):
        return 0 <= self.c <= self.max


class OdcitaniDoDeseti(OdcitaniDo):
    def __init__(self, nadpis=""):
        if nadpis == "":
            nadpis = "Odčítání do deseti"
        super().__init__(10, nadpis)


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


class OdcitaniDoplnPrvnihoCinitele(Odcitani):
    def __init__(self, nadpis=""):
        if nadpis == "":
            nadpis = "Doplň prvního činitele"
        super().__init__(nadpis)

    def tisk(self):
        print("… – %d = %d" % (self.b, self.c))


class OdcitaniDoplnDruhehoCinitele(Odcitani):
    def __init__(self, nadpis=""):
        if nadpis == "":
            nadpis = "Doplň druhého činitele"
        super().__init__(nadpis)

    def tisk(self):
        print("%d – … = %d" % (self.a, self.c))


class OdcitaniDoDesetiDoplnPrvnihoCinitele(OdcitaniDoDeseti, OdcitaniDoplnPrvnihoCinitele):
    def __init__(self):
        super(OdcitaniDoDesetiDoplnPrvnihoCinitele, self).__init__("Odčítání do deseti, doplň prvního činitele")

    def tisk(self):
        OdcitaniDoplnPrvnihoCinitele.tisk(self)


class OdcitaniDoDesetiDoplnDruhehoCinitele(OdcitaniDoDeseti, OdcitaniDoplnDruhehoCinitele):
    def __init__(self):
        super(OdcitaniDoDesetiDoplnDruhehoCinitele, self).__init__("Odčítání do deseti, doplň druhého činitele")

    def tisk(self):
        OdcitaniDoplnDruhehoCinitele.tisk(self)


# p = OdcitaniDo(20)
# p = OdcitaniDoDeseti()
# p = OdcitaniDoDesetiPresPet()
# p = OdcitaniDoDesetiDoplnPrvnihoCinitele()
# p = OdcitaniDoDesetiDoplnDruhehoCinitele()
# p.vyrob()
# p.tisk()


# c = Cviceni(OdcitaniDoDeseti, 20)
# c.vyrob()
# c.tisk()

c = OdcitaniDoDesetiDoplnPrvnihoCinitele()
c.vyrob()
c.tisk()

c = OdcitaniDoDesetiDoplnDruhehoCinitele()
c.vyrob()
c.tisk()


class OdcitaniDoDvaceti(OdcitaniDo):
    def __init__(self, nadpis=""):
        super().__init__(20, nadpis)

    def over_vysledek(self):
        return super().over_vysledek() and 5 <= self.c


c = Cviceni(OdcitaniDoDesetiOdectiMeneNezPet, 20)
c.vyrob()
c.tisk()

c = Cviceni(OdcitaniDoDesetiOdectiViceNezPet, 20)
c.vyrob()
c.tisk()

c = Cviceni(OdcitaniDoDvaceti, 20)
c.vyrob()
c.tisk()


class ScitaniDoDvacetiDoplnPrvnihoCinitele(ScitaniDoDvaceti, ScitaniDoplnPrvnihoCinitele):
    def __init__(self, nadpis=""):
        super(ScitaniDoDvacetiDoplnPrvnihoCinitele, self).__init__("Sčítání do 20, doplň prvního činitele")

    def tisk(self):
        OdcitaniDoplnPrvnihoCinitele.tisk(self)


class OdcitaniDoDvacetiDoplnDruhehoCinitele(ScitaniDoDvaceti, ScitaniDoplnDruhehoCinitele):
    def __init__(self, nadpis=""):
        super(ScitaniDoDvacetiDoplnDruhehoCinitele, self).__init__("Sčítání do 20, doplň druhého činitele")

    def tisk(self):
        OdcitaniDoplnDruhehoCinitele.tisk(self)


c = Cviceni(ScitaniDoDvacetiDoplnPrvnihoCinitele, 20)
c.vyrob()
c.tisk()

c = Cviceni(ScitaniDoDvacetiDoplnPrvnihoCinitele, 20)
c.vyrob()
c.tisk()


class OdcitaniDoDvacetiDoplnPrvnihoCinitele(OdcitaniDoDvaceti, OdcitaniDoplnPrvnihoCinitele):
    def __init__(self, nadpis=""):
        super(OdcitaniDoDvacetiDoplnPrvnihoCinitele, self).__init__("Odčítání do 20, doplň prvního činitele")

    def tisk(self):
        OdcitaniDoplnPrvnihoCinitele.tisk(self)


class OdcitaniDoDvacetiDoplnDruhehoCinitele(OdcitaniDoDvaceti, OdcitaniDoplnDruhehoCinitele):
    def __init__(self, nadpis=""):
        super(OdcitaniDoDvacetiDoplnDruhehoCinitele, self).__init__("Odčítání do 20, doplň druhého činitele")

    def tisk(self):
        OdcitaniDoplnDruhehoCinitele.tisk(self)


c = Cviceni(OdcitaniDoDvacetiDoplnDruhehoCinitele, 20)
c.vyrob()
c.tisk()

c = Cviceni(OdcitaniDoDvacetiDoplnPrvnihoCinitele, 20)
c.vyrob()
c.tisk()


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
