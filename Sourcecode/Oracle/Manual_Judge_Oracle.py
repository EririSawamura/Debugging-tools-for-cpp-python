# This is for manual checking
# User is responsible for checking whether the result is correct

def check(inputpath, outputpath):
    inp = open(inputpath)
    print("Input: ")
    for line in inp.readlines():
        print(line)
    inp.close()
    print()
    print("Output: ")
    out = open(outputpath)
    for line in out.readlines():
        print(line)
    print()
    while True:
        d = input("Your decision (y/n): ")
        if d.lower == 'y':
            return True
        if d.lower == 'n':
            return False
        print("Unrecognized decision. ", end = ' ')
    