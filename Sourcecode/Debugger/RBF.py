import numpy as np
import matplotlib.pyplot as plt
def RBF(CoverageMatrix, CoverageLabel):
    #Transform CoverageMatrix, CoverageLabel to Dataset, Labels
    Dataset = np.matrix(CoverageMatrix).astype(int)
    Labels = np.array(CoverageLabel)

    #Train data
    parameters = Train(Dataset, Labels)
    T_dataset = np.identity(Dataset.shape[1])
    result,rubbish = Moveforward(T_dataset, parameters)

    #Sort result
    result,index = Quicksort(np.squeeze(np.asarray(result)))
    return index

def sigmoid(dW, cookie):
    s = np.squeeze(np.asarray(1/(1+np.exp(-cookie))))
    dZ = np.squeeze(np.asarray(dW)) * s * (1-s)
    if (cookie.shape[0] == 1):
        dZ = dZ.reshape((1, dZ.shape[0]))
    return dZ

def Moveforward(Dataset, parameters):
    cookies = []
    for i in range(1, len(parameters) // 2):
        Dataset_prev = Dataset
        Z = np.dot(parameters['L' + str(i)], Dataset_prev) + parameters['H' + str(i)]
        cookie = (Dataset_prev, parameters['L' + str(i)], parameters['H' + str(i)])
        Dataset = 1 / (1 + np.exp(-Z))
        cookies.append((cookie, Z))
    Z = np.dot(parameters['L' + str(len(parameters) // 2)], Dataset_prev) + parameters['H' + str(len(parameters) // 2)]
    cookie = (Dataset_prev, parameters['L' + str(len(parameters) // 2)], parameters['H' + str(len(parameters) // 2)])
    cookies.append((cookie, Z))
    return 1 / (1 + np.exp(-Z)), cookies

def Movebackward(WA, Labels, cookies):
    grads = {}
    Labels = Labels.reshape(WA.shape)

    linear_cookie, activation_cookie = cookies[len(cookies)-1]
    dZ = sigmoid(- (np.divide(Labels, WA) - np.divide(1 - Labels, 1 - WA)), activation_cookie)
    W_prev, dL, dH = linear_cookie
    grads["dW" + str(len(cookies))] = np.dot(dL.T, dZ)
    grads["dL" + str(len(cookies))] = np.dot(dZ, W_prev.T) / W_prev.shape[1]
    grads["dH" + str(len(cookies))] = np.sum(dZ) / W_prev.shape[1]

    for i in reversed(range(len(cookies)-1)):
        linear_cookie, activation_cookie = cookies[i]
        dZ = sigmoid(grads["dW" + str(i + 2)], activation_cookie)
        W_prev, dL, dH = linear_cookie
        grads["dW" + str(i+1)] = np.dot(dL.T, dZ)
        grads["dL" + str(i+1)] = np.dot(dZ, W_prev.T) / W_prev.shape[1]
        grads["dH" + str(i+1)] = np.sum(dZ) / W_prev.shape[1]

    return grads

def getModel(Dataset, Labels, Layers, learn = 0.0075):
    np.random.seed(5)
    costs = []

    # Parameters initialization.
    parameters = {}
    for i in range(1, len(Layers)):
        parameters['L' + str(i)] = np.random.randn(Layers[i], Layers[i - 1]) * 0.01
        parameters['H' + str(i)] = np.zeros((Layers[i], 1))

    # Loop for machine learning of neuron network
    for l in range(0, 3000):
        # Forward propagation.
        WA, cookies = Moveforward(Dataset.T, parameters)

        # Backward propagation.
        grads = Movebackward(WA, Labels, cookies)

        # Update parameters.
        for i in range(len(parameters) // 2):
            parameters["L" + str(i + 1)] = parameters["L" + str(i + 1)] - learn * grads["dL" + str(i + 1)]
            parameters["H" + str(i + 1)] = parameters["H" + str(i + 1)] - learn * grads["dH" + str(i + 1)]

        # Print the cost every 100 training example
        if l % 100 == 0:
            cost = np.squeeze(-np.sum(np.multiply(np.log(WA), Labels) + np.multiply(np.log(1 - WA), 1 - Labels)) / Labels.shape[1])
            costs.append(cost)
            
    #Plot the cost
    plt.plot(np.squeeze(costs))
    plt.ylabel('cost')
    plt.xlabel('iterations (*100)')
    plt.title("Cost change when learning rate =" + str(learn))
    plt.show()

    return parameters

def Train(Dataset, Labels):
    # Four layers, including an input layer, two hidden layers and one output layer
    Layers = [Dataset.shape[1],5,5,1]
    Labels = np.array([Labels])
    parameters = getModel(Dataset, Labels, Layers, learn = 0.3)
    return parameters

def Quicksort(array):
    Index = []
    for i in range(len(array)):
        Index.append(i+1)
    Rank,Index = Quicksort_Rec(array, Index)
    return Rank, Index

def Quicksort_Rec(Rank, Index):
    less = []
    equal = []
    greater = []
    lessIndex = []
    equalIndex = []
    greaterIndex = []
    if len(Rank) > 1:
        pivot = Rank[0]
        for x in range(len(Rank)):
            if Rank[x] < pivot:
                less.append(Rank[x])
                lessIndex.append(Index[x])
            elif Rank[x] == pivot:
                equal.append(Rank[x])
                equalIndex.append(Index[x])
            elif Rank[x] > pivot:
                greater.append(Rank[x])
                greaterIndex.append(Index[x])
        iRank = []
        iIndex = []
        if len(lessIndex) > 0:
            less, lessIndex = Quicksort_Rec(less,lessIndex)
            for item in less:
                iRank.append(item)
            for item in lessIndex:
                iIndex.append(item)
        if len(equalIndex) > 0:
            equal, equalIndex = Quicksort_Rec(equal,equalIndex)
            for item in equal:
                iRank.append(item)
            for item in equalIndex:
                iIndex.append(item)
        if len(greaterIndex) > 0:
            greater, greaterIndex = Quicksort_Rec(greater, greaterIndex)
            for item in greater:
                iRank.append(item)
            for item in greaterIndex:
                iIndex.append(item)
        return iRank, iIndex
    else:
        return Rank, Index
