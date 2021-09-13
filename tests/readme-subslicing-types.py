from slicey import Slice

base = [*range(10)]  # a native list
slc = Slice(base)[1:10]  # a slicey slice
natv_sublc = slc[1:-1]  # a native list equal to base[2:9]
assert type(natv_sublc) == type(base)
assert natv_sublc == base[2:9]

# ... break for commentary

slcy_subslc = slc.slice[1:-1]  # an instance of Slice
assert type(slcy_subslc) is Slice
assert [*slcy_subslc] == base[2:9]
# for the generic programmers among us Slices can be subsliced like a list
gnrl_slc = Slice(slc)[1:-1]
