import functools
from random import random, randint


def inicializace():
    import sys
    import random
    seed_value = randint(0, sys.maxsize)
    # seed_value = ...
    print("Random seed = %d" % (seed_value))
    random.seed(seed_value)


class SadaPrikladu:
    def __init__(self, zadani, pocet_prikladu=10):
        self.zadani = zadani
        self.pocet_prikladu = pocet_prikladu
        self.priklady = []

    def vyrob(self):
        dup_zbyva = 10000
        while len(self.priklady) < self.pocet_prikladu:
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
            except ArithmeticError:
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
        if do < 10:
            if od != 1:
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
        # 1) trivialni (tj. 0 nebo 1) nebo
        # 2) jednoduche (nedostatecne velka cisla)
        return self.trivialni(parametry) or self.jednoduche(parametry)

    def trivialni(self, parametry):
        # if self.do <= 10:
        #     return False
        if parametry.a in [0, 1]:
            return True
        if parametry.b in [0, 1]:
            return True
        if parametry.c in [0, 1]:
            return True
        return False

    def jednoduche(self, parametry):
        # if self.do <= 20:
        #     return False
        hranice = 0.6 * self.do
        if parametry.a < hranice and parametry.b < hranice and parametry.c < hranice:
            return True
        return False

    def tisk(self, parametry):
        s = ""
        s += format_cislo(parametry.a, self.typ is not Operand1)
        s += " "
        s += self.op_text
        s += " "
        s += format_cislo(parametry.b, self.typ is not Operand2)
        s += " = "
        s += format_cislo(parametry.c, self.typ is not Vysledek)
        print(s)

    def __eq__(self, item):
        if self.__class__ != item.__class__:
            return False
        return True


def format_cislo(n, to_fill=False):
    formatted = ""
    if to_fill:
        if n < 0:
            formatted += "–"
        formatted += str(abs(n))
    else:
        formatted += "…"
    return formatted


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


class ScitaniOdcitaniVse(ZadaniBinarni):
    def __init__(self, od, do):
        self.nadpis = "Sčítání a odčítání do %d" % do
        self.od = od
        self.do = do

    def vyrob_priklad(self):
        volba = randint(1, 6)
        match volba:
            case 1:
                zadani = lambda od=self.od, do=self.do: Scitani(od, do, Vysledek)
            case 2:
                zadani = lambda od=self.od, do=self.do: Scitani(od, do, Operand2)
            case 3:
                zadani = lambda od=self.od, do=self.do: Scitani(od, do, Operand1)
            case 4:
                zadani = lambda od=self.od, do=self.do: Odcitani(od, do, Vysledek)
            case 5:
                zadani = lambda od=self.od, do=self.do: Odcitani(od, do, Operand2)
            case 6:
                zadani = lambda od=self.od, do=self.do: Odcitani(od, do, Operand1)
            case _:
                raise ValueError('Unsupported branch ' + volba)
        return zadani().vyrob_priklad()


class ZadaniNasobeniDeleni(ZadaniBinarni):
    def __init__(self, n, typ):
        # Sestav nadpis
        nadpis = self.nadpis
        nadpis += ", číslo %d" % n
        if typ.nadpis != "":
            nadpis += ", %s" % typ.nadpis
        # super().__init__(nadpis)
        self.nadpis = nadpis

        self.n = n
        self.typ = typ

    def over_vysledek(self, parametry):
        return True

    def jednoduche(self, parametry):
        return False


class Nasobeni(ZadaniNasobeniDeleni):
    nadpis = "Násobení"
    op_text = "·"

    def spocitej(self, parametry):
        parametry.c = parametry.a * parametry.b

    def vstup_nahodny(self):
        parametry = ParametryBinarni()
        # if self.typ == Operand2:
        parametry.a = self.n
        parametry.b = randint(0, 10)
        # Swap
        if self.typ == Operand1 or (self.typ == Vysledek and randint(0, 1) == 0):
            parametry.a, parametry.b = parametry.b, parametry.a
        return parametry


