from operator import itemgetter
def getJaccard(statementCoverage):
    ncf = statementCoverage[0]
    ncs = statementCoverage[1]
    nuf = statementCoverage[2]
    nf = ncf + nuf
    if nf+ncs!=0:
        return ncf / (nf + ncs)
    else:
        return -1

def rankBySuspiciousness(CoverageList):
    suspiciousness = [];
    i = 1;
    for statementCoverage in CoverageList:
        suspiciousness.append([i, getJaccard(statementCoverage)]);
        i += 1
    suspiciousnessRank = sorted(suspiciousness, key=itemgetter(1), reverse=True)
    return suspiciousnessRank

