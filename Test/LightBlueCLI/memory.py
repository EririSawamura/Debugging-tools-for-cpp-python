# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.2 (v3.6.2:5fd33b5, Jul  8 2017, 04:57:36) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\Users\ZHANGDorisXStudent\Desktop\LightBlue_NLTK\src\ChatBotDesign\memory.py
# Compiled at: 2018-10-06 16:57:20
from knowledge import *
from understanding import *
import json

class Memory:

    def __init__(self):
        self.ID = 0
        exclamatory = Node(' ! ', level=1)
        exclamatory.spikeTime = 1
        questionmark = Node(' ? ', level=1)
        questionmark.spikeTime = 1
        dot = Node(' . ', level=1)
        dot.spikeTime = 1
        exclamatory.actions[1] = 1
        dot.actions[2] = 1
        questionmark.actions[3] = 1
        self.patterns = {' ! ':exclamatory, 
         ' ? ':questionmark,  ' . ':dot}
        self.vocabulary = {'!':1,  '?':1,  '.':1}
        self.actions = ['', 'Hello, I am a chatbot.', 'Ok, I got it.', "I don't know."]
        self.connections = 3
        self.chatHistory = []

    #def reprJSON(self):
        #return dict(ID=self.ID, patterns=self.patterns, vocabulary=self.vocabulary, actions=self.actions, connections=self.connections, chatHistory=self.changeHistory)

    def testSpace(self):
        for i in range(2990):
            self.vocabulary[str(i)] = i

        for i in range(10000):
            action = Node(str(i))
            self.actions.append(action)

        for i in range(30000):
            pattern = Node(str(i))
            self.patterns[str(i)] = pattern

        for pattern in self.patterns:
            self.patterns[pattern].actions = {2:1, 
             3:5,  90:5,  7:10,  8:20,  9:300,  90:70}

    def testExtream(self):
        for i in range(2990):
            self.vocabulary[str(i)] = i

        for i in range(10000):
            action = Node(str(i))
            self.actions.append(action)

        for i in range(30000):
            pattern = Node(str(i))
            self.patterns[str(i)] = pattern

        for pattern in self.patterns:
            for i in range(100):
                self.patterns[pattern].actions[i] = 1

    def addHistory(self, item):
        self.chatHistory.append(item)

    def addConnections(self, newLink):
        self.connections += newLink

    def changeHistory(self, sentence):
        item = self.chatHistory[-1]
        item.outputSent = sentence
        item.mode = 'Change'

    def likeHistory(self):
        item = self.chatHistory[-1]
        item.like += 1

    def connectPatterns(self, unknown, known):
        newPatterns = {}
        for index in self.patterns:
            if unknown in index:
                continue
            newPatterns[index] = self.patterns[index]
            if known not in index:
                continue
            newIndex = index.replace(known, unknown)
            if newIndex != index:
                newPatterns[newIndex] = self.patterns[index]
                newPatterns[newIndex].index = newIndex
            print(newIndex)

        self.patterns = newPatterns