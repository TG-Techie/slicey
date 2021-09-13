from slicey import Slice

base = [0, 1, 2, 3, 4]
slc = Slice(base)[0:]
assert all(base[i] == slc[i] for i in range(len(base)))
slc[2] = -1
assert base[2] == slc[2]
