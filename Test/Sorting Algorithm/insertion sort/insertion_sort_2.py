# insertion sort
def insertion_sort(numbers):
    for i in range(len(numbers)-1):
        position=1                                                  #error!!! should be ==> position = i
        while position>0 and numbers[position]<numbers[position-1]:     
            #print("Position:",numbers[position])
            #print("Position-1:",numbers[position-1])
            temp=numbers[position-1]
            numbers[position-1]=numbers[position]
            numbers[position]=temp
            #print("New value of position",numbers[position])

            position=position+1                                     #error!!! should be ==> position = position - 1
            
    return numbers

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