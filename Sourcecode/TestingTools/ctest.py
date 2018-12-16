# Structure:
# Input: source code, sample input
# Output: code coverage report, output after compiling
# This is for C / C++ testing
# gcc and g++ is required
import os, glob

class CTesting:
    def __init__(self, cfilename):
        self.cname = cfilename.split("\\")[-1]
        if cfilename.endswith('.c'):
            use = 'gcc'
        elif cfilename.endswith('.cpp'):
            use = 'g++'
        else:
            return
        result = os.popen(use + " -fprofile-arcs -ftest-coverage \"" + cfilename + "\" -o test.out")
        res = result.read()
        for line in res.splitlines():
            #print(line)
            pass
    
    def Test(self, inputpath, outputpath):
        result = os.popen("test.out" + " < \"" + inputpath + "\" > \"" + outputpath + "\"")
        res = result.read()
        for line in res.splitlines():
            #print(line)
            pass
        result = os.popen("gcov " + self.cname)
        res = result.read()
        for line in res.splitlines():
            #print(line)
            pass
        #print(use + " -Wall -fprofile-arcs -ftest-coverage " + cfilename + " -o test.out")
        #print("test.out < " + inputpath  + " > " + outputpath)
        #print("gcov " + cname)
        # Evaluate gcov file
        file = open(self.cname + ".gcov")
        lines = []
        for line in file.readlines():
            s = line.split(":")
            if s[0][-1] != '-' and s[0][-1] != '#':
                lines.append(int(s[1]))
        file.close()
        for filename in glob.glob('*.gcov'):
            os.remove(filename)
        for filename in glob.glob('*.gcda'):
            os.remove(filename)
        return lines
    
    def Delete(self):
        for filename in glob.glob("*.gcno"):
            os.remove(filename)
        os.remove("test.out")


def main():
    src = input("The position of source code: ")
    inputpath = input("Please specify the input path: ")
    outputpath = input("Please specify the output path: ")
    print(CTesting(src, inputpath, outputpath))

#main()
