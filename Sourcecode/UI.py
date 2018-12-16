# This is user interface
import Fault, glob, importlib, os, shutil

def printProgress(iteration, total, prefix='', suffix='', decimals=1, barLength=100):
    """
    Call in a loop to create a terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        barLength   - Optional  : character length of bar (Int)
    """
    import sys
    formatStr = "{0:." + str(decimals) + "f}"
    percent = formatStr.format(100 * (iteration / float(total)))
    filledLength = int(round(barLength * iteration / float(total)))
    bar = '#' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)),
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

def main():
    while True:
        src = input("Please input the location of source code: ")
        if os.path.isfile(src):
            break
        print("Invalid file. Please check! ")
    while True:
        testSuite = input("Please input the location of the test suite: ")
        if os.path.exists(testSuite):
            break
        print("Invalid diretory. Please check! ")
    order = input("Oracle Types:\n1.Human juedgement\n2.Fixed-answer judgement\n3.Special judgement\nPlease indicate your selection: ")
    while order!='1' and order!='2' and order!='3':
        order = input("Error input! Please give the answer in 1-3")
    if order == '1':
        oracle = importlib.import_module("Oracle.Manual_Judge_Oracle")
    if order == '2':
        oracle = importlib.import_module("Oracle.Judge_Oracle")
    if order == '3':
        path = input("Please input the path of Oracle: ")
        shutil.copyfile(path, ".\\Oracle\\user_defined_oracle.py")
        oracle = importlib.import_module("Oracle.user_defined_oracle")

    fault = Fault.FaultStorage(src)

    f_list = os.listdir(testSuite)

    total = 0
    for filename in f_list:
        if filename.endswith(".in"):
            total = total + 1
    
    i = 0
    printProgress(i, total, prefix='Progress:', suffix='Complete', barLength=50)
    for filename in f_list:
        #suggestion: replace the last .in with .out // may be a filename containing multiple .in
        if not filename.endswith(".in"):
            continue
        #print(filename)
        fault.Test(testSuite + "\\" + filename, testSuite + "\\" + filename.replace(".in", ".out"))
        fault.ResultRecord(oracle.check(testSuite + "\\" + filename, testSuite + "\\" + filename.replace(".in", ".out")))
        os.remove(testSuite + "\\" + filename.replace(".in", ".out"))
        i += 1
        printProgress(i, total, prefix='Progress:', suffix='Complete', barLength=50)

    fault.EndTest()
    
    #print(fault.records)
    # select debugger here
    while True:
        #move to the back and list all possible debuggers
        print("Possible debuggers: 1. Tarantula 2. Crosstab 3. Jaccard 4. Ochiai 5. Radio basis function")
        print("Other operations: e.exit")
        debugger = input("Please select the one you want: ")
        while debugger!='1' and debugger!='2' and debugger!='3' and debugger!='4' and debugger!='5' and debugger!='e':
            debugger = input("Error input! Please give the answer in 1-5 or e: ")
        if debugger == '1':
            print("You are now using Tarantula. ")
            suspiciousnessRank = fault.GenerateTarantula()
            #print(suspiciousnessRank)
            generateReport(suspiciousnessRank)
        elif debugger == '2':
            print("You are now using Crosstab. ")
            suspiciousnessRank = fault.GenerateCrosstab()
            #print(suspiciousnessRank)
            generateCrosstabReport(suspiciousnessRank)
        elif debugger == '3':
            print("You are now using Jaccard. ")
            suspiciousnessRank = fault.GenerateJaccard()
            generateReport(suspiciousnessRank)
        elif debugger == '4':
            print("You are now using Ochiai. ")
            suspiciousnessRank = fault.GenerateOchiai()
            generateReport(suspiciousnessRank)
        elif debugger == '5':
            print("You are now using RBF. ")
            index = fault.GenerateRBF()
            print("The most suspicious line:\n\tLine Rank")
            count = 0
            if len(index) >= 10:
                for i in range(len(index)-1,len(index)-11,-1):
                    count += 1
                    print("\t{:<5}{:<5}".format(index[i]+1,count))
            else:
                for i in range(len(index)-1,-1,-1):
                    count += 1
                    print("\t{:<5}{:<5}".format(index[i]+1,count))
        elif debugger == 'e':
            break

def generateReport(suspiciousnessRank):
    count = 0
    check = 0
    for item in suspiciousnessRank:
        if item[1] != -1:
            check = 1
    if check == 0:
        print("You must provide a test suite containing both successful abd failed test cases.")
    else:
        print("The most suspicious line:\n\tLine Rank")
        if len(suspiciousnessRank) >= 10:
            for item in suspiciousnessRank:
                count += 1
                print("\t{:<5}{:<5}".format(item[0],count))
                if count == 10:
                    break
        else:
            for item in suspiciousnessRank:
                count += 1
                print("\t{:<5}{:<5}".format(item[0],count))

def generateCrosstabReport(suspiciousnessRank):
    count = 0
    isValidTest = False
    for item in suspiciousnessRank:
        if item[1] != -1:
            isValidTest = True
 #   if not isValidTest:
 #       print("You must provide a test suite containing both successful abd failed test cases.")
 #   else:
    print("The most suspicious line:\n\tLine Rank")
    if len(suspiciousnessRank) >= 10:
        for item in suspiciousnessRank:
            count += 1
            print("\t{:<5}{:<5}".format(item[0],count))
            if count == 10:
                break
    else:
        for item in suspiciousnessRank:
            count += 1
            print("\t{:<5}{:<5}".format(item[0],count))
    
#main()
if __name__ == "__main__":
    main()

