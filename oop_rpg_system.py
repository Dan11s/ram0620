from abc import ABC, abstractmethod
import random

#Abstraktne klass: defineerib üldise tegelase, kuid ei rakenda kõiki meetodeid
class Tegelane(ABC):
    def __init__(self, nimi, elud):
        self._nimi = nimi
        self._elud = elud

    @abstractmethod
    def runda(self, vastane):
        # Abstraktsioon: iga alamklass peab defineerima ründeviisi
        pass

    def vota_kahju(self, kahju):
        # Kapseldamine: elu vähenemine toimub läbi meetodi, mitte otseselt
        self._elud -= kahju
        if self._elud < 0:
            self._elud = 0

    def on_elus(self):
        return self._elud > 0

    def seisund(self):
        return f"{self._nimi}: {self._elud} elu"

# Pärilus: Sodalane on Tegelane
class Sodalane(Tegelane):

    def __init__(self, nimi):
        super().__init__(nimi, 100)

    # Polümorfism: runda käitub teistmoodi sõltuvalt tegelase tüübist
    def runda(self, vastane):
        kahju = random.randint(10, 20)
        vastane.vota_kahju(kahju)
        print(f"{self._nimi} ründab {vastane._nimi} ja teeb {kahju} kahju")

# Pärilus ja kapseldamine: maagil on lisaks eludele ka mana
class Maag(Tegelane):

    def __init__(self, nimi):
        super().__init__(nimi, 65)
        self._mana = 30

    def seisund(self):
        return f"{self._nimi}: {self._elud} elu ja {self._mana} manat"

    # Polümorfism: runda käitub teistmoodi sõltuvalt tegelase tüübist
    def runda(self, vastane):

        if self._mana >= 5:
            kahju = random.randint(5, 15)
            vastane.vota_kahju(kahju)
            print(f"{self._nimi} ründab {vastane._nimi} ja teeb {kahju} kahju")
            self._mana -= 5
            if self._mana < 0:
                self._mana = 0
        else:
            lisa_mana = random.randint(1, 8)
            self._mana += lisa_mana
            print(f"Maagil puudub mana. Kogub {lisa_mana} manat juurde.")

# Pärilus ja kapseldamine: vibukütil on nooled
class Vibukutt(Tegelane):

    def __init__(self, nimi):
        super().__init__(nimi, 80)
        self._nooled = 6

    def seisund(self):
        return f"{self._nimi}: {self._elud} elu ja {self._nooled} noolt"

    # Polümorfism: runda käitub teistmoodi sõltuvalt tegelase tüübist
    def runda(self, vastane):

        if self._nooled >= 1:
            kahju = random.randint(10, 25)
            vastane.vota_kahju(kahju)
            print(f"{self._nimi} ründab {vastane._nimi} ja teeb {kahju} kahju")
            self._nooled -= 1
            if self._nooled < 0:
                self._nooled = 0

        else:
            lisa_nooled = random.randint(1, 3)
            self._nooled += lisa_nooled
            print(f"Puuduvad nooled. Vibukütt leiab {lisa_nooled} noolt")

def lahing(t1, t2):

    # Polümorfism: runda meetod käitub erinevalt sõltuvalt tegelase tüübist
    print(f"Algab lahing: {t1._nimi} vs {t2._nimi}")
    print(f"{t1.seisund()} | {t2.seisund()}")

    kaik = 1

    while t1.on_elus() and t2.on_elus():

        print(f"\nKäik {kaik}")

        if kaik % 2 == 1:
            t1.runda(t2)
        else:
            t2.runda(t1)

        kaik += 1

        print(f"Seis: {t1.seisund()} | {t2.seisund()}")

    if t1.on_elus():
        print(f"\nVõitja on {t1._nimi}\n")
    else:
        print(f"\nVõitja on {t2._nimi}\n")

if __name__ == "__main__":
    sõdalane = Sodalane("Karl")
    maag = Maag("Liisa")
    vibukütt = Vibukutt("Mari")

    #lahing(sõdalane, maag)
    #lahing(vibukütt, sõdalane)
    lahing(maag, vibukütt)
