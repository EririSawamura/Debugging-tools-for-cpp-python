# sorting algorithm from small to large

def copy_array(alist):
    b = []

    for i in alist:
        b.append(i)

    return b

# bubble sort
def bubble_sort(alist):
    length = len(alist)

    for i in range (0, length - 1):
        
        for j in range (i+1, length):
            
            if alist[i] > alist[j]:
                alist[i], alist[j] = alist[j], alist[i]

    return alist

# selection sort
def selection_sort(alist):
    length = len(alist)

    for i in range (0, length):
        k = i
        
        for j in range(k+1, length):
            if alist[k] > alist[j]:
                k = j
        
        if k != i:
            alist[i], alist[k] = alist[k], alist[i]
            
    return alist

# insertion sort
def insertion_sort(alist):
    length = len(alist)

    for i in range(1, length):
        j = i

        while j > 0 and alist[j-1] > alist[j]:
            alist[j], alist[j-1] = alist[j-1], alist[j]
            j = j - 1
            
    return alist

# quick sort
def quickSort(alist):
   quickSortHelper(alist,0,len(alist)-1)
   return alist

def quickSortHelper(alist,first,last):
   if first<last:

       splitpoint = partition(alist,first,last)

       quickSortHelper(alist,first,splitpoint-1)
       quickSortHelper(alist,splitpoint+1,last)


def partition(alist,first,last):
   pivotvalue = alist[first]

   leftmark = first+1
   rightmark = last

   done = False
   while not done:

       while leftmark <= rightmark and alist[leftmark] <= pivotvalue:
           leftmark = leftmark + 1

       while alist[rightmark] >= pivotvalue and rightmark >= leftmark:
           rightmark = rightmark -1

       if rightmark < leftmark:
           done = True
       else:
           alist[leftmark], alist[rightmark] = alist[rightmark], alist[left]

   alist[first], alist[rightmark] = alist[rightmark], alist[first]

   return rightmark

# merge sort
def mergeSort(alist):
    if len(alist)>1:
        mid = len(alist)//2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]

        mergeSort(lefthalf)
        mergeSort(righthalf)

        i=0
        j=0
        k=0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i] < righthalf[j]:
                alist[k]=lefthalf[i]
                i=i+1
            else:
                alist[k]=righthalf[j]
                j=j+1
            k=k+1

        while i < len(lefthalf):
            alist[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j < len(righthalf):
            alist[k]=righthalf[j]
            j=j+1
            k=k+1

    return alist

# shell sort
def shellSort(alist):
    sublistcount = len(alist)//2
    while sublistcount > 0:

        for startposition in range(sublistcount):
            gapInsertionSort(alist,startposition,sublistcount)

        sublistcount = sublistcount // 2

    return alist

def gapInsertionSort(alist,start,gap):
    for i in range(start+gap,len(alist),gap):

        currentvalue = alist[i]
        position = i

        while position>=gap and alist[position-gap]>currentvalue:
            alist[position]=alist[position-gap]
            position = position-gap

        alist[position]=currentvalue

# heap sort
def heapsort(alist):
    #convert alist to heap
    length = len(alist) - 1
    leastParent = int(length / 2)
    for i in range (leastParent, -1, -1):
        moveDown(alist, i, length)

    # flatten heap into sorted array
    for i in range (length, 0, -1):
        if alist[0] > alist[i]:
            alist[0], alist[i] = alist[i], alist[0]
            moveDown(alist, 0, i-1)
    
    return alist

def moveDown(alist, first, last):
    largest = 2 * first + 1
    while largest <= last:
        # right child exists and is larger than left child
        if (largest < last) and (alist[largest] < alist[largest+1]):
            largest += 1

        #right child is larger than parent
        if alist[largest] > alist[first]:
            alist[largest], alist[first] = alist[first], alist[largest]
            first = largest
            largest = 2 * first + 1
        else:
            return

# main part
def main():
    n = int(input())
    a = []
    for i in range(n):
        a.append(int(input()))
    b = heapsort(copy_array(a))
    for e in b:
        print(e)

main()
