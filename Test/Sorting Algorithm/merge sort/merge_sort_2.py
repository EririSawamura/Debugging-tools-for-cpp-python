from math import floor

def merge(array, p, q, r):
    left_array = []
    right_array = []

    k = p
    while (k <= q):                  
        left_array.append(array[k])
        k += 1
    while (k <= r):                  
        right_array.append(array[k])
        k += 1

    k = p
    i = 0
    j = 0
    while (i < len(left_array) and j < len(right_array)):
        if (left_array[i] <= right_array[j]):	
            array[k] = left_array[i]
            k += 1
            i += 1
        else:
            array[k] = right_array[j]
            k += 1
            j += 1

    while (i < len(left_array)):
        array[k] = left_array[i]
        k += 1
        i += 1

    while (j < len(right_array)):
        array[k] = right_array[j]
        k += 1
        j += 1
    #print("Merging", array)

def merge_sort(array, p, r):
    #print("Splitting", array)
    if p < r:
        q = floor((p + r) / 2)
        merge_sort(array, p, q)
        merge_sort(array, q + 1, r)
        merge(array, p, q, r)
    return array

# main part
def main():
    n = int(input())
    a = []
    for i in range(n):
        a.append(int(input()))
    b = merge_sort(a, 0, len(a))        #error!!! should be ==> b=merge_sort(a, 0, len(a)-1)
    for e in b:
        print(e)

main()