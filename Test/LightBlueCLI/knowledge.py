# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.2 (v3.6.2:5fd33b5, Jul  8 2017, 04:57:36) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\Users\ZHANGDorisXStudent\Desktop\LightBlue_NLTK\src\ChatBotDesign\knowledge.py
# Compiled at: 2018-10-06 16:48:26
import random
import json

def calculationFunction(node, mode):
    if mode == 0:
        return
    else:
        if mode == 1:
            spike = 0
            count = 0
            for edge in node.preLinks:
                count += edge.strength
                if edge.isActive():
                    spike += edge.strength

        else:
            if mode == 2:
                spike = 1
                for edge in node.preLinks:
                    if not edge.initiator.isActive():
                        spike = 0

            else:
                if mode == 3:
                    spike = 0
                    for edge in node.preLinks:
                        if edge.initiator.isActive():
                            spike = 1

            node.spike = spike
        return 0


def conbineWords(wordList):
    string = ' '
    for word in wordList:
        string += word
        string += ' '

    return string


class Node:

    def __init__(self, string, level=1):
        self.index = string
        self.actions = {}
        self.state = 0
        self.spikeTime = 0
        self.level = level

    #def reprJSON(self):
        #return dict(index=self.index, actions=self.actions, state=self.state, spikeTime=self.spikeTime, level=self.level)

    def spike(self):
        self.state = 1
        self.spikeTime += 1

    def backward(self, action):
        newAction = 0
        if action in self.actions:
            self.actions[action] += 1
        else:
            if len(self.actions) < 100:
                self.actions[action] = 1
                newAction = 1
        self.state = 0
        return newAction


class Edge:

    def __init__(self, initiatorNode, targetNode, default=True):
        self.initiator = initiatorNode
        self.target = targetNode
        self.stimulateTimes = 1e-08
        self.backwardTimes = 0
        self.strength = 0.1
        self.state = 0
        if default:
            initiatorNode.linkTo(self)
        targetNode.linkFrom(self)

    #def reprJSON(self):
        #return dict(initiator=self.initiator, target=self.target, stimulateTimes=self.stimulateTimes, backwardTimes=self.backwardTimes, strength=self.strength, state=self.state)

    def isActive(self):
        if self.state:
            return True
        else:
            return False

    def cleanState(self):
        self.state = 0

    def stimulate(self):
        self.state = 1
        self.stimulateTimes += 1

    def sleep(self):
        self.state = 0

    def backward(self):
        if self.state:
            self.backwardTimes += 1
            self.state = 0
            self.strength = self.backwardTimes / self.stimulateTimes
            self.initiator.backward()


class ChatItem:

    def __init__(self, inputSent, inputTime, outputSent, outputTime, mode='Retrieval'):
        self.inputSent = inputSent
        self.inputTime = inputTime
        self.outputSent = outputSent
        self.outputTime = outputTime
        self.mode = mode
        self.like = 0

    #def reprJSON(self):
        #return dict(inputSent=self.inputSent, inputTime=self.inputTime, outputSent=self.outputSent, outputTime=self.outputTime, mode=self.mode, like=self.like)


class WorkMemory:

    def __init__(self):
        self.activePatterns = []
        self.action = 0
        self.maxStrength = 0
        self.maxActions = []
        self.countPatterns = []
        self.newPatterns = []
        self.level = 0

    #def reprJSON(self):
        #return dict(activePatterns=self.activePatterns, action=self.action, maxStrength=self.maxStrength, maxActions=self.maxActions, countPatterns=self.countPatterns, newPatterns=self.newPatterns, level=self.level)

    def spikePatterns(self, inputList, patternList, level=5):
        unknownWord = None
        self.level = min(level, len(inputList))
        for i in range(self.level):
            for j in range(len(inputList) - i):
                patternIndex = conbineWords(inputList[j:j + i + 1])
                if patternIndex in patternList:
                    pattern = patternList[patternIndex]
                else:
                    pattern = Node(patternIndex, level=i + 1)
                    patternList[patternIndex] = pattern
                    self.newPatterns.append(patternIndex)
                pattern.spike()
                self.activePatterns.append(pattern)
                if not i and not unknownWord:
                    unknownWord = not unknownWord and not pattern.actions and pattern

        return unknownWord

    def getAction(self):
        file = open("test.txt", "w")
        for pattern in self.activePatterns:
            file.write("[PATTERN]:" + pattern.index + "\n[SPIKETIME]:" + str(pattern.spikeTime) + "\t[LEVEL]:" + str(pattern.level) + "\t[SELFLEVEL]:" + str(self.level) + "\n")
            for action in pattern.actions:
                strength = (pattern.actions[action] + 1) / pattern.spikeTime * pattern.level / self.level
                file.write("\t[ACTION]" + str(action) + "\n")
                file.write("\t[ACTIONTIMES]" + str(pattern.actions[action]) + "\n")
                file.write("\t[STRENGTH]" + str(strength) + "\n")
                file.write("\n")
                if strength > self.maxStrength:
                    self.maxStrength = strength
                    self.maxActions = [action]
                    self.countPatterns = [pattern.index]
                elif strength == self.maxStrength:
                    self.maxActions.append(action)
                    self.countPatterns.append(pattern.index)
        file.close()
        maxCount = 0
        print('[STRENGTH]:', self.maxStrength)
        print('[PATTERNS]:', self.countPatterns)
        print('[ACTIONS]:', self.maxActions)
        for a in set(self.maxActions):
            c = self.maxActions.count(a)
            if c >= maxCount:
                maxCount = c
                self.action = a

        if maxCount == 1:
            if len(self.maxActions) > 1:
                return self.maxActions
            return [self.action]

    def clean(self):
        self.action = 0
        self.activePatterns = []
        self.maxStrength = 0
        self.maxActions = []
        self.countPatterns = []
        self.newPatterns = []
        self.level = 0

    def backward(self, clean=True):
        newLink = 0
        if self.action:
            for pattern in self.activePatterns:
                newLink += pattern.backward(self.action)
                if not clean:
                    pattern.spike()

        if clean:
            self.clean()
        return newLink

    def analysis(self):
        if self.countPatterns:
            return [self.countPatterns[0]]
        else:
            return []


def maxSpike(nodeList):
    maxspike = 0
    maxnode = Node('')
    for node in nodeList:
        node.calculate()
        if node.spike > maxspike:
            maxspike = node.spike
            maxnode = node

    return maxnode


def patternGenerlize(nodeList, PATTERNS, EDGES, patternNum=1, mode=0):
    if len(nodeList):
        for i in range(patternNum):
            if not mode:
                mode = random.randint(2, 3)
            patternNode = Node('Pattern' + str(len(PATTERNS)), 'Pattern', mode=mode)
            prob = 3 / len(nodeList)
            for node in nodeList:
                if random.random() < prob:
                    edge = Edge(node, patternNode)
                    EDGES[(node, patternNode)] = edge

            PATTERNS.append(patternNode)