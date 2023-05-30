import csv
from pyaxols.atypes import Table
from pyaxols.atypes.seq import Seq


def write_csv(filepath: str, table: Table, encoding="utf-8") -> None:
    """Write a Table to a CSV file.

    Parameters
    ----------
    filepath : str
        The path to the file to write.
    table : Table
        The Table to write to the file.

    """
    with open(filepath, "w", encoding=encoding) as f:
        f.write(",".join(table.cols) + "\n")
        for i in range(table.shape[1]):
            f.write(",".join(str(v) for v in table.i(i)) + "\n")


def read_csv(filepath: str, encoding="utf-8") -> Table:
    """Read a CSV file into a Table.

    Args:
        filepath (str): The path to the file to read.

    Returns:
        Table: The Table read from the file.
    """
    dr = csv.DictReader(open(filepath, encoding=encoding))
    data = {
        k: Seq(
            name=k,
        )
        for k in dr.fieldnames
    }
    for row in dr:
        for k, v in row.items():
            if v == "":
                v = None
            data[k].append(v)
    for k in data:
        data[k]._Seq__dtype = str
    return Table(data)
