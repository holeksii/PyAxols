import csv

from table import Table


def read(filepath: str) -> Table:
    with open(filepath, "r") as f:
        reader = csv.reader(f)
        data = list(reader)
        return Table.from_iterable(data)


if __name__ == "__main__":
    print(read("C:\\Users\\Oleksii\\Desktop\\coursework\\PyAxols\\happydata.csv"))
