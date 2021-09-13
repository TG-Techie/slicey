from slicey import Slice

base = [7, 3, 2, 5, 4]

slc = Slice(base)[1:-1]  # grab from 1 through 3 ([3, 2, 5])
assert [*slc] == [3, 2, 5]

slc[2] = 1
assert base[3] == 1

slc.sort()
assert base == [7, 1, 2, 3, 4]
