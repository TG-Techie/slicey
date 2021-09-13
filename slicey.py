# The MIT License (MIT)

# Copyright (c) 2021 Jonah Yolles-Murphy (TG-Techie)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import builtins
from typing import *

__version__ = "0.1.0"

T = TypeVar("T")

Sliceable = Union["Slice[T]", MutableSequence[T]]


class _SliceConstructor(Generic[T]):
    """
    An intermediate constructor that holds the sequence to be sliced and allows for
    a more flexible `.slice(...)` or `.slice[...]` syntax.
    """

    __slots__ = {"_seq"}

    def __init__(self, seq: Sliceable) -> None:
        self._seq = seq

    def __getitem__(self, s: Union[int, builtins.slice]) -> "Slice[T]":
        # allow single item slicing with Slice(...)[n] syntax
        if isinstance(s, int) or hasattr(s, "__index__"):
            index = s.__index__()
            s = builtins.slice(index, index + 1)

        assert (
            s.step is None
        ), f"slicing cannot be non-contiguous (got `{s.step!r}` for step)"
        seq = self._seq
        start = s.start
        stop = s.stop

        if start is None:
            start = 0

        while start < 0:
            start += len(seq)

        if stop is None:
            stop = len(seq)

        while stop < 0:
            stop += len(seq)

        return self(
            start=start,
            length=stop - start,
        )

    def __call__(self, *, length, start) -> "Slice[T]":
        return Slice(self._seq, start=start, length=length)


class Slice(Generic[T]):
    """
    A more tradition slice of sequences where the created slice mutates the sliced object.
    When using a Slice to mutate the base Sequence the Slice assumes the base will not change size
    ex:
    ```
    ls = [0, 3, -1, 1, 4]
    slc = Slice(ls)[1:4]
    slc[0] = 1
    slc[2] = 3
    assert ls == [0, 1, -1, 3, 4]
    ```
    By default, slicing Slice object will return whatever slicing the base object would normally be.
    ```
    assert type(slc[0:1]) == list # evaluates as True
    ```
    If you want a "sub slice" use .slice to make a further slice
    ```
    sub = slc.slice[1:2]
    sub[0] = 2
    assert ls == [0, 1, 2, 3, 4]
    ```
    """

    Self = Union["Slice"]

    _seq: Sliceable
    _start: int
    _length: int
    _constructor: Optional[_SliceConstructor[T]]

    __slots__ = {"_seq", "_start", "_length", "_constructor"}

    def __new__(
        cls: Type[Self],
        seq: Sliceable,
        start=None,
        length=None,
    ):
        if start is not None and length is not None:
            return super(Slice, cls).__new__(cls)  # type: ignore
        elif start is None and length is None:
            return _SliceConstructor(seq)
        else:
            raise ValueError(
                f"{cls.__name__} cannot be called with only one of start= and length=, "
                f"got only {'start=' if start is not None else 'length='}"
            )

    def __init__(
        self,
        seq: Sliceable,
        *,
        start=None,  # type: ignore
        length=None,  # type: ignore
    ) -> None:

        # sanitize the inputs, as they must be integers
        start = start.__index__()
        length = length.__index__()

        # verify that the given start and length are in bounds
        if not length >= 1:
            raise ValueError(
                f"Slices cannot be created with lengths less than 1, got {length}"
            )

        if not (0 <= start < len(seq)):
            raise ValueError(f"start index out of bounds, got {start}")

        if not ((start + length) <= len(seq)):
            raise ValueError(
                f"slice out of bounds. starting at {start}, a slice of length {length} extends"
                f" past the end of the sliced sequence "
            )

        # if this is slicing a slice, instead driectly slice the original object
        if isinstance(seq, Slice):
            self._seq = seq._seq
            start += seq._start
        else:
            self._seq = seq

        self._start = start
        self._length = length

        # sanitization
        assert hasattr(start, "__index__"), (
            "start must be an integer, " + f"got {start!r}"
        )
        assert hasattr(length, "__index__"), (
            "length must be an integer, " + f"got {length!r}"
        )

        # this will be lazily evaluated later
        self._constructor = None

    @property
    def slice(self) -> _SliceConstructor[T]:
        # lazily create a constructor for sub slices of this slice
        constructor = self._constructor
        if constructor is None:
            self._constructor = constructor = _SliceConstructor(self)
        return constructor

    def _isinited(self) -> bool:
        return hasattr(self, "_start") and hasattr(self, "_length")

    def __getitem__(self, index: Union[int, builtins.slice]):
        if isinstance(index, int) or hasattr(index, "__index__"):
            return self._get_item(index.__index__())  # type: ignore
            # idk to test for SupportsIndex in 3.6 yet
        elif isinstance(index, slice):
            return self._get_slice(index)
        else:
            raise TypeError(
                f"{type(self).__name__} indices must be integers or slices, "
                f"not {type(index).__name__}"
            )

    def __setitem__(self, index: Union[int, builtins.slice], value: T) -> None:
        # check for slice assignment as it is not yet supported
        if isinstance(index, builtins.slice):
            offset = self._start
            self._seq.__setitem__(
                builtins.slice(
                    index.start + offset,
                    index.stop + offset,
                    index.step,
                ),
                value,
            )
            return
        elif isinstance(index, int) or hasattr(index, "__index__"):
            index = self._bounds_check_and_mod(index)

            self._seq[self._start + index] = value
        else:
            raise NotImplementedError()

    def _get_slice(self, s: builtins.slice) -> MutableSequence[T]:

        offset = self._bounds_check_and_mod(self._start)
        stop = s.stop % self._length
        return self._seq[s.start + offset : stop + offset : s.step]

    def _get_item(self, index: int) -> T:
        # check that the index is in range assuming the base sequence has not changed
        index = self._bounds_check_and_mod(index)
        return self._seq[self._start + index]

    def __len__(self) -> int:
        assert self._isinited()
        return self._length

    def __iter__(self) -> Generator[T, None, None]:
        seq = self._seq
        for index in range(self._start, self._start + self._length):
            yield seq[index]
        else:
            return None

    def __repr__(self) -> str:
        return f"${self._seq[self._start : self._start+self._length]}"

    def _bounds_check_and_mod(self, index: int) -> int:
        if index >= self._length:
            raise IndexError(
                f"Slice index out of range, got [{index}] in slice of length {self._length}"
            )
        elif index < 0:
            index %= self._length
        else:
            pass

        return index

    def sort(self, **kwargs) -> None:
        for index, value in enumerate(sorted(self, **kwargs)):
            self[index] = value


if __name__ == "__main__":
    # test basic sicing
    ls = [0, 3, -1, 1, 4]
    slc = Slice(ls)[1:4]
    slc[0] = 1
    slc[2] = 3
    assert ls == [0, 1, -1, 3, 4]

    # test sub-slicing
    sub = slc.slice[1:2]
    sub[0] = 2
    assert ls == [0, 1, 2, 3, 4]

    # test slicing types
    ls = [*range(8)]
    # test default start and stop
    slc = Slice(ls)[:]
    assert [*slc] == ls
    # test negative end
    slc = Slice(ls)[0:-1]
    assert [*slc] == ls[0:-1]
    # test negative start
    slc = Slice(ls)[-8:]
    assert [*slc] == ls[-8:]

    # test slice sorting
    ls = [0, 4, 3, 2, 1, 5]
    slc = Slice(ls)[1:-1]
    assert [*slc] == [4, 3, 2, 1]
    slc.sort()
    assert ls == [0, 1, 2, 3, 4, 5]
