class City:
    def __init__(self, name: str, population: int):
        self.name = name
        self.location = name
        self.population = population


text: str = "Hello, World!"
pert: int = 90
temp: float = 36.6
is_active: bool = True
names: list[str] = ["Alice", "Bob", "Charlie"]
ages: dict[str, int] = {"Alice": 30, "Bob": 25, "Charlie": 35}
value = "string"
number: int | float = 11.5
optional: str | None = None
digits: list[int] = [1, 2, 3, 4, 5]
table_5: tuple[int, ...] = (1, 2, 3, 4, 5)

city_temp: tuple[City, float] = (City("Gdansk", 500000), 20.5)

for x in city_temp:
    if isinstance(x, City):
        print(f"City: {x.name}, Population: {x.population}")
    else:
        print(x)

shipment = {
    "id": 123,
    "weight": 25.5,
    "content": "wooden table",
    "status": "In transit",
}


for key, value in shipment.items():
    print(f"{key}: {value}")

for key in shipment.keys():
    print(key)

for value in shipment.values():
    print(value)


def root(num: int | float, exp: float | None = 0.5) -> float:
    return pow(num, 0.5 if exp is None else exp)


root_25 = root(2, None)
print(root_25)

print(shipment["content"])
