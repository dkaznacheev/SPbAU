# Remove equal adjacent elements
#
# Example input: [1, 2, 2, 3]
# Example output: [1, 2, 3]
def remove_adjacent(lst):
    lst1 = []
    lastc = lst[0]
    lst1.append(lastc)
    for c in lst[1:]: 
        if c != lastc:
            lst1.append(c)
            lastc = c
    return lst1
 
# Merge two sorted lists in one sorted list in linear time
#
# Example input: [2, 4, 6], [1, 3, 5]
# Example output: [1, 2, 3, 4, 5, 6]
def linear_merge(lst1, lst2):
    i = 0
    j = 0
    l1 = len(lst1)
    l2 = len(lst2)
    lst3 = []
    while i < l1 or j < l2:
        if j >= l2:
            lst3.extend(lst1[i:])
            i = l1
        elif i >= l1:
            lst3.extend(lst2[j:])
            j = l2
        elif lst1[i] < lst2[j]:
            lst3.append(lst1[i])
            i += 1
        else:
            lst3.append(lst2[j])
            j += 1
    return lst3
                                                       