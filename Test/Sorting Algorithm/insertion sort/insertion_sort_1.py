# insertion sort
def insertion_sort(alist):
    length = len(alist)

    for i in range(1, length):
        j = i

        while j < length and alist[j-1] > alist[j]:         # error should be ==> while j > 0 and alist[j-1] > alist[j]
            alist[j], alist[j-1] = alist[j-1], alist[j]
            j = j + 1                                       # error should be ==> j = j - 1
            
    return alist

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
