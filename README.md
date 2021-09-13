# slicey

---

#### Add mutating slices to python lists

Slicey adds mutating slices (or "reference slices") to python lists. This contrasts python's native "value slicing" where slicing a list provides a new list.

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

However, slicey you can opt into slices that change the base.

```python
from slicey import Slice

base = [0, 1, 2, 3, 4]
slc = Slice(base)[0:] # slicey slicing syntax
assert all(base[i] == slc[i] for i in range(len(base)))
slc[2] = -1
assert base[2] == slc[2]
```

Otherwise a slicey slice can be used like a normal slice!

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

### some nitty gritty

---

slicey is always opt-in. This means when you slice a slicey slice (an instance of Slice) you'll get whatever slicing the base object would be. In the likely case that was non-sense, let's just do it.

```python
from slicey import Slice

base = [*range(10)]  # a native list
slc = Slice(base)[1:10]  # a slicey slice
sub_slc = slc[1:-1]  # a native list equal to base[2:9]
assert type(sub_slc) == type(base)
assert sub_slc == base[2:9]
```

TODO: and `slc.slice[...] syntax, consider switching to .sub[...]`
