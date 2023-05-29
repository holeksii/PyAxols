from typing import Callable, Type, Sequence
import matplotlib.pyplot as plt


class Seq:
    """
    A sequence of data. This is a wrapper around a list, with some extra functionality.

    Attributes:
        data (Sequence[dtype]):
            The data stored in the sequence
        name (str):
            The name of the sequence
        dtype (Type):
            The type of the data

    Examples:
        >>> from pyaxols.atypes import Seq
        >>> s = Seq([1, 2, 3], "my sequence", int)
        >>> s
        +-------------+
        | my sequence |
        +-------------+
        |           1 |
        |           2 |
        |           3 |
        +-------------+
        >>> s.name
        'my sequence'
        >>> s.dtype
        <class 'int'>
        >>> s.data
        [1, 2, 3]
        >>> s.append(4)
        >>> s
        +------------+
        | my sequence |
        +-------------+
        |           1 |
        |           2 |
        |           3 |
        |           4 |
        +-------------+
        >>> s.head()
        +-------------+
        | my sequence |
        +-------------+
        |           1 |
        +-------------+
        >>> s.tail()
        +-------------+
        | my sequence |
        +-------------+
        |           4 |
        +-------------+
    """

    def __init__(
        self,
        data: Sequence["dtype"] = None,
        name: str = "unnamed",
        dtype: Type = object,
    ):
        """Initializes a Seq.

        Parameters:
            data (Sequence[dtype], optional):
                The data to store in the sequence, by default None
            name (str, optional):
                The name of the sequence, by default "unnamed"
            dtype (Type, optional):
                The type of the data, by default object

        Raises:
            TypeError:
                Raised if data is not a sequence
                Raised if dtype is not a type
        """
        if data is None:
            data = []
        self._dtype = dtype
        self._data = data
        self._name = name

    def append(self, value: "dtype") -> "Seq":
        """Append a value to the sequence.

        Args:
            value (dtype): The value to append

        Returns:
            Seq: self
        """
        self.__data.append(value)
        return self

    def head(self, n: int = 1) -> "Seq":
        """Get the first n elements of the sequence.

        Args:
            n (int, optional): The number of elements to get. Defaults to 1.

        Returns:
            Seq: A new sequence containing the first n elements
        """
        return Seq(self.data[:n], self.name, self.dtype)

    def tail(self, n: int = 1) -> "Seq":
        """Get the last n elements of the sequence

        Args:
            n (int, optional): The number of elements to get. Defaults to 1.

        Returns:
            Seq: A new sequence containing the last n elements
        """
        return Seq(self.data[-n:], self.name, self.dtype)

    def rename(self, name: str) -> "Seq":
        """Rename the sequence.

        Args:
            name (str): The new name

        Returns:
            Seq: self
        """
        self.name = name
        return self

    def find(self, value: "dtype") -> int:
        """Find the index of a value in the sequence.

        Args:
            value (dtype): The value to find

        Returns:
            int: The index of the value
        """
        return self.data.index(value)

    def grow(self, n: int) -> "Seq":
        """Grow the sequence by n elements.

        Args:
            n (int): The number of elements to grow by

        Returns:
            Seq: self
        """
        if n < 0:
            raise ValueError("n must be a positive integer")
        if n == 0:
            return self
        return self + ([None] * n)

    def reverse(self) -> "Seq":
        """Reverse the sequence.

        Returns:
            Seq: A new sequence with the elements in reverse order
        """
        return Seq(self.data[::-1], self.name, self.dtype)

    def sorted(self, desc: bool = False) -> "Seq":
        """Sort the sequence.

        Args:
            desc (bool, optional): Whether to sort in descending order.
            Defaults to False.

        Returns:
            Seq: A new sequence with the sorted elements
        """
        return Seq(sorted(self.data, reverse=desc), self.name, self.dtype)

    def filter(self, f: Callable[["dtype"], bool]) -> "Seq":
        """Filter the sequence.

        Args:
            f (Callable[[dtype], bool]): The filter function

        Returns:
            Seq: A new sequence with the filtered elements
        """
        return Seq(list(filter(f, self.data)), self.name, self.dtype)

    def map(self, f: Callable[["dtype"], "dtype"]) -> "Seq":
        """Map a function over the sequence.

        Args:
            f (Callable[[dtype], dtype]): The function to map

        Returns:
            Seq: A new sequence with the mapped elements
        """
        return Seq(list(map(f, self.data)), self.name, self.dtype)

    def as_type(self, dtype: Type) -> "Seq":
        """Cast the sequence to a new type.

        Args:
            dtype (Type): The new type

        Returns:
            Seq: A new sequence with the elements casted to the new type
        """
        return Seq(self.data, self.name, dtype)

    def as_pycollection(self, coltype: Type) -> Sequence:
        """Convert the sequence to a python collection.

        Args:
            coltype (Type): The type of collection to convert to

        Returns:
            Sequence: The converted collection
        """
        return coltype(self.data)

    def hist(self, bins: int = 10, *args, **kwargs) -> None:
        """Plot a histogram of the sequence.

        Args:
            bins (int, optional): The number of bins. Defaults to 10.
        """
        plt.hist(self.data, bins, *args, **kwargs)

    def pie(self, labels=None, *args, **kwargs) -> None:
        """Plot a pie chart of the sequence.

        Args:
            labels (None, optional): The labels to use. Defaults to None.
        """
        if labels is False:
            labels = None
        elif labels is None:
            labels = self.data
        plt.pie(
            self.data,
            labels=labels,
            *args,
            **kwargs,
        )

    @staticmethod
    def empty(name: str = "unnamed", dtype: Type = object) -> "Seq":
        """Static method to create an empty sequence.

        Args:
            name (str, optional): The name of the sequence. Defaults to "unnamed".
            dtype (Type, optional): The type of the sequence. Defaults to object.

        Returns:
            Seq: The empty sequence
        """
        return Seq(name=name, dtype=dtype)

    @property
    def _str_percentage(self) -> float:
        """The percentage of elements in the sequence that are strings.

        Returns:
            float: The percentage of elements in the sequence that are strings
        """
        return len(tuple(filter(lambda x: isinstance(x, str), self.data))) / len(
            self.data
        )

    @property
    def name(self) -> str:
        return self._Seq__name

    @name.setter
    def _name(self, name: str) -> None:
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
            # cast to dtype but keep nones
            data = [self.dtype(i) if i is not None else None for i in data]
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

    # del
    def __delitem__(self, position: int) -> None:
        del self.data[position]
