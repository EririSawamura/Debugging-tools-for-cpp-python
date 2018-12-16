def insertion_sort(Array):
    First = 1
    Last = len(Array)
    PositionOfNext = Last - 1
    while PositionOfNext >= First:
        Next = Array[PositionOfNext]
        Current = PositionOfNext
        while (Current < Last) and (Next > Array[Current] + 1):
            Current = Current + 1
            Array[Current-1]  = Array[Current]          # error!!! should be ==> Array[Current-1], Array[Current] = Array[Current], Array[Current-1]
        Array[Current] = Next
        PositionOfNext = PositionOfNext - 1
    
    return Array

# main part
def main():
    n = int(input())
    a = []
    for i in range(n):
        a.append(int(input()))
    b = insertion_sort(a)
    for e in b:
        print(e)

main()