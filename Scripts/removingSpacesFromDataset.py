import string
import codecs
import re # import regex for removing punctuations if needed

file1 = open('English_ASL.txt', 'r', encoding="UTF-8")
file2 = open('Dataset.txt', 'w')

allSentences = []
for line in file1: # for removing all the \n and spaces in the file
    if line != '\n':
        str_initial = line.replace('\n', '')
        str_final = str_initial.translate(str.maketrans('', '', ',')) # for removing punctuations from a sentence
        allSentences.append(str_final) # storing all the sentences and their gloss in a list

for i in range(0,len(allSentences),2):
    if i <= (len(allSentences) - 2):
        sentence = allSentences[i] + ',' + ' ' + allSentences[i + 1] + '\n'
        file2.write(sentence)

# another way of removing punctuations:
# str_final = re.sub(r'[^\w\s]', '', str_initial)  # will select anything that isnt a word or a whitespace and replace that with a ''
