from slicey import Slice

base = [*range(10)]  # a native list
slc = Slice(base)[1:10]  # a slicey slice
print(slc)
sub_slc = slc[1:-1]  # a native list equal to base[2:9]
print(sub_slc)
assert type(sub_slc) == type(base)
assert sub_slc == base[2:9]