class Deleni(ZadaniNasobeniDeleni):
    nadpis = "Dělení"
    op_text = ":"

    def spocitej(self, parametry):
        parametry.c = parametry.a / parametry.b

    def vstup_nahodny(self):
        parametry = ParametryBinarni()
        c = randint(0, 10)
        parametry.b = self.n
        parametry.a = parametry.b * c
        if self.typ == Operand2:
            parametry.b = c
        return parametry

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


class Clen:
    pass


class Operand1(Clen):
    nadpis = "doplň první operand"


class Operand2(Clen):
    nadpis = "doplň druhý operand"


class Vysledek(Clen):
    nadpis = ""


def vytvor2(operator, od, do, dopln=Vysledek, pocet=20):
    c = SadaPrikladu(operator(od, do, dopln), pocet)
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


class Posloupnost(Zadani):
    """
A0 + A1 + ... + An-1 = B
pro každé i: od <= Ai <= do
a od <= B <= do
    """

    def __init__(self, n, od, do, neznama=None):
        # Sestav nadpis
        nadpis = "Vice operací"
        nadpis += " délky %d" % n
        nadpis += ", čísla od %d do %d" % (od, do)
        if neznama is not None:
            nadpis += ", doplň %d. číslo" % (neznama + 1)
        super().__init__(nadpis)

        if neznama is None:
            neznama = n

        self.n = n
        self.od = od
        self.do = do
        self.neznama = neznama

    def vstup_nahodny(self):
        parmametry = ParametryPosl()
        parmametry.a = []
        for i in range(self.n):
            n = randint(self.od, self.do)
            if randint(0, 1) == 0:
                n = -n
            parmametry.a.append(n)
        return parmametry

    def spocitej(self, parametry):
        parametry.b = functools.reduce(lambda x, y: x + y, parametry.a)

    def over_vysledek(self, parametry):
        # Vysledek musi byt s povolenem rozssahu
        if not (self.od <= parametry.b <= self.do): return False
        # Prubezne vysledky musi byt kladne a v rozsahu
        sum = 0
        for a in parametry.a:
            sum += a
            if not (0 < sum): return False
            if not (self.od <= sum <= self.do): return False
        return True

    def tisk(self, parametry):
        s = ""
        for i in range(len(parametry.a)):
            n = parametry.a[i]
            if i == self.neznama:
                if i != 0:
                    s += " + " if 0 <= n else " – "
                s += format_cislo(n, i != self.neznama)
            else:
                if i == 0:
                    s += format_cislo(n, i != self.neznama)
                else:
                    s += " + " if 0 <= n else " – "
                    s += format_cislo(abs(n), i != self.neznama)
        s += " = "
        s += format_cislo(parametry.b, self.n != self.neznama)
        print(s)

    def __eq__(self, item):
        if self.__class__ != item.__class__:
            return False
        if self.n != item.n:
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


def vytvor_posl(n, od, do, neznama=None, pocet=20):
    c = SadaPrikladu(Posloupnost(n, od, do, neznama), pocet)
    c.vyrob()
    c.tisk()


class Tridy:
    def seznam(self):
        tridy = {
            1: "1. třída",
            2: "Sčítání a odčítání do 100", # TODO Pridat: aspon jedno cislo je "v poslednich 10"
            3: "Malá násobilka",
            4: "Sčítání a odčítání do 1000",
            5: "Velká násobilka (do 20)",
            # 6: "Násobení do 1000", # TODO Pridat podminku: vysledek je do 1000
        }
        return tridy


