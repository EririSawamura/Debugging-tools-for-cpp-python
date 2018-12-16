from operator import itemgetter
# "main" function
# compute and rank the statement with suspiciousness
# receiving list of statement coverage information
def rankBySuspiciousness(CoverageList):
    suspiciousness = []
    i = 1
    for statementCoverage in CoverageList:
        suspiciousness.append([i, getSuspiciousnessValue(getCrosstab(statementCoverage))])
        i += 1
    suspiciousnessRank = sorted(suspiciousness, key=itemgetter(1), reverse=True)
    return suspiciousnessRank

# compute the crosstab from statement coverage information
def getCrosstab(statementCoverage):
    ncf = statementCoverage[0]
    ncs = statementCoverage[1]
    nuf = statementCoverage[2]
    nus = statementCoverage[3]
    nc = ncf + ncs
    nu = nuf + nus
    nf = ncf + nuf
    ns = ncs + nus
    n = nc + nu
    crosstab = [[ncs, nus, ns], [ncf, nuf, nf], [nc, nu, n]]
    return crosstab

# get the final suspicious value using crosstab methods
def getSuspiciousnessValue(crosstab):
    nc = crosstab[2][0]
    nf = crosstab[2][1]
    if nc == 0 or nf == 0:
        return -1
    contingencyCoefficient = getContingencyCoefficient(crosstab)
    associationValue = getAssociationValue(crosstab)
    if associationValue > 1:
        return contingencyCoefficient
    elif associationValue == 1:
        return 0
    else:
        return -1 * contingencyCoefficient    

def getChiSquareValue(crosstab):
    ncs = crosstab[0][0]
    nus = crosstab[0][1]
    ns = crosstab[0][2]
    ncf = crosstab[1][0]
    nuf = crosstab[1][1]
    nf = crosstab[1][2]
    nc = crosstab[2][0]
    nu = crosstab[2][1]
    n = crosstab[2][2]
    ecf = nc * nf / n
    ecs = nc * ns / n
    euf = nu * nf / n
    eus = nu * ns / n
    chiSquareValue = (ncf - ecf) ** 2 / ecf + (ncs - ecs) ** 2 / ecs + (nuf - euf) ** 2 / euf + (nus - eus) ** 2 / eus
    return chiSquareValue

def getContingencyCoefficient(crosstab):
    chiSquareValue = getChiSquareValue(crosstab)
    testNum = crosstab[2][2]
    return chiSquareValue / testNum

def getAssociationValue(crosstab):
    ncf = crosstab[1][0]
    nf = crosstab[0][2]
    ncs = crosstab[1][0]
    ns = crosstab[0][2]
    pf = ncf / nf
    ps = ncs / ns
    associationValue = pf / ps
    return associationValue
