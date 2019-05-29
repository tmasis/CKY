import sys
import math
import random
from collections import defaultdict
from nltk.tree import Tree

def cky(sentence, grammar):
    #split sentence into words
    sentence = sentence.split()
    #instantiate chart
    chart = []
    for each in range(len(sentence)):
        chart.append([])
        for each2 in range(len(sentence)):
            chart[each].append([])

    for j in range(len(sentence)):
        #insert tags/terminals
        n = []
        n.append(sentence[j])
        for each in grammar[tuple(n[0:])]:
            chart[j][j].append((each[1], each[0], sentence[j]))
            #all rows above diagonal splits b/n i and j
            for i in range(j-1, -1, -1):
                for k in range(i+1, j+1):
                    #add any rules matching [i][j] -> [i][k-1] + [k][j]
                    if (not chart[i][k-1]) or (not chart[k][j]):
                        continue
                    node1length = len(chart[i][k-1])
                    node2length = len(chart[k][j])
                    #loop through each tuple in each cell
                    for num1 in range(node1length):
                        for num2 in range(node2length):
                            node1 = chart[i][k-1][num1][1]
                            node2 = chart[k][j][num2][1]
                            node = [node1, node2]
                            for rule in grammar[tuple(node)]:
                                chart[i][j].append((rule[1]+
                                                    chart[i][k-1][num1][0]+
                                                    chart[k][j][num2][0],
                                                    rule[0], [i, k-1, num1, k, j, num2])) 

    #return completed chart
    return chart


def printTree(chart):
    #if there is no parse in the last cell that has ROOT in it, then there is no parse
    isThereParse = False
    if not chart[0][len(chart)-1]:
        pass
    else:
        for each in chart[0][len(chart)-1]:
            if each[1] == 'ROOT':
                isThereParse = True
        
    if not isThereParse:
        print "No Parse!"
    else:
        #for each complete parse
        n = 1
        #if the parses are the exact same, then skip
        skip = False
        for each in chart[0][len(chart)-1]:
            for num in range(0, n-1):
                if bracket(chart, 0, len(chart)-1, n-1) == bracket(chart, 0, len(chart)-1, num):
                    skip = True
            if skip:
                continue
            if each[1] == 'ROOT':
                #print weight
                print "Tree " + str(n) + " weight: \t" + str(each[0])
                #print parse
                print "Tree " + str(n) + " parse:" + bracket(chart, 0, len(chart)-1, n-1)
                n += 1

def bracket(chart, i, j, n):
    result = ""
    node = chart[i][j][n]

    #if the backpointer is a string, then it is a terminal node
    if type(node[2]) == str:
        result += "( " + node[1] + " " + node[2] + " )"
    #else, it is a non-terminal and should be recursed
    else:
        result += "( " + node[1] + " " + bracket(chart,
                                           node[2][0],
                                           node[2][1],
                                           node[2][2]) + " " + bracket(chart,
                                                                           node[2][3],
                                                                           node[2][4], node[2][5]) + " )" 

    return result


def main():
    #read grammar
    grammarfile = sys.argv[1]
    f = open(grammarfile, "r")
    grammar = defaultdict(lambda:[])
    f = open(grammarfile, "r")
    for line in f:
        line = line.strip() #strip whitespace
        if line == '':
            continue
        fields = line.split()
        p = float(fields[0])
        #lhs is list with lefthand side and rule weight
        lhs = [fields[1], p]
        rhs = fields[2:]
        #for each rhs, there is a list of lhs lists
        grammar[tuple(rhs)].extend ( [lhs] )
            
    #read and split sentence corpus into individual sentences
    sentencesfile = sys.argv[2]
    s = open(sentencesfile, "r")
    sentences = []
    for line in s:
        sentences.append(line)
        
    #for each sentence in the corpus, run CKY parser
    for each in sentences:
        print "PARSING: : \t" + each
        printTree(cky(each, grammar))


if __name__ == "__main__":
    main()
