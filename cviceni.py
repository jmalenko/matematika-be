from random import randint
import functools

class Cviceni:
    def __init__(self, priklad, pocetPrikladu = 10):
        self.priklad = priklad
        self.pocetPrikladu = pocetPrikladu
        self.priklady = []

    def vyrob(self):
        for i in range(self.pocetPrikladu):
            priklad = self.priklad()
            priklad.vyrob()
            self.priklady.append(priklad)

    def tisk(self):
        print(self.priklady[0].nadpis)
        for priklad in self.priklady:
            priklad.tisk()

class Priklad:
    def __init__(self, nadpis):
        self.nadpis = nadpis

    def vyrob(self):
        while True:
            self.vstup_nahodny()
            self.spocitej()
            if self.over_vysledek():
                break

    def vstup_nahodny(self):
        pass

    def spocitej(self):
        pass

    def over_vysledek(self):
        pass

    def tisk(self):
        pass


class Scitani(Priklad):
    """
A + B = C
    """
    def __init__(self, nadpis = ""):
        if nadpis == "":
            nadpis = "Sčítání"
        super().__init__(nadpis)

    def spocitej(self):
        self.c = self.a + self.b

    def tisk(self):
        print("%d + %d = …" % (self.a, self.b))


class ScitaniDo(Scitani):
    def __init__(self, max, nadpis = ""):
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
    def __init__(self, nadpis = ""):
        if nadpis == "":
            nadpis = "Sčítání do deseti"
        super().__init__(10, nadpis)

class ScitaniDoDesetiPresPet(ScitaniDoDeseti):
    def __init__(self):
        super().__init__("Sčítání do deseti přes pět")

    def over_vysledek(self):
        return super().over_vysledek() and 6 <= self.c


class ScitaniDoplnPrvnihoCinitele(Scitani):
    def __init__(self, nadpis = ""):
        if nadpis == "":
            nadpis = "Doplň prvního činitele"
        super().__init__(nadpis)

    def tisk(self):
        print("… + %d = %d" % (self.a, self.c))

class ScitaniDoplnDruhehoCinitele(Scitani):
    def __init__(self, nadpis = ""):
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
    def __init__(self, nadpis = ""):
        super().__init__(20, nadpis)

    def over_vysledek(self):
        return super().over_vysledek() and 10 <= self.c

c = Cviceni(ScitaniDoDvaceti, 20)
c.vyrob()
c.tisk()

class ScitaniDoDvacetiDoplnPrvnihoCinitele(ScitaniDoDvaceti, ScitaniDoplnPrvnihoCinitele):
    def __init__(self, nadpis = ""):
        super(ScitaniDoDvacetiDoplnPrvnihoCinitele, self).__init__("Sčítání do 20, doplň prvního činitele")

    def tisk(self):
        ScitaniDoplnPrvnihoCinitele.tisk(self)

class ScitaniDoDvacetiDoplnDruhehoCinitele(ScitaniDoDvaceti, ScitaniDoplnDruhehoCinitele):
    def __init__(self, nadpis = ""):
        super(ScitaniDoDvacetiDoplnDruhehoCinitele, self).__init__("Sčítání do 20, doplň druhého činitele")

    def tisk(self):
        ScitaniDoplnDruhehoCinitele.tisk(self)


c = Cviceni(ScitaniDoDvacetiDoplnPrvnihoCinitele, 20)
c.vyrob()
c.tisk()

c = Cviceni(ScitaniDoDvacetiDoplnDruhehoCinitele, 20)
c.vyrob()
c.tisk()



# ====

class Odcitani(Priklad):
    """
A - B = C
    """
    def __init__(self, nadpis = ""):
        if nadpis == "":
            nadpis = "Odčítání"
        super().__init__(nadpis)

    def spocitej(self):
        self.c = self.a - self.b

    def tisk(self):
        print("%d – %d = …" % (self.a, self.b))


class OdcitaniDo(Odcitani):
    def __init__(self, max, nadpis = ""):
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
    def __init__(self, nadpis = ""):
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
    def __init__(self, nadpis = ""):
        if nadpis == "":
            nadpis = "Doplň prvního činitele"
        super().__init__(nadpis)

    def tisk(self):
        print("… – %d = %d" % (self.a, self.c))

class OdcitaniDoplnDruhehoCinitele(Odcitani):
    def __init__(self, nadpis = ""):
        if nadpis == "":
            nadpis = "Doplň prvního činitele"
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

class OdcitaniDoDvaceti(OdcitaniDo):
    def __init__(self, nadpis = ""):
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

