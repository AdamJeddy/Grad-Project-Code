import string
import codecs

file1 = open('English_ASL.txt', 'r', encoding="UTF-8")
file2 = open('AllSentences.txt', 'w')

allSentences = []
for line in file1: # for removing all the \n and spaces in the file
    if line != '\n':
        str = line.replace('\n', '')
        allSentences.append(str) # storing all the sentences and their gloss in a list

for i in range(0, len(allSentences)):
    if(i <= (len(allSentences) - 2)):
        sentence = allSentences[i] + ',' + ' ' + allSentences[i + 1] + '\n'
        file2.write(sentence)
        i = i+1
