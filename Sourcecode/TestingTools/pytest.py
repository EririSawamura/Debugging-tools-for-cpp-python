import os, shutil
from subprocess import check_output

class PythonTesting:
    def __init__(self, pyfile):
        self.pyfile = "test.py"
        shutil.copyfile(pyfile, self.pyfile)
        #print("Copy successfully")

    def Test(self, inputpath, outputpath):
        result = os.popen("coverage run " + self.pyfile + " < \"" + inputpath + "\" > \"" + outputpath + "\"")
        res = result.read()
        for line in res.splitlines():
            #print(line)
            pass
        #print("coverage run " + pyfilename + " < " + inputpath + " > " + outputpath)
        Report = check_output("coverage report -m "+self.pyfile, shell=True).decode()
        ReportList = Report.split("\n")  # Analyze information in the Report information
        ReportInfo = ReportList[2].split(" ")
        ReportInfo = [x.replace('\r', '') for x in ReportInfo if x != '']
        ReportInfo = [x.replace(',', '') for x in ReportInfo]
        Totlength = int(ReportInfo[1])
        MissingLine = []
        CoverLine = []
        if len(ReportInfo) > 4:
            for i in range(4, len(ReportInfo)):
                if '-' in ReportInfo[i]:
                    RInfoList = ReportInfo[i].split('-')
                    L = RInfoList[0]
                    R = RInfoList[1]
                    for i in range(int(L), int(R) + 1):
                        MissingLine.append(i)
                else:
                    MissingLine.append(int(ReportInfo[i]))
        for i in range(1,Totlength+1):
            if i not in MissingLine:
                CoverLine.append(i)
        return CoverLine

    def Delete(self):
        os.remove(self.pyfile)
        os.remove(".coverage")