class OdcitaniDoDvacetiDoplnPrvnihoCinitele(OdcitaniDoDvaceti, OdcitaniDoplnPrvnihoCinitele):
    def __init__(self, nadpis = ""):
        super(OdcitaniDoDvacetiDoplnPrvnihoCinitele, self).__init__("Odčítání do 20, doplň prvního činitele")

    def tisk(self):
        OdcitaniDoplnPrvnihoCinitele.tisk(self)

class OdcitaniDoDvacetiDoplnDruhehoCinitele(OdcitaniDoDvaceti, OdcitaniDoplnDruhehoCinitele):
    def __init__(self, nadpis = ""):
        super(OdcitaniDoDvacetiDoplnDruhehoCinitele, self).__init__("Odčítání do 20, doplň druhého činitele")

    def tisk(self):
        OdcitaniDoplnDruhehoCinitele.tisk(self)


class OdcitaniDoDvacetiDoplnPrvnihoCinitele(OdcitaniDoDvaceti, OdcitaniDoplnPrvnihoCinitele):
    def __init__(self, nadpis = ""):
        super(OdcitaniDoDvacetiDoplnPrvnihoCinitele, self).__init__("Odčítání do 20, doplň prvního činitele")

    def tisk(self):
        OdcitaniDoplnPrvnihoCinitele.tisk(self)

class OdcitaniDoDvacetiDoplnDruhehoCinitele(OdcitaniDoDvaceti, OdcitaniDoplnDruhehoCinitele):
    def __init__(self, nadpis = ""):
        super(OdcitaniDoDvacetiDoplnDruhehoCinitele, self).__init__("Odčítání do 20, doplň druhého činitele")

    def tisk(self):
        OdcitaniDoplnDruhehoCinitele.tisk(self)


c = Cviceni(OdcitaniDoDvacetiDoplnPrvnihoCinitele, 20)
c.vyrob()
c.tisk()

c = Cviceni(OdcitaniDoDvacetiDoplnDruhehoCinitele, 20)
c.vyrob()
c.tisk()

class Posloupnost(Priklad):
    """
A1 + A2 + ... + An = B
pro každé i: Ai < max
    """
    def __init__(self, nadpis = "", N = 3, max = 5, neznama = None):
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
                n = randint(1, self.max) # Zjednoduseni
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
                    print("…", end = "")
                else:
                    print(" + …", end = "")
            else:
                if i == 0:
                    print(n, end = "")
                else:
                    print(" + " if 0 <= n else " – ", end = "")
                    print(abs(n), end = "")
        print(" = ", end = "")
        if self.N == self.neznama:
            print("…", end = "")
        else:
            print(self.b, end = "")
        print("")

class PosloupnostTriScitance(Posloupnost):
    def __init__(self, nadpis = ""):
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
    def __init__(self, nadpis = ""):
        if nadpis == "":
            nadpis = "Čtyři sčítance"
        super().__init__(nadpis, N = 4)

    def vstup_nahodny(self):
        self.a = []
        for i in range(self.N):
            n = randint(1, self.max)
            self.a.append(n)

c = Cviceni(PosloupnostCtyriScitance, 20)
c.vyrob()
c.tisk()


class PosloupnostTriScitanceNeznama0(PosloupnostTriScitance):
    def __init__(self, nadpis = ""):
        super().__init__(nadpis)
        self.neznama = 0

c = Cviceni(PosloupnostTriScitanceNeznama0, 20)
c.vyrob()
c.tisk()


class PosloupnostTriScitanceNeznama1(PosloupnostTriScitance):
    def __init__(self, nadpis = ""):
        super().__init__(nadpis)
        self.neznama = 1

c = Cviceni(PosloupnostTriScitanceNeznama1, 20)
c.vyrob()
c.tisk()


class PosloupnostTriScitanceNeznama2(PosloupnostTriScitance):
    def __init__(self, nadpis = ""):
        super().__init__(nadpis)
        self.neznama = 2

c = Cviceni(PosloupnostTriScitanceNeznama2, 20)
c.vyrob()
c.tisk()


class PosloupnostTri(Posloupnost):
    def __init__(self, nadpis = ""):
        if nadpis == "":
            nadpis = "Tři čísla, ruzné operace"
        super().__init__(nadpis)

c = Cviceni(PosloupnostTri, 20)
c.vyrob()
c.tisk()


class ZapornaCislaOdcitani(Odcitani):
    def __init__(self, nadpis = ""):
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
    def __init__(self, nadpis = ""):
        super().__init__("Záporná čísla, přičti k zápornému")

    def vstup_nahodny(self):
        self.a = randint(-5, -1)
        self.b = randint(1, 9)

    def over_vysledek(self):
        return 0 < self.c

c = Cviceni(ZapornaCislaScitani, 20)
c.vyrob()
c.tisk()