class Cviceni:
    def seznam_zadani(self, id_trida):
        match id_trida:
            case 1:
                zadani = self.zadani_1_trida()
            case 2:
                zadani = self.zadani_scitani_odcitani_do_100()
            case 3:
                zadani = self.zadani_mala_nasobilka()
            case 4:
                zadani = self.zadani_scitani_odcitani_do_1000()
            case 5:
                zadani = self.zadani_velka_nasobilka()
            # case 6:
            #     zadani = self.zadani_nasobeni_do_1000()
            case _:
                raise ValueError('Unsupported id_trida ' + id_trida)
        return zadani

    def zadani_1_trida(self):
        zadani = []

        for do in range(5, 20 + 1):
            od = 1 if do < 10 else 0

            # Trick, force the lambda parameters to instantiate
            zadani.append(lambda od=od, do=do: Scitani(od, do, Vysledek))
            zadani.append(lambda od=od, do=do: Scitani(od, do, Operand2))
            zadani.append(lambda od=od, do=do: Scitani(od, do, Operand1))

            zadani.append(lambda od=od, do=do: Odcitani(od, do, Vysledek))
            zadani.append(lambda od=od, do=do: Odcitani(od, do, Operand2))
            zadani.append(lambda od=od, do=do: Odcitani(od, do, Operand1))

            zadani.append(lambda od=od, do=do: ScitaniOdcitaniVse(od, do))

            # Nula
            if do == 9:
                od = 0
                zadani.append(lambda od=od, do=do: Scitani(od, do, Vysledek))
                zadani.append(lambda od=od, do=do: Scitani(od, do, Operand2))
                zadani.append(lambda od=od, do=do: Scitani(od, do, Operand1))

                zadani.append(lambda od=od, do=do: Odcitani(od, do, Vysledek))
                zadani.append(lambda od=od, do=do: Odcitani(od, do, Operand2))
                zadani.append(lambda od=od, do=do: Odcitani(od, do, Operand1))

        # Více operandů
        do = 20
        od = do // 3
        zadani.append(lambda od=od, do=do: Posloupnost(3, od, do, None))
        zadani.append(lambda od=od, do=do: Posloupnost(3, od, do, 2))
        zadani.append(lambda od=od, do=do: Posloupnost(3, od, do, 1))
        zadani.append(lambda od=od, do=do: Posloupnost(3, od, do, 0))

        zadani.append(lambda od=od, do=do: Posloupnost(4, od, do, None))
        zadani.append(lambda od=od, do=do: Posloupnost(4, od, do, 3))
        zadani.append(lambda od=od, do=do: Posloupnost(4, od, do, 2))
        zadani.append(lambda od=od, do=do: Posloupnost(4, od, do, 1))
        zadani.append(lambda od=od, do=do: Posloupnost(4, od, do, 0))

        return zadani

    def zadani_mala_nasobilka(self):
        zadani = []

        for n in range(2, 10 + 1):
            zadani.append(lambda n=n: Nasobeni(n, Vysledek))
            zadani.append(lambda n=n: Nasobeni(n, Operand2))
            zadani.append(lambda n=n: Nasobeni(n, Operand1))

            zadani.append(lambda n=n: Deleni(n, Vysledek))
            zadani.append(lambda n=n: Deleni(n, Operand2))
            zadani.append(lambda n=n: Deleni(n, Operand1))

        return zadani

    def zadani_velka_nasobilka(self):
        zadani = []

        for n in range(11, 20 + 1):
            zadani.append(lambda n=n: Nasobeni(n, Vysledek))
            zadani.append(lambda n=n: Nasobeni(n, Operand2))
            zadani.append(lambda n=n: Nasobeni(n, Operand1))

            zadani.append(lambda n=n: Deleni(n, Vysledek))
            zadani.append(lambda n=n: Deleni(n, Operand2))
            zadani.append(lambda n=n: Deleni(n, Operand1))

        return zadani

    def zadani_scitani_odcitani_do_100(self):
        zadani = []

        for do in range(30, 100 + 1, 10):
            zadani.append(lambda do=do: Scitani(0, do, Vysledek))
            zadani.append(lambda do=do: Scitani(0, do, Operand2))
            zadani.append(lambda do=do: Scitani(0, do, Operand1))

            zadani.append(lambda do=do: Odcitani(0, do, Vysledek))
            zadani.append(lambda do=do: Odcitani(0, do, Operand2))
            zadani.append(lambda do=do: Odcitani(0, do, Operand1))

            zadani.append(lambda do=do: ScitaniOdcitaniVse(0, do))

        return zadani

    def zadani_scitani_odcitani_do_1000(self):
        zadani = []

        for do in range(200, 1000 + 1, 100):
            zadani.append(lambda do=do: Scitani(0, do, Vysledek))
            zadani.append(lambda do=do: Scitani(0, do, Operand2))
            zadani.append(lambda do=do: Scitani(0, do, Operand1))

            zadani.append(lambda do=do: Odcitani(0, do, Vysledek))
            zadani.append(lambda do=do: Odcitani(0, do, Operand2))
            zadani.append(lambda do=do: Odcitani(0, do, Operand1))

            zadani.append(lambda do=do: ScitaniOdcitaniVse(0, do))

        return zadani

    # def zadani_nasobeni_do_1000(self):
    # zadani = []
    #
    # for n in range(200, 1000 + 1, 100):
    #     zadani.append(lambda n=n: Nasobeni(n, Vysledek))
    #     zadani.append(lambda n=n: Nasobeni(n, Operand2))
    #     zadani.append(lambda n=n: Nasobeni(n, Operand1))
    #
    #     zadani.append(lambda n=n: Deleni(n, Vysledek))
    #     zadani.append(lambda n=n: Deleni(n, Operand2))
    #     zadani.append(lambda n=n: Deleni(n, Operand1))
    #
    # return zadani

    def seznam(self, id_trida):
        zadani = self.seznam_zadani(id_trida)
        seznam = {}
        id = 1
        for zadani1 in zadani:
            seznam[id] = zadani1().nadpis
            id += 1
        return seznam

    def get_zadani(self, id_trida, id_cviceni):
        zadani_pro_tridu = self.seznam_zadani(id_trida)
        zadani1 = zadani_pro_tridu[id_cviceni - 1]
        zadani = zadani1()
        return zadani

    def get_priklad(self, id_trida, id_cviceni):
        zadani = self.get_zadani(id_trida, id_cviceni)
        priklad = zadani.vyrob_priklad()
        return priklad


