base = [0, 1, 2, 3, 4]
slc = base[0:]  # take a slice of the whole list
# now let's check each element is the same in each list
assert all(base[i] == slc[i] for i in range(len(base)))
# if we change the slice (slc) the base won't change
slc[2] = -1
# now they should be different
assert base[2] != slc[2]
