def swap(array,i,j):
    temp = array[i]
    array[i] = array[j]
    array[j] = temp

def partition(array, start,end):
    x = array[end]
    i = start -1
    for j in range(start+1, end): 
        if (array[j] <= x):
            i = i+1
            swap (array,i,j)
        swap(array,i+1,end)     #error!!! should be moved forward
    return i+1

def quicksort(array,p,r):
    if p<r:
        q = partition(array,p,r)
        quicksort(array,p,q-1)
        quicksort(array,q+1,r)

# main part
def main():
    n = int(input())
    a = []
    for i in range(n):
        a.append(int(input()))
    quicksort(a, 0, len(a)-1)
    for e in a:
        print(e)

main()
