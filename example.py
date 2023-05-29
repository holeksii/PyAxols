from pyaxols.atypes import Table, Seq


drinks = Seq(["coke", "pepsi", "fanta", "sprite"], "drinks", str)
burgers = Seq(["big mac", "whopper", "quarter pounder", "mcchicken"], "burgers", str)
fries = Seq(["small", "medium", "large", "super size"], "fries", str)
prices = Seq(
    [2.99, 1.99, 4.99, 3.99, 8],
    "prices",
    float,
)

fast_food = Table.from_seqs([drinks, burgers, fries, prices])
fast_food = fast_food.union_all(fast_food)
# print(fast_food.sorted("drinks"))

for i in fast_food.group_by("drinks"):
    print(i)

# aio.csv.write("fast_food.csv", fast_food)
# aio.xml.write("fast_food.xml", fast_food)
# aio.json.write("fast_food.json", fast_food)


# salads = Seq(["garden", "caesar", "greek", "cobb"], "salads", str)
# fruits = Seq(["apple", "banana", "orange", "grapes"], "fruits", str)
# healthy_food = Table.from_seqs([salads, fruits, prices])

# print(fast_food.inner_join("prices", healthy_food))
