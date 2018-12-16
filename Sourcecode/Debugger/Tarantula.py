from operator import itemgetter
def rankBySuspiciousness(CoverageList):
    suspiciousness = []
    i = 1
    for statementCoverage in CoverageList:
        suspiciousness.append([i, getTarantula(statementCoverage)])
        i += 1
    suspiciousnessRank = sorted(suspiciousness, key=itemgetter(1), reverse=True)
    #print(suspiciousnessRank)
    return suspiciousnessRank

def getTarantula(statementCoverage):
    #print(statementCoverage)
    ncf = statementCoverage[0]
    ncs = statementCoverage[1]
    nuf = statementCoverage[2]
    nus = statementCoverage[3]
    nf = ncf + nuf
    ns = ncs + nus
    if nf!=0 and ns!=0 and (ncf / nf) + (ncs / ns)!=0:
        return (ncf / nf) / ((ncf / nf) + (ncs / ns))
    else:
        return -1

"""CoverageList = [[0,1,1,2], [1,2,0,1]]
print(rankBySuspiciousness(CoverageList))"""
