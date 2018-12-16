# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.2 (v3.6.2:5fd33b5, Jul  8 2017, 04:57:36) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\Users\ZHANGDorisXStudent\Desktop\LightBlue_NLTK\src\ChatBotDesign\understanding.py
# Compiled at: 2018-09-18 14:32:08
from knowledge import *
from pre_processing import *
import time

def spikeVocabulary(list, ENTITIES, VOCABULARY, EDGES, WORKMEMORY):
    level0 = []
    for word in list:
        if word[0] == '#':
            word = word[1:]
            if word not in ENTITIES:
                ENTITIES[word] = Node(word)
            if word not in VOCABULARY:
                VOCABULARY[word] = Node(word)
                initiator = VOCABULARY[word]
                target = ENTITIES[word]
                edge = Edge(initiator, target, default=False)
                EDGES[(initiator, target)] = edge
                initiator.entities.append(edge)
            else:
                if word not in VOCABULARY:
                    VOCABULARY[word] = Node(word)
            node = VOCABULARY[word]
            node.stimulate()
            node.link()
            level0.append(node)

    WORKMEMORY.addLevel(level0)


def updateVocabulary(list, vocabulary):
    new_words = []
    for word in list:
        if word not in vocabulary:
            vocabulary[word] = 1
            new_words.append(word)
        else:
            vocabulary[word] += 1

    return new_words


def buildLink(fromList, toList, EDGES, stimulate=False):
    for initiator in fromList:
        for target in toList:
            if initiator != target:
                if target.property != 'Vocabulary':
                    edge = Edge(initiator, target)
                    if stimulate:
                        edge.stimulate()
                    EDGES.append(edge)


def chat(inputSent, memory):
    if memory.WORKMEMORY.action:
        buildLink(memory.WORKMEMORY.visitedList, [memory.WORKMEMORY.action], memory.EDGES)
        memory.WORKMEMORY.action.backward()
        memory.WORKMEMORY.clean()
    inputList = sentenceFilter(inputSent)
    spikeVocabulary(inputList, memory.ENTITIES, memory.VOCABULARY, memory.EDGES, memory.WORKMEMORY)
    memory.WORKMEMORY.evolve()
    patternGenerlize(memory.WORKMEMORY.visitedList, memory.PATTERNS, memory.EDGES)
    memory.WORKMEMORY.spikeCalculation(memory.INTENTIONS)
    memory.WORKMEMORY.action = maxSpike(memory.INTENTIONS)
    return memory.WORKMEMORY.action.index


def change(inputSent, memory):
    action = Node(inputSent, 'Intention', mode=1)
    memory.INTENTIONS.append(action)
    memory.WORKMEMORY.action = action


def conbine_actions(a1, a2, EDGES, INTENTIONS):
    for edge in a2.preLinks:
        initiator = edge.initiator
        if (initiator, a1) in EDGES:
            e = EDGES[(initiator, a1)]
            e.stimulateTimes += edge.stimulateTimes
            initiator.postLinks.remove(edge)
        else:
            edge.target = a1
            a1.preLinks.append(edge)
            EDGES[(initiator, a1)] = edge
        EDGES.pop((initiator, a2))

    INTENTIONS.remove(a2)


def ruminate(memory):
    i = 0
    while i < len(memory.INTENTIONS):
        a1 = memory.INTENTIONS[i]
        j = i + 1
        while j < len(memory.INTENTIONS):
            a2 = memory.INTENTIONS[j]
            if a1.index.lower() == a2.index.lower():
                conbine_actions(a1, a2, memory.EDGES, memory.INTENTIONS)
            j += 1

        i += 1


def import_file(filename, memory):
    f = open(filename)
    input = f.readline().strip()
    output = f.readline().strip()
    while input:
        chat(input, memory)
        change(output, memory)
        input = f.readline().strip()
        output = f.readline().strip()

    f.close()