class Property:
    def __init__(self, area, rooms:int, price, address):
        self.area, self.rooms, self.price, self.address = area,rooms, price, address
        self._name = "Posiadłość"

    def __str__(self):
        return (f"{self._name}: rozmiar: {self.area} m2, ilość pokoi: {self.rooms}, "
                f"cena: {self.price} PLN, adres: '{self.address}'")

class House(Property):
    def __init__(self, area, rooms:int, price, address, plot):
        super().__init__(area,rooms, price, address)
        self.plot = plot
        self._name = "Dom"

    def __str__(self):
        return (f"{super().__str__()}, "
                f"rozmiar działki: {self.plot} m2")

class Flat(Property):
    def __init__(self, area, rooms:int, price, address, floor:int):
        super().__init__(area,rooms, price, address)
        self.floor=floor
        self._name = "Mieszkanie"

    def __str__(self):
        return (f"{super().__str__()}, "
                f"ilość pięter: {self.floor}")
    

p = Property(120, 4, 550000, "Warszawa, Kwiatowa 12")
h = House(180, 5, 850000, "Kraków, Długa 4", 600)
f = Flat(60, 2, 350000, "Poznań, Zielona 7", 3)

print(p)
print(h)
print(f)