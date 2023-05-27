import csv
from atypes import Table
from atypes.seq import Seq


def read(filepath: str) -> Table:
    dr = csv.DictReader(open(filepath))
    data = {
        k: Seq(
            name=k,
        )
        for k in dr.fieldnames
    }
    for row in dr:
        for k, v in row.items():
            data[k].append(v)
    for k in data:
        data[k]._Seq__dtype = str
    return Table(data)


def write(filepath: str, table: Table) -> None:
    with open(filepath, "w") as f:
        f.write(",".join(table.cols) + "\n")
        for i in range(table.shape[1]):
            f.write(",".join(str(v) for v in table.i(i)) + "\n")
