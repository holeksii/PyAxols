from typing import Sequence, Type

from pyaxols.utils import argsort
from .seq import Seq
from copy import copy
import matplotlib.pyplot as plt


class Table:
    """A table of data.
    This is a wrapper around a dictionary of Seqs, with some extra functionality.

    Attributes
    ----------
    cols : tuple[str]
        The columns of the table
    dtypes : tuple[Type]
        The data types of the columns
    data : dict[str, Seq]
        The data stored in the table

    Examples
    --------
    >>> from pyaxols.atypes import Table
    >>> t = Table.from_seqs([Seq([1, 2, 3], "a", int), Seq([4, 5, 6], "b", int)
    >>> t
    +---+---+
    | a | b |
    +---+---+
    | 1 | 4 |
    | 2 | 5 |
    | 3 | 6 |
    +---+---+

    >>> t.cols
    ('a', 'b')

    >>> t.dtypes
    (<class 'int'>, <class 'int'>)

    >>> t.data
    {'a': [1, 2, 3], 'b': [4, 5, 6]}
    """

    def __init__(
        self,
        data: dict[str, Seq] = None,
    ) -> None:
        """Initializes a Table.

        Parameters
        ----------
        data : dict[str, Seq]
            The data stored in the table

        Raises
        ------
        TypeError
            If data is not a dictionary of Seqs
        """
        if data is None:
            data = {}
        for k, v in data.items():
            if not isinstance(v, Seq):
                raise TypeError("data must be a sequence of Seq")
        self._data = data
        try:
            self._smooth()
        except Exception:
            pass

    def concat(self, other: "Table") -> "Table":
        """Concatenates two tables.

        Parameters
        ----------
        other : Table
            The table to concatenate with

        Returns
        -------
        Table
            The concatenated table

        Raises
        ------
        TypeError
            If other is not a Table
        """
        if not isinstance(other, Table):
            raise TypeError("other must be a Table")
        return Table({**self._data, **other._data})

    def union(self, other: "Table") -> "Table":
        """Returns the union of two tables without duplicates.

        Parameters
        ----------
        other : Table
            The table to union with

        Returns
        -------
        Table
            The union of the two tables

        Raises
        ------
        TypeError
            If other is not a Table
        ValueError
            If other does not have the same columns as self
        """
        if not isinstance(other, Table):
            raise TypeError("other must be a Table")
        if self._data.keys() != other._data.keys():
            raise ValueError("other must have the same keys as self")
        cpy = copy(self)
        for row in other:
            if not cpy.contains_row(row):
                cpy.append_row(row)
        return cpy

    def union_all(self, other: "Table") -> "Table":
        """Returns the union of two tables, including duplicates.

        Parameters
        ----------
        other : Table
            The table to union with

        Returns
        -------
        Table
            The union with duplicates of the two tables

        Raises
        ------
        TypeError
            If other is not a Table
        ValueError
            If other does not have the same columns as self
        """
        if not isinstance(other, Table):
            raise TypeError("other must be a Table")
        if self._data.keys() != other._data.keys():
            raise ValueError("other must have the same keys as self")
        return Table({k: self._data[k] + other._data[k] for k in self._data})

    def where(self, col: str, func: callable) -> "Table":
        if not callable(func):
            raise TypeError("func must be callable")
        empt = Table.empty(self.cols, self.dtypes)
        for i, row in enumerate(self[col]):
            if func(row):
                empt.append_row(self.i(i))
        return empt

    def intersect(self, other: "Table") -> "Table":
        """Returns the intersection of two tables.

        Parameters
        ----------
        other : Table
            The table to intersect with

        Returns
        -------
        Table
            The intersection of the two tables

        Raises
        ------
        TypeError
            If other is not a Table
        ValueError
            If other does not have the same columns as self
        """
        if self.cols != other.cols:
            raise ValueError("other must have the same columns as self")
        emt = Table.empty(self.cols, self.dtypes)
        for row in self:
            if other.contains_row(row):
                emt.append_row(row)
        return emt

    def row_count(self, row: Sequence) -> int:
        """Returns the number of times a row appears in the table.

        Parameters
        ----------
        row : Sequence
            The row to count

        Returns
        -------
        int
            The number of times the row appears

        Raises
        ------
        ValueError
            If row is not the same length as the columns
        """
        if len(row) != self.shape[0]:
            raise ValueError("row must be the same length as cols")
        t = tuple(row)
        res = 0
        for i in range(len(self)):
            if self.i(i) == t:
                res += 1
        return res

    def contains_row(self, row: Sequence) -> bool:
        """Returns whether or not the table contains a row.

        Parameters
        ----------
        row : Sequence
            The row to check

        Returns
        -------
        bool
            Whether or not the table contains the row

        Raises
        ------
        ValueError
            If row is not the same length as the columns
        """
        if len(row) != self.shape[0]:
            raise ValueError("row must be the same length as cols")
        for r in self:
            if r == tuple(row):
                return True
        return False

    def sorted(self, column: str, desc: bool = False) -> "Table":
        """Returns a sorted table.

        Parameters
        ----------
        column : str
            The column to sort by
        desc : bool, optional
            Whether or not to sort in descending order

        Returns
        -------
        Table
            The sorted table

        Raises
        ------
        TypeError
            If column is not a string
        ValueError
            If column is not a key in self
        """
        if not isinstance(column, str):
            raise TypeError("column must be a string")
        if column not in self._data.keys():
            raise ValueError("column must be a key in self")

        return Table.from_iterable(
            tuple(
                tuple(
                    s[i]
                    for i in argsort(
                        self[column].data, dtype=self[column].dtype, desc=desc
                    )
                )
                for s in self._data.values()
            ),
            self._data.keys(),
            tuple(seq.dtype for seq in self._data.values()),
        )

    def sorted_by_pattern(self, pattern: Sequence[int]) -> "Table":
        """Returns a sorted table by a pattern.

        Parameters
        ----------
        pattern : Sequence[int]
            The pattern to sort by

        Returns
        -------
        Table
            The sorted table

        Raises
        ------
        TypeError
            If pattern is not a Sequence
        ValueError
            If pattern is not the same length as the columns

        Example:
            >>> t = Table.from_seqs([Seq([1, 2, 3], "a", int), Seq([4, 5, 6], "b", int)
            >>> t.sorted_by_pattern([1, 2, 0])
            +---+---+
            | a | b |
            +---+---+
            | 3 | 6 |
            | 1 | 4 |
            | 2 | 5 |
            +---+---+
        """
        if len(pattern) != len(self):
            raise ValueError("pattern must be the same length as column")

        r = list(list(s[i] for i in argsort(pattern)) for s in self._data.values())
        return Table.from_iterable(r)

    def inner_join(self, on: str, other: "Table") -> "Table":
        if not isinstance(other, Table):
            raise TypeError("table must be a Table")
        if not self[on].dtype == other[on].dtype:
            raise ValueError("on must be the same type as self")

        if len(set(self.cols).intersection(set(other.cols))) != 1:
            raise ValueError("other must not contain any of the same columns as self")

        empt = Table.empty(other.cols, other.dtypes)
        for val in self[on]:
            index = -1
            try:
                index = other[on].find(val)
            except ValueError:
                index = -1
            if index == -1:
                empt.append_row([None] * self.shape[0])
            else:
                empt.append_row(other.i(index))
        for col in self.cols:
            if col in other.cols:
                empt.drop_col(col)
        return empt

    def left_join(self, on: str, other: "Table") -> "Table":
        """Returns a left join of two tables.

        Parameters
        ----------
        on : str
            The column to join on
        other : Table
            The table to join with

        Returns
        -------
        Table
            The left join of the two tables

        Raises
        ------
        TypeError
            If other is not a Table
        ValueError
            If other does not have the same columns as self
        """
        if not isinstance(other, Table):
            raise TypeError("table must be a Table")
        if not self[on].dtype == other[on].dtype:
            raise ValueError("on must be the same type as self")

        if len(set(self.cols).intersection(set(other.cols))) != 1:
            raise ValueError("other must not contain any of the same columns as self")

        empt = Table.empty(other.cols, other.dtypes)
        for val in self[on]:
            index = -1
            try:
                index = other[on].find(val)
            except ValueError:
                index = -1
            if index == -1:
                empt.append_row([None] * self.shape[0])
            else:
                empt.append_row(other.i(index))
        for col in self.cols:
            if col in other.cols:
                empt.drop_col(col)
        return self.concat(empt)

    def right_join(self, on: str, other: "Table") -> "Table":
        """Returns a right join of two tables. Alias for left_join."""
        return other.left_join(on, self)

    def group_by(self, col: str) -> list["Table"]:
        """Returns a list of tables grouped by a column."""
        res = []
        prev_val = None
        empt = Table.empty(self.cols, self.dtypes)
        sorted = self.sorted(col)
        for i, val in enumerate(sorted[col]):
            if val != prev_val:
                res.append(empt)
                empt = Table.empty(sorted.cols, sorted.dtypes)
            empt.append_row(sorted.i(i))
            prev_val = val
        return res

    def append_row(self, row: Sequence) -> "Table":
        """Appends a row to the table.  The row must be the same length as the table.

        Parameters
        ----------
        row : Sequence
            The row to append

        Returns
        -------
        Table
            self

        Raises
        ------
        TypeError
            If row is not a Sequence
        TypeError
            If row is not the same type as the table
        ValueError
            If row is not the same length as the table
        """
        if not isinstance(row, Sequence):
            raise TypeError("row must be a sequence")
        if len(row) != len(self._data.keys()):
            raise ValueError("row must be the same length as self")
        for i, v in enumerate(row):
            if (
                not isinstance(v, self._data[list(self._data.keys())[i]].dtype)
                and v is not None
            ):
                raise TypeError("row must be the same type as self")

        for i, k in enumerate(self._data.keys()):
            self._data[k].append(row[i])

        return self

    def drop_col(self, col: str) -> "Table":
        """Drops a column from the table.

        Parameters
        ----------
        col : str
            The column to drop

        Returns
        -------
        Table
            self
        """
        del self._data[col]
        return self

    def dropped_col(self, col: str) -> "Table":
        """Returns a copy of the table with a column dropped."""
        return copy(self).drop_col(col)

    def drop_row(self, index: int) -> "Table":
        """Drops a row from the table.

        Parameters
        ----------
        index : int
            The index of the row to drop

        Returns
        -------
        Table
            self

        Raises
        ------
        IndexError
            If index is out of bounds
        """
        for col in self.cols:
            del self._data[col][index]
        return self

    def dropped_row(self, index: int) -> "Table":
        """Returns a copy of the table with a row dropped."""
        return copy(self).drop_row(index)

    def drop_nones(self) -> "Table":
        """Drops all rows that contain None."""
        i = 0
        while i < self.shape[1]:
            if any(v is None for v in self.i(i)):
                self.drop_row(i)
            else:
                i += 1
        return self

    def dropped_nones(self) -> "Table":
        """Returns a copy of the table with all rows that contain None dropped."""
        return copy(self).drop_nones()

    def i(self, index: int) -> tuple:
        """Returns a row at an index."""
        return tuple(s[index] for s in self._data.values())

    def _smooth(self):
        max_len = max(len(s) for s in self._data.values())
        for k, v in self._data.items():
            self._data[k] = v.grow(max_len - len(v))

    @staticmethod
    def _create_cols(cols: set[str], data: Sequence[Sequence]) -> tuple[str]:
        if cols is None:
            if isinstance(data[0], Seq):
                cols = (s.name for s in data)
            else:
                cols = (f"unnamed_{i}" for i in range(len(data)))
        else:
            if len(cols) != len(data):
                raise ValueError("cols must be the same length as data")
            elif len(set(cols)) != len(data):
                raise ValueError("cols must be unique")
            elif not all(isinstance(n, str) for n in cols):
                raise TypeError("cols must be a sequence of strings")
        return tuple(cols)

    @staticmethod
    def empty(cols: Sequence[str] = [], dtypes: Sequence[Type] = []) -> "Table":
        """Creates an empty table.

        Parameters
        ----------
        cols : Sequence[str]
            The columns of the table
        dtypes : Sequence[Type]
            The data types of the columns

        Returns
        -------
        Table
            An empty table
        """
        return Table({c: Seq.empty(c, dtype=d) for c, d in zip(cols, dtypes)})

    @staticmethod
    def from_seqs(seqs: Sequence[Seq]) -> "Table":
        """Creates a table from a sequence of sequences.

        Parameters
        ----------
        seqs : Sequence[Seq]
            The sequences to create the table from

        Returns
        -------
        Table
            A table created from the sequence of sequences
        """
        if len(set(s.name for s in seqs)) != len(list(seqs)):
            raise ValueError("seqs must have unique col")
        return Table({s.name: s for s in seqs})

    @staticmethod
    def from_dict_of_iterable(
        d: dict[str, Sequence], dtypes: Sequence[Type] = None
    ) -> "Table":
        """Creates a table from a dictionary of iterables.

        Parameters
        ----------
        d : dict[str, Sequence]
            The dictionary of iterables to create the table from
        dtypes : Sequence[Type]
            The data types of the columns

        Returns
        -------
        Table
            A table created from the dictionary of iterables

        Raises
        ------
        ValueError
            If dtypes is not the same length as d
        TypeError
            If dtypes is not a sequence of types
        """
        if dtypes is None:
            dtypes = [object for _ in d]
        elif len(dtypes) != len(d):
            raise ValueError("dtypes must be the same length as d")
        for dtype in dtypes:
            if not isinstance(dtype, type) and dtype is not None:
                raise TypeError("dtypes must be a sequence of types")
        return Table(
            {
                col: Seq(data, col, dtype)
                for (col, data), dtype in zip(d.items(), dtypes)
            }
        )

    @staticmethod
    def from_iterable(
        data: Sequence, cols: tuple[str] = None, dtypes: Sequence[Type] = None
    ) -> "Table":
        """Creates a table from a sequence of sequences.

        Parameters
        ----------
        data : Sequence
            The sequences to create the table from
        cols : tuple[str]
            The columns of the table
        dtypes : Sequence[Type]
            The data types of the columns

        Returns
        -------
        Table
            A table created from the sequence of sequences
        """
        cols = Table._create_cols(cols, data)
        if dtypes is None:
            dtypes = [object for d in data]
        elif len(dtypes) != len(data):
            raise ValueError("dtypes must be the same length as data")
        for dtype in dtypes:
            if not isinstance(dtype, type) and dtype is not None:
                raise TypeError("dtypes must be a sequence of types")
        d = {col: Seq(d, col, dtype) for col, d, dtype in zip(cols, data, dtypes)}
        return Table(d)

    def head(self, n: int = 5) -> "Table":
        """Returns the first n rows of the table."""
        return Table({k: v.head(n) for k, v in self._data.items()})

    def tail(self, n: int = 5) -> "Table":
        """Returns the last n rows of the table."""
        return Table({k: v.tail(n) for k, v in self._data.items()})

    def plot(self, x: str, y: str, *args, **kargs) -> None:
        """Plots a column against another column.

        Parameters
        ----------
        x : str
            The column to plot on the x axis
        y : str
            The column to plot on the y axis
        """
        plt.plot(self[x], self[y], *args, **kargs)

    def scatter(self, x: str, y: str, *args, **kargs) -> None:
        """Scatters a column against another column.

        Parameters
        ----------
        x : str
            The column to plot on the x axis
        y : str
            The column to plot on the y axis
        """
        plt.scatter(self[x], self[y], *args, **kargs)

    @property
    def cols(self) -> tuple[str]:
        """Returns the columns of the table."""
        return tuple(self._data.keys())

    @property
    def dtypes(self) -> tuple[Sequence]:
        """Returns the dtypes of the table."""
        return tuple(s.dtype for s in self._data.values())

    @property
    def shape(self) -> tuple[int, int]:
        """Returns the shape of the table."""
        if len(self):
            return len(self), len(self[self.cols[0]])
        else:
            return 0, 0

    def __getitem__(self, key: str | Sequence[str]) -> "Seq | Table":
        if isinstance(key, str):
            return self._data[key]
        elif isinstance(key, Sequence):
            return Table({k: self._data[k] for k in key})
        else:
            raise TypeError("key must be a string or sequence of strings")

    def __setitem__(self, key: str, value: Seq) -> None:
        if not isinstance(key, str):
            raise TypeError("key must be a string")
        if not isinstance(value, Seq):
            raise TypeError("value must be a Seq")
        self._data[key] = value
        self._smooth()

    def __str__(self) -> str:
        from tabulate import tabulate

        return tabulate(self._data, headers="keys", tablefmt="psql", showindex=True)

    def __repr__(self) -> str:
        return self.__str__()

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self):
        self.it = 0
        return self

    def __next__(self):
        if self.it < len(self):
            self.it += 1
            return self.i(self.it - 1)
        else:
            raise StopIteration
