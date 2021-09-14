# Slicey

---

> :warning: there are bugs, if you find one please file an issue

#### Add Mutating Slices to Python

Mutating slices (or "reference slices") deal with a subset of a list as if it was its own list. This contrasts python's native "value slicing" where slicing a list provides a new list.

### Let's Take a Look

---

Starting with python's normal slicing

```python
base = [0, 1, 2, 3, 4]
slc = base[0:]  # take a slice of the whole list
# now let's check each element is the same in each list
assert all(base[i] == slc[i] for i in range(len(base)))
# if we change the slice (slc) the base won't change
slc[2] = -1
# now they should be different
assert base[2] != slc[2]
```

However, with slicey you can opt into slices that change the base.

```python
from slicey import Slice

base = [0, 1, 2, 3, 4]
slc = Slice(base)[0:] # slicey slicing syntax
assert all(base[i] == slc[i] for i in range(len(base)))
slc[2] = -1
assert base[2] == slc[2]
```

Excluding that slicey slices mutate the base list, they can be used like a normal slice!

```python
from slicey import Slice

base = [7, 3, 2, 5, 4]

slc = Slice(base)[1:-1]  # grab from 1 through 3 ([3, 2, 5])
assert [*slc] == [3, 2, 5]

slc[2] = 1
assert base[3] == 1

slc.sort()
assert base == [7, 1, 2, 3, 4]

```

### Why

---

Don't get me wrong, I love python! But sometimes... you just want a pointer.

The initial inspiration for this project was implementing merge sort, in a clear manner. Often merge sort is written with a variety of indices (i, j, k, etc); I can't speak for other but I can't make heads or tails of it. In languages that expose raw pointers, like c, one can mutate subsections of arrays by referencing an item and passing a smaller length to some function.
In short, I wanted to write a merge sort I sould read.

### Some Nitty Gritty

---

#### Slicing Slicey Slices ... ( ☉︵ ಠ )?

**slicey is always opt-in.** This means when you slice a slicey slice (an instance of Slice) you'll get an object of whatever slicing the base object would be.

In the likely case that was non-sense, let's just take a look

```python
from slicey import Slice

base = [*range(10)]  # a native list
slc = Slice(base)[1:10]  # a slicey slice
natv_sublc = slc[1:-1]  # a native list equal to base[2:9]
assert type(natv_sublc) == type(base)
assert natv_sublc == base[2:9]
```

Sometimes it make sense to have a refence slice of a reference slice.

```python
# continuing from above

slcy_subslc = slc.slice[1:-1]  # an instance of Slice
assert type(slcy_subslc) is Slice
assert [*slcy_subslc] == base[2:9]
# for the generic programmers among us Slices can be subsliced like a list
gnrl_slc = Slice(slc)[1:-1]
```

#### Transparent Slice Collapsing

Some steps have been taken to avoid indirection when sub-slicing instances of `Slice`. Taking a sub-slice of a `Slice` is always equivalent to take a slice out of the base object

#### readme todo

- changing base list size not permitted, b/c notifications
- excluding `.pop()` and other length mutating methods
- typing and `Sliceable`
