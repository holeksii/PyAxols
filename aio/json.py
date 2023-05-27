import json
from atypes.table import Table


def write(filepath: str, data: Table) -> None:
    """Write a Table to a JSON file.

    Args:
        filepath (str): The path to the file to write to.
        data (Table): The Table to write.
    """
    lst = [
        {col: val for col, val in zip(data.cols, data.i(ind))}
        for ind in range(data.shape[1])
    ]
    with open(filepath, "w") as f:
        json.dump(lst, f, indent=4)


def read(filepath: str) -> Table:
    """Read a JSON file into a Table.

    Args:
        filepath (str): The path to the file to read.

    Returns:
        Table: The Table read from the file.
    """
    with open(filepath, "r") as f:
        lst = json.load(f)

    empt = Table.empty(
        cols=lst[0].keys(),
        dtypes=tuple(type(t) for t in lst[0].values()),
    )

    for d in lst:
        empt.append_row(list(d.values()))

    return empt
