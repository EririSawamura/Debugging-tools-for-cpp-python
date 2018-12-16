# Attention: only are c/c++/py supported!!!
from TestingTools.ctest import CTesting
from TestingTools.pytest import PythonTesting
from Debugger import Crosstab, Tarantula, LineCoverage, Jaccard, Ochiai, RBF
#import Crosstab, Tarantula, LineCoverage, Jaccard, Ochiai, RBF

class FaultStorage:
    def __init__(self, srccode):
        self.srccode = srccode
        self.records = []
        self.tempstorage = []
        file = open(srccode)
        self.lines = len(file.readlines())
        file.close()
        if self.srccode.endswith('.py'):
            self.type = 'python'
            self.py = PythonTesting(srccode)
        elif self.srccode.endswith('.c') or self.srccode.endswith('.cpp'):
            self.type = 'c'
            self.c = CTesting(srccode)
        else:
            raise Exception("We are not supported for this code debugging. ")

    def Test(self, inputcase, outputpath):
        #print(inputcase, " " , outputpath)
        if self.type == 'python':
            #print(type(self.py))
            self.tempstorage = self.py.Test(inputcase, outputpath)
            #print(self.tempstorage)
        elif self.type == 'c':
            self.tempstorage = self.c.Test(inputcase, outputpath)
        else:
            print("We are not supported for this code debugging. Coming soon. ")
            return
    
    def EndTest(self):
        if self.type == 'python':
            self.py.Delete()
        elif self.type == 'c':
            self.c.Delete()

    def ResultRecord(self, result):
        temp = [result]
        temp.extend(self.tempstorage)
        self.records.append(temp)
        self.tempstorage = []
    
    def GenerateTarantula(self):
        return Tarantula.rankBySuspiciousness(LineCoverage.getLineCoverage(self.lines, self.records))

    def GenerateCrosstab(self):
        return Crosstab.rankBySuspiciousness(LineCoverage.getLineCoverage(self.lines, self.records))

    def GenerateJaccard(self):
        return Jaccard.rankBySuspiciousness(LineCoverage.getLineCoverage(self.lines, self.records))

    def GenerateOchiai(self):
        return Ochiai.rankBySuspiciousness(LineCoverage.getLineCoverage(self.lines, self.records))

    def GenerateRBF(self):
        CoverageMatrix, CoverageLabel=LineCoverage.getLineCoverageMatrix(self.lines, self.records)
        return RBF.RBF(CoverageMatrix, CoverageLabel)
