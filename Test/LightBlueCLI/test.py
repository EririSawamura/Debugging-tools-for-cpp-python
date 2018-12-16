from chatbot import Chatbot
from operator import attrgetter
import time
import json

class MyEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__ 

class answer():
    def __init__(self, answer, spikeTime, probability, index):
        self.answer = answer
        self.spikeTime = spikeTime
        self.probability = probability
        self.index = index

class info():
    def __init__(self, pattern, level, spikeTime):
        self.pattern = pattern
        self.answerList = []
        self.level = level
        self.spikeTime = spikeTime

    def answerAppend(self, answerstr, spikeTime, probability):
        self.answerList.append(answer(answerstr, spikeTime, probability, len(self.answerList)))

    def sort(self):
        self.answerList.sort(key = attrgetter('probability', 'index'), reverse = True)



def patternAnswer(chatbot):
    f = open("PatternAnswer.csv", "w")
    js = open("pattern.txt", "w")
    valid = open("patternpos.txt", "w")
    patterns = chatbot.memory.patterns
    actions = chatbot.memory.actions
    for index in set(patterns):
        pattern = patterns[index]
        level = pattern.level
        spiketime = pattern.spikeTime
        information = info(pattern.index, level, spiketime)
        validinfo = info(pattern.index, level, spiketime)
        maxstrength = 0
        actionIndex = []
        for action in pattern.actions:
            if pattern in chatbot.workMemory.activePatterns:
                strength = (pattern.actions[action] + 1) / (spiketime)
            else:
                strength = (pattern.actions[action]) / (spiketime)
            information.answerAppend(actions[action], pattern.actions[action], strength)
            if strength > maxstrength:
                actionIndex = [action]
                maxstrength = strength
                validinfo.answerList = []
                if strength >= 0.2:
                    validinfo.answerAppend(actions[action], pattern.actions[action], strength)
            elif strength == maxstrength:
                actionIndex.append(action)
                if strength >= 0.2:
                    validinfo.answerAppend(actions[action], pattern.actions[action], strength)
        information.sort()
        js.write(json.dumps(information, cls = MyEncoder, indent=4) + "\n")
        if validinfo.answerList != None and len(validinfo.answerList) > 1 and len(information.answerList) > 1:
            valid.write(json.dumps(validinfo, cls = MyEncoder, indent=4) + "\n")
        #print(pattern.index, maxstrength, actionIndex)
        if actionIndex == None or len(actionIndex) == 0:
            f.write(pattern.index + ',\n')
            continue
        answerindex = actionIndex[-1]
        finalAnswer = actions[answerindex]
        f.write('"' + pattern.index + '","' + finalAnswer + '","')
        for i in range(1, 11, 1):
            if i >= level:
                tmp = maxstrength / i
            else:
                tmp = 0
            f.write(str(tmp) + '","')
        f.write('"\n')
    f.close()
    js.close()
    valid.close()



def main():
    chatbot = Chatbot()
    while True:
        file=open("view.txt", "w")
        MyEncoder().encode(chatbot)
        file.write(json.dumps(chatbot, cls=MyEncoder, indent=4))
        file.close()

        file=open("AnswerList.txt", "w")
        i = 0
        for answer in chatbot.memory.actions:
            file.write(str(i) + ". "+ answer + "\n")
            i = i + 1
        file.close()

        timestamp = time.strftime('%d %b %H:%M:%S', time.localtime())
        question = input(timestamp + "\tYou: ")
        if question == 'E':
            break
        elif question == 'I':
            filename = input("Please input the filename: ")
            chatbot.import_file(filename)
        elif question == 'X':
            filepath = input("Please input the path")
            filepath += "history.csv"
            chatbot.export_history(filepath)
        else:
            answer, outtime = chatbot.chat(question, timestamp)
            print(outtime + "\tChatbot: " + answer)
            #print("I am safe: ", chatbot.workMemory.action)
            while True:
                operation = input("Your operation: ")
                if operation == 'E' or operation == 'e':
                    #print("I am safe: ", chatbot.workMemory.action)
                    print("\n\n")
                    break
                if operation == 'C' or operation == 'c':
                    change = input("New answer: ")
                    chatbot.change(change)
                if operation == 'L' or operation == 'l':
                    chatbot.like()
                if operation == 'A' or operation == 'a':
                    print(chatbot.analysis())
        #print("I am safe: ", chatbot.workMemory.action)
        patternAnswer(chatbot)
        #print("fuck you: ", chatbot.workMemory.action)

main()
        
