import utils
from seq import Seq
from table import Table
from time import time


# n = 1_000_000
# r = range(4, n)

drinks = Seq(["coke", "pepsi", "fanta", "sprite"], "drinks", str)
burgers = Seq(["big mac", "whopper", "quarter pounder", "mcchicken"], "burgers", str)
fries = Seq(["small", "medium", "large", "super size"], "fries", str)
prices = Seq(
    [2.99, 1.99, 4.99, 3.99],
    "prices",
    float,
)
fast_food = Table.from_seqs([drinks, burgers, fries, prices])


salads = Seq(["garden", "caesar", "greek", "cobb"], "salads", str)
fruits = Seq(["apple", "banana", "orange", "grapes"], "fruits", str)
prices1 = Seq(
    [2.99, 1.99, 4.99, 3],
    "prices",
    float,
)
healthy_food = Table.from_seqs([drinks.reverse, salads, fruits, prices1])

print(fast_food.right_join("prices", healthy_food))
