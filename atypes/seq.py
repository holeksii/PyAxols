import json
from typing import Callable, Type, Sequence, AnyStr


class Seq:
    def __init__(
        self,
        data: Sequence["dtype"] = None,
        name: AnyStr = "unnamed",
        dtype: Type = object,
    ):
        if data is None:
            data = []
        self._dtype = dtype
        self._data = data
        self._name = name

    def append(self, value: "dtype") -> "Seq":
        self.__data.append(value)
        return self

    def head(self, n: int = 1) -> "Seq":
        return Seq(self.data[:n], self.name, self.dtype)

    def tail(self, n: int = 1) -> "Seq":
        return Seq(self.data[-n:], self.name, self.dtype)

    def rename(self, name: AnyStr) -> "Seq":
        self.name = name
        return self

    def find(self, value: "dtype") -> int:
        return self.data.index(value)

    def grow(self, n: int) -> "Seq":
        if n < 0:
            raise ValueError("n must be a positive integer")
        if n == 0:
            return self
        return self + ([None] * n)

    @property
    def reverse(self) -> "Seq":
        return Seq(self.data[::-1], self.name, self.dtype)

    def sorted(self, desc: bool = False) -> "Seq":
        return Seq(sorted(self.data, reverse=desc), self.name, self.dtype)

    def filter(self, f: Callable[["dtype"], bool]) -> "Seq":
        return Seq(tuple(filter(f, self.data)), self.name, self.dtype)

    def map(self, f: Callable[["dtype"], "dtype"]) -> "Seq":
        return Seq(tuple(map(f, self.data)), self.name, self.dtype)

    def as_type(self, dtype: Type) -> "Seq":
        return Seq(self.data, self.name, dtype)

    def as_pycollection(self, coltype: Type) -> Sequence:
        return coltype(self.data)

    def toJson(self) -> str:
        return json.dumps(self.data)

    @staticmethod
    def empty(name: AnyStr = "unnamed", dtype: Type = object) -> "Seq":
        return Seq([], name, dtype)

    @property
    def _str_percentage(self) -> float:
        return len(tuple(filter(lambda x: isinstance(x, str), self.data))) / len(
            self.data
        )

    @property
    def name(self) -> AnyStr:
        return self._Seq__name

    @name.setter
    def _name(self, name: AnyStr) -> None:
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        self.__name = name

    @property
    def dtype(self) -> Type:
        return self._Seq__dtype

    @dtype.setter
    def _dtype(self, dtype) -> None:
        if not isinstance(dtype, type):
            raise TypeError("dtype must be a type")
        self.__dtype = dtype

    @property
    def data(self) -> Sequence:
        return self._Seq__data

    @data.setter
    def _data(self, data) -> None:
        if not isinstance(data, Sequence):
            raise TypeError("data must be a sequence")
        if self.dtype is not object:
            data = list(map(self.dtype, data))
        self.__data = data

    def __str__(self) -> str:
        from tabulate import tabulate

        return tabulate(
            {self.name: self.data}, headers="keys", tablefmt="psql", showindex=True
        )

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, position: int) -> "dtype":
        return self.data[position]

    def __iter__(self):
        return iter(self.data)

    def __add__(self, other: "Seq") -> "Seq":
        if isinstance(other, self.dtype):
            return Seq([i + other for i in self.data], self.name, self.dtype)
        elif isinstance(other, Seq):
            return Seq(self.data + other.data, self.name, self.dtype)
        elif isinstance(other, Sequence):
            return Seq(self.data + other, self.name, self.dtype)
        raise TypeError("other must be a dtype, Seq, or Sequence")