if __name__ == "__main__":
    inicializace()
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

        # vytvor(Nasobeni, do)
        # vytvor(Nasobeni, do, Operand1)
        # vytvor(Nasobeni, do, Operand2)
        #
        # vytvor(Deleni, do)
        # vytvor(Deleni, do, Operand1)
        # vytvor(Deleni, do, Operand2)

    # Dlouha posloupnost

    vytvor_posl(3, 1, 5)
    vytvor_posl(3, 1, 5, 0)
    vytvor_posl(3, 1, 5, 1)
    vytvor_posl(3, 1, 5, 2)

    vytvor_posl(4, 1, 5)
    vytvor_posl(4, 1, 5, 0)
    vytvor_posl(4, 1, 5, 1)
    vytvor_posl(4, 1, 5, 2)
    vytvor_posl(4, 1, 5, 3)

    # Velka cisla
    do = 20
    od = do // 3
    vytvor_posl(2, od, do)
    vytvor_posl(2, od, do, 1)
    vytvor_posl(2, od, do, 0)

    vytvor_posl(3, od, do)
    vytvor_posl(3, od, do, 2)
    vytvor_posl(3, od, do, 1)
    vytvor_posl(3, od, do, 0)

    # Zaporna cisla

    vytvor_posl(3, -5, 5)
    vytvor_posl(3, -5, 5, 0)
    vytvor_posl(3, -5, 5, 1)
    vytvor_posl(3, -5, 5, 2)

    vytvor_posl(4, -5, 5)
    vytvor_posl(4, -5, 5, 0)
    vytvor_posl(4, -5, 5, 1)
    vytvor_posl(4, -5, 5, 2)
    vytvor_posl(4, -5, 5, 3)

    # Lekce
    tridy = Tridy().seznam()
    for id_trida, nazev_trida in tridy.items():
        # print("%d: %s" % (id_trida, nazev_trida))
        seznam = Cviceni().seznam(id_trida)
        for id_zadani, nazev_zadani in seznam.items():
            print("%s, cvičení %d: %s" % (nazev_trida, id_zadani, nazev_zadani))
            priklad = Cviceni().get_priklad(id_trida, id_zadani)
            priklad.tisk()
