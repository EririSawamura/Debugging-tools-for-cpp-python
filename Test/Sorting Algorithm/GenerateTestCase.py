from random import randint

def generate():
    n = randint(1, 100)
    alist = []
    for i in range (n):
        alist.append(randint(1, 200))
    return alist

# bubble sort
def bubble_sort(alist):
    length = len(alist)

    for i in range (0, length - 1):
        
        for j in range (i+1, length):
            
            if alist[i] > alist[j]:
                alist[i], alist[j] = alist[j], alist[i]

    return alist

def store(filename, i):
    file = open(filename, "w")
    select = randint(0,1)
    if select == 0:
        alist = generate()
    else:
        alist = bubble_sort(generate())
        print(i)
    file.write(str(len(alist)) + "\n")
    for a in alist:
        file.write(str(a) + "\n")
    file.close()

def main():
    for i in range(1, 101):
        filename = ".\\test\\test" + str(i) + ".in"
        store(filename, i)

main()
