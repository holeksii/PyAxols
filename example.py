from pyaxols import aio
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


students = aio.csv.read_csv("students.csv")

print(students)

# first_name = Seq(["Artem", "Anna", "Sophie"], "FirstName", str)
# last_name = Seq(["Hrushevskii", "Shevchenko", "Melnyk"], "LastName", str)
# grades = Seq([4, 5, 4], "Grade", int)

# print(first_name)

# students = Table.from_seqs([first_name, last_name, grades])
# aio.csv.write_csv("students.csv", students)
# aio.xml.write_xml("students.xml", students)
# aio.json.write_json("students.json", students)


# aio.csv.write("fast_food.csv", fast_food)
# aio.xml.write("fast_food.xml", fast_food)
# aio.json.write("fast_food.json", fast_food)


# salads = Seq(["garden", "caesar", "greek", "cobb"], "salads", str)
# fruits = Seq(["apple", "banana", "orange", "grapes"], "fruits", str)
# healthy_food = Table.from_seqs([salads, fruits, prices])

# print(fast_food.inner_join("prices", healthy_food))
