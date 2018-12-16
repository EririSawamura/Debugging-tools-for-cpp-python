# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.2 (v3.6.2:5fd33b5, Jul  8 2017, 04:57:36) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\Users\ZHANGDorisXStudent\Desktop\LightBlue_NLTK\src\ChatBotDesign\chatbot.py
# Compiled at: 2018-10-09 06:51:54
from memory import Memory
from understanding import *
import json
import time, csv

class Chatbot:

    def __init__(self):
        self.identity = generate_random_str()
        self.memory = Memory()
        self.workMemory = WorkMemory()
        self.specialMode = 0
        self.unknownWord = None
        self.state = 0
        self.lastInputSentence = ''


    #def reprJSON(self):
        #return dict(identity=self.identity, memory=self.memory, workMemory=self.workMemory, specialMode=self.specialMode, unknownWord=self.unknownWord, state=self.state, lastInputSentence=self.lastInputSentence)

    def copy(self, other):
        self.identity = other.identity
        self.memory = other.memory
        self.workMemory = other.workMemory
        self.specialMode = other.specialMode
        self.unknownWord = other.unknownWord
        self.state = other.state
        self.lastInputSentence = other.lastInputSentence

    def chat(self, inputSent, timeStamp):
        write_memory = True
        mode = 'Retrieval'
        if self.specialMode == 1:
            inputList = sentenceFilter(inputSent)
            oldPattern = conbineWords(inputList)
            self.memory.connectPatterns(self.unknownWord.index, oldPattern)
            inputSent = self.lastInputSentence
            self.workMemory.clean()
        if self.specialMode == 2:
            self.workMemory.clean()
        #print("[may be change]: ", self.workMemory.action)
        if self.workMemory.action:
            if not self.specialMode:
                self.memory.addConnections(self.workMemory.backward())
        self.lastInputSentence = inputSent
        inputList = sentenceFilter(inputSent)
        self.specialMode = 0
        print('[INPUT LIST]:', inputList)
        new_words = updateVocabulary(inputList, self.memory.vocabulary)
        print("[NEW WORDS]:", new_words)
        self.unknownWord = self.workMemory.spikePatterns(inputList, self.memory.patterns, level=10)
        print("[UNKNOWNWORD]:", self.unknownWord)
        actionIndex = self.workMemory.getAction() 
        print('[ACTIONINDEX]:', actionIndex)
        if actionIndex != None:
            for i in actionIndex:
                print('[POSSIBLE OUTPUT]', self.memory.actions[i])

        outputSent = ""
        if self.unknownWord:
            self.specialMode = 1
            mode = 'Question'
            outputSent = 'What does' + self.unknownWord.index + 'mean?'
        else:
            if actionIndex == None or len(actionIndex) == 0:
                outputSent = "I don't know how to answer."
                self.specialMode = 2
                mode = 'Confused'
                print("pass1")
            else:
                if len(actionIndex) >= 1:
                    print("[CHATSTRENGTH]: " , self.workMemory.maxStrength)
                    if self.workMemory.maxStrength < 0.2:
                        print("[CHATSTRENGTH]: " , self.workMemory.maxStrength)
                        outputSent = "I don't know how to answer."
                        self.specialMode = 2
                        mode = 'Confused'
                    outputSent = self.memory.actions[actionIndex[-1]]
        #            print("[hhda]: ", actionIndex[-1], " ", outputSent)
                    self.memory.action = actionIndex[-1]
        #            print("[mmda]: ", actionIndex[-1], " ", self.memory.action)
        outputTime = time.strftime('%d %b %H:%M:%S', time.localtime())
        #print("[may be change]: ", self.workMemory.action)
        if write_memory:
            self.memory.addHistory(ChatItem(inputSent, timeStamp, outputSent, outputTime, mode))
            print("pass2")
        #print("[may be change]: ", self.workMemory.action)
        # print(outputSent)
        return (outputSent, outputTime)

    def change(self, inputSent):
        index = 0
        inputSent_l = inputSent.lower()
        for i in range(len(self.memory.actions)):
            if self.memory.actions[i].lower() == inputSent_l:
                index = i
                self.memory.actions[i] = inputSent
                break

        if not index:
            index = len(self.memory.actions)
            self.memory.actions.append(inputSent)
        self.workMemory.action = index
        self.memory.changeHistory(inputSent)
        self.specialMode = 0

    def like(self):
        if self.workMemory.action:
            self.memory.addConnections(self.workMemory.backward(clean=False))
            self.memory.likeHistory()

    def currentDialogs(self):
        dialog = []
        l = len(self.memory.chatHistory)
        index = max(l - 20, 0)
        for item in self.memory.chatHistory[index:]:
            dialog.append([item.inputSent, item.inputTime, item.outputSent, item.outputTime])

        return dialog

    def getVocabulary(self):
        voca = []
        for word in self.memory.vocabulary:
            voca.append((word, self.memory.vocabulary[word]))

        return voca

    def getStatus(self):
        return (
         len(self.memory.vocabulary), len(self.memory.patterns), len(self.memory.actions), self.memory.connections)

    def analysis(self):
        if not self.workMemory.action:
            return "I don't know at all the meaning of this sentence."
        else:
            patterns = self.workMemory.analysis()
            reason = 'Based on past experience, I think this is a suitable reply for the sentence containing:'
            for pattern in patterns:
                reason += ' '
                reason += "'"
                reason += pattern
                reason += "'"

            reason += '.'
            return reason

    def import_file(self, filename):
        correct = 0
        f = open(filename)
        fi = open("similar.txt", "w")
        input = f.readline().strip()
        output = f.readline().strip()
        count = 0
        while input:
            if output:
                if count < 10001:
                    input = sentencePreprocessing(input)
                    output = sentencePreprocessing(output)
                    print("[Question]: " + input)
                    print("[Answer]: " + output)
                    timeStamp = time.strftime('%d %b %H:%M:%S', time.localtime())
                    answer, _ = self.chat(input, timeStamp)
                    if output == answer:
                        correct = correct + 1
                        fi.write(input + "\n")
                    self.change(output)
                    input = f.readline().strip()
                    output = f.readline().strip()
                    count += 1
                else:
                    print(count)
                    break

        f.close()
        fi.close()
        print("[CORRECT ANSWER]: ", correct)

    def export_history(self, filepath):
        try:
            csvout = open(filepath, 'w')
            txtout = open(filepath[:-3] + 'txt', 'w')
            csv_writer = csv.writer(csvout)
            temp = ['User', 'Chatbot', 'State', 'Liked']
            csv_writer.writerow(temp)
            for item in self.memory.chatHistory:
                csv_writer.writerow([item.inputSent, item.outputSent, item.mode, item.like])
                txtout.write(item.inputSent + '\n' + item.outputSent + '\n')

            csvout.close()
            txtout.close()
            vocout = open(filepath[:-4] + '(vocabulary)' + '.csv', 'w')
            csv_writer = csv.writer(vocout)
            csv_writer.writerow(['Word', 'Count'])
            for word in self.memory.vocabulary:
                csv_writer.writerow([word, self.memory.vocabulary[word]])

            vocout.close()
        except:
            print('Export failed.')