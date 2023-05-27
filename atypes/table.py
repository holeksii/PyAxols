from typing import Sequence, Type
from utils import argsort
from .seq import Seq
from copy import copy


class Table:
    def __init__(
        self,
        data: dict[str, Seq] = {},
    ) -> None:
        for k, v in data.items():
            if not isinstance(v, Seq):
                raise TypeError("data must be a sequence of Seq")
        self._data = data
        try:
            self._smooth()
        except Exception:
            pass

    def concat(self, other: "Table") -> "Table":
        if not isinstance(other, Table):
            raise TypeError("other must be a Table")
        return Table({**self._data, **other._data})

    def union_all(self, other: "Table") -> "Table":
        if not isinstance(other, Table):
            raise TypeError("other must be a Table")
        if self._data.keys() != other._data.keys():
            raise ValueError("other must have the same keys as self")
        return Table({k: self._data[k] + other._data[k] for k in self._data})

    def row_count(self, row: Sequence) -> int:
        if len(row) != self.shape[0]:
            raise ValueError("row must be the same length as cols")
        t = tuple(row)
        res = 0
        for i in range(len(self)):
            if self.i(i) == t:
                res += 1
        return res

    def contains_row(self, row: Sequence) -> bool:
        if len(row) != self.shape[0]:
            raise ValueError("row must be the same length as cols")
        return tuple(row) in self._data.values()

    def sorted(self, column: str, desc: bool = False) -> "Table":
        if not isinstance(column, str):
            raise TypeError("column must be a string")
        if column not in self._data.keys():
            raise ValueError("column must be a key in self")

        return Table.from_iterable(
            tuple(
                tuple(s[i] for i in argsort(self[column].data, desc=desc))
                for s in self._data.values()
            ),
            self._data.keys(),
            tuple(seq.dtype for seq in self._data.values()),
        )

    def sorted_by_pattern(self, pattern: Sequence[int]) -> "Table":
        if len(pattern) != len(self):
            raise ValueError("pattern must be the same length as column")

        r = list(list(s[i] for i in argsort(pattern)) for s in self._data.values())
        return Table.from_iterable(r)

    def left_join(self, on: str, other: "Table") -> "Table":
        if not isinstance(other, Table):
            raise TypeError("table must be a Table")
        if not self[on].dtype == other[on].dtype:
            raise ValueError("on must be the same type as self")

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
        return other.left_join(on, self)

    def append_row(self, row: Sequence) -> "Table":
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
        del self._data[col]
        return self

    def dropped_col(self, col: str) -> "Table":
        return copy(self).drop_col(col)

    def i(self, index: int) -> tuple:
        return tuple(s[index] for s in self._data.values())

    def _smooth(self):
        max_len = max(len(s) for s in self._data.values())
        for k, v in self._data.items():
            self._data[k] = v.grow(max_len - len(v))

    @staticmethod
    def _create_cols(cols: set[str], data: Sequence[Sequence]) -> set[str]:
        if cols == {}:
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
        return set(cols)

    @staticmethod
    def empty(cols: Sequence[str] = [], dtypes: Sequence[Type] = []) -> "Table":
        return Table({c: Seq.empty(c, dtype=d) for c, d in zip(cols, dtypes)})

    @staticmethod
    def from_seqs(seqs: Sequence[Seq]) -> "Table":
        if len(set(s.name for s in seqs)) != len(list(seqs)):
            raise ValueError("seqs must have unique col")
        return Table({s.name: s for s in seqs})

    @staticmethod
    def from_dict_of_iterable(
        d: dict[str, Sequence], dtypes: Sequence[Type] = None
    ) -> "Table":
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
        data: Sequence, cols: set[str] = {}, dtypes: Sequence[Type] = None
    ) -> "Table":
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
        return Table({k: v.head(n) for k, v in self._data.items()})

    def tail(self, n: int = 5) -> "Table":
        return Table({k: v.tail(n) for k, v in self._data.items()})

    @property
    def cols(self) -> tuple[str]:
        return tuple(self._data.keys())

    @property
    def dtypes(self) -> tuple[Sequence]:
        return tuple(s.dtype for s in self._data.values())

    @property
    def shape(self) -> tuple[int, int]:
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

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> "Table":
        return iter(self._data)
