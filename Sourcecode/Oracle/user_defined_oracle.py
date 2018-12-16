def SortingJudge(inname, outname):
    infile = open(inname, "r")
    a = []
    flag = False
    for line in infile.readlines():
        if flag:
            a.append(int(line[:-1]))
        flag = True
    outfile = open(outname, "r")
    sorteda = []
    for line in outfile.readlines():
        sorteda.append(int(line[:-1]))
    for s in sorteda:
        if s in a:
            a.remove(s)
        else:
            return False
    if len(a) > 0:
        return False
    
    flag = True
    length = len(sorteda)
    for i in range(0, length-1):
        if sorteda[i] > sorteda[i+1]:
            flag = False
            break
    if flag:
        return True

    flag = True
    for i in range(0, length-1):
        if sorteda[i] < sorteda[i+1]:
            flag = False
            break
    return flag

def check(inputpath, outputpath):
    return SortingJudge(inputpath, outputpath)