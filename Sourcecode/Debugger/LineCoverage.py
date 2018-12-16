def getLineCoverage(lineNum, testCoverageList):
    testNum = len(testCoverageList)
    ncf = [0] * lineNum
    ncs = [0] * lineNum
    ns = 0
    nf = 0
    for testCoverage in testCoverageList:
        if testCoverage[0]:
            ns += 1
            for i in range(1, len(testCoverage)):
                ncs[testCoverage[i]-1] += 1
        else:
            nf += 1
            for i in range(1, len(testCoverage)):
                ncf[testCoverage[i]-1] += 1
    nuf = []
    nus = []
    for i in range(0, lineNum):
        nuf.append(nf - ncf[i])
        nus.append(ns - ncs[i])

    lineCoverage = [ncf, ncs, nuf, nus]
    lineCoverage = list(map(list, zip(*lineCoverage)))
    return lineCoverage

def getLineCoverageMatrix(lineNum, testCoverageList):
    #print(lineNum)
    #print(testCoverageList)
    CoverageLabel = [0]*(len(testCoverageList))
    CoverageMatrix = []
    for i in range(len(testCoverageList)):
        CoverageMatrix.append([0]*lineNum)
    for i in range(len(testCoverageList)):
        if testCoverageList[i][0]:
            CoverageLabel[i] += 1
        for j in range(1,len(testCoverageList[i])):
            CoverageMatrix[i][testCoverageList[i][j]-1] = CoverageMatrix[i][testCoverageList[i][j]-1] + 1
    return CoverageMatrix, CoverageLabel

"""lineNum = 29
testCoverageList = [[True, 5, 6, 8, 9, 12, 15, 20], [False, 1, 5, 6, 8, 9, 12, 15, 20],[True, 2, 5, 6, 8, 9, 11, 13, 17],]
print(getLineCoverageMatrix(lineNum, testCoverageList))"""
