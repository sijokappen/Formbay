

## Functional Arrays
import numpy as np

def create_array_from_function(f, d, dtype=None):
    a = np.array([f(i, j) for i in range(d[0]) for j in range(d[1])], dtype)
    return a.reshape(d)

print(create_array_from_function(lambda i,j: (i - j)**2, [4, 4]))





## Removing Boundaries
def boundary_cropping(a, m):
	return a[np.ix_(*map(lambda e: range(e.min(), e.max() + 1),np.where(m)))]

a1 = np.array([[0,0,0,0,0], [0,0,0,0,0], [0,1,0,1,1], [0,0,0,0,0]])
a2 = np.array([[ [0,0,0], [0,1,0], [0,1,0] ], [ [0,0,0], [0,1,0], [0,0,0] ], [ [0,0,0], [0,1,0], [0,0,0] ]])

print(boundary_cropping(a1, a1 != 0))
# [[1 0 1 1]]
print(boundary_cropping(a2, a2 != 0))
# [[[1] [1]] [[1] [0]] [[1] [0]]]




## Block Reshaping
def get_a_block(a, r, c):
    pick_count = 0
    skip_count = 0
    block = list()
    row = list()
    for value in a:
        if skip_count > 0:
            skip_count -= 1
            continue
        if pick_count < c:
            row.append(value)
            pick_count += 1
        else:
            block.append(row)
            if len(block) == r:
                return block
            pick_count = 0
            row = list()
            skip_count = r * c - 1
    block.append(row)
    return block

def shape_as_blocks(a, r, c):
    if len(a.flat) % (r * c) != 0:
        print("Invalid block size")
        exit(0)
    num_of_blocks = int(len(a.flat) / (r * c))
    a_flat = list(a.flat)
    result = list()
    for i in range(num_of_blocks):
        block = get_a_block(a_flat, r, c)
        result.append(block)
        a_flat = a_flat[c:]
    result_arr = np.array(result)
    return result_arr

arr = np.array([[1,2,3,4], [5,6,7,8], [9,0,1,2]])
print(shape_as_blocks(arr, 2, 2))



## Population Variance from Subpopulation Variance
def pop_var_from_subpop_var(groups):
    variance  = np.array( [ np.var(group)for group in groups] )
    averages = np.array( [ np.mean(group)for group in groups] )
    counts = np.array( [ np.size(group)for group in groups] )
    average = np.average(averages, weights=counts)
    size = 0
    for count in counts:
        size += count
    return np.sum((counts) * variance + counts * (averages - average)**2) / (size)
   
groups = [np.array([1,2,3,4]), np.array([5,6])]
print(pop_var_from_subpop_var(groups))
# 2.9166666666666665



## Shuffle a Large List
import random

l = [1,2,3,4,5]

def shuffle_list_inplace_constant_memory(l):
    for i in range((len(l)-1),0,-1):
        j = random.randint(0,i)
        l[i],l[j] = l[j],l[i]
shuffle_list_inplace_constant_memory(l)
print(l)





## Acquiring Coordinates
def coordinates_from_steps(a, s, dtype=int):
    result = list()
    rowCount,ColumnCount = (0,0)
    for index, value in np.ndenumerate(a):
        if ( rowCount == 0 ) and ( ColumnCount == 0 ):
            result.append(list(index))
        if(index[1] == 0):
            rowCount += 1
        if( rowCount >= s[0]):
            rowCount = 0
        ColumnCount += 1
        if( ColumnCount >= s[1]):
            ColumnCount = 0
    return np.array(result)

print(coordinates_from_steps(np.array([[1,2],[3,4]]), (1,1)))
# [[0 0]
#  [0 1]
#  [1 0]
#  [1 1]]

print(coordinates_from_steps(np.array([[1,2],[3,4]]), (1,2)))
# [[0 0]
#  [1 0]]