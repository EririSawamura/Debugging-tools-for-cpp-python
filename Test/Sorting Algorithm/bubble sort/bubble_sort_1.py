def bubble_sort(array):
    number = 1
    ArrayIndex = 0
    numchange = 0
    TotalNumberofLoops = len(array)
    OuterLoop = 0
    InnerLoop = 0

    while OuterLoop < TotalNumberofLoops:
        InnerLoop = OuterLoop + 1
        while InnerLoop < TotalNumberofLoops:
            if array[OuterLoop] < array[InnerLoop]:
                numchange = array[InnerLoop]
                array[OuterLoop] = array[InnerLoop]     #error!!!! should be ==> array[InnerLoop] = array[OuterLoop]
                array[InnerLoop] = numchange

            InnerLoop=InnerLoop + 1
        #print array
        OuterLoop = OuterLoop + 1
    
    return array

# main part
def main():
    n = int(input())
    a = []
    for i in range(n):
        a.append(int(input()))
    b = bubble_sort(a)
    for e in b:
        print(e)

main()
