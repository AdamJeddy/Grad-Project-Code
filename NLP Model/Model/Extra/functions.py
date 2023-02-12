import numpy as np
import re
import string
import ast

def preprocess_data(df):
    replacements = {'1': " one ", '2':" two ", '3':" three ", '4':" four ", '5':" five ", '6':" six ", '7':" seven ", '8':" eight ", '9':" nine ", '0':" zero "}
    df['English'] = df['English'].apply(lambda x: re.sub('(\d)', lambda m: replacements[m.group()], x))
    df['ASL Gloss'] = df['ASL Gloss'].apply(lambda x: re.sub('(\d)', lambda m: replacements[m.group()], x))
    df['English'] = df['English'].apply(lambda x: x.strip())
    df['ASL Gloss'] = df['ASL Gloss'].apply(lambda x: x.strip())
    df['English'] = df['English'].apply(lambda x: x.lower())
    df['ASL Gloss'] = df['ASL Gloss'].apply (lambda x: x.lower())
    df['English'] = df['English'].apply(lambda x: x.replace('  ', ' '))
    df['ASL Gloss'] = df['ASL Gloss'].apply(lambda x: x.replace('  ', ' '))
    df['English'] = df['English'].apply(lambda x: ''.join (ch for ch in x if ch not in set(string.punctuation)))
    df['ASL Gloss'] = df['ASL Gloss'].apply(lambda x: ''.join (ch for ch in x if ch not in set(string.punctuation)))
    df['English'] = df['English'].apply(lambda x : 'START_ ' + x + ' _END')

    return df

def get_variables(df):
    # Vocabulary of English
    all_eng_words = set()
    for eng in df['English']:
        for word in eng.split():
            if word not in all_eng_words:
                all_eng_words.add(word)

    # Vocabulary of ASL 
    all_ASL_words = set()
    for asl in df['ASL Gloss']:
        for word in asl.split():
            if word not in all_ASL_words:
                all_ASL_words.add(word)

    # Max Length of source sequence and target sequence
    length_list=[]
    for l in df ['English']:
        length_list.append(len(l.split(' ')))
    max_length_tar = np.max(length_list)
    print("Max length target: ", max_length_tar)

    length_list=[]
    for l in df ['ASL Gloss']:
        length_list.append(len(l.split(' ')))
    max_length_src = np.max(length_list)
    print("Max length sorce: ", max_length_src)

    input_words = sorted(list(all_ASL_words))
    target_words = sorted(list(all_eng_words))

    # Calculate Vocab size for both source and target
    #num_encoder_tokens = len(all_ASL_words) + 1
    num_decoder_tokens = len(all_eng_words) + 2

    # Create word to token dictionary for both source and target
    input_token_index = dict([(word, i+1) for i, word in enumerate(input_words)])
    target_token_index = dict([(word, i+1) for i, word in enumerate(target_words)])

    # Create token to word dictionary for both source and target
    reverse_target_char_index = dict((i, word) for word, i in target_token_index.items())

    return max_length_src, max_length_tar, num_decoder_tokens, input_token_index, target_token_index, reverse_target_char_index

def write_list_to_file(var_list):
    outputFile = open( "../myVars.txt", "w")
    outputFile.write(str(var_list))
    outputFile.flush()
    outputFile.close()

def read_list_from_file():
    inputFile = open( "../myVars.txt", "r")
    lines = inputFile.readlines()

    objects = []
    for line in lines:
        objects.append(ast.literal_eval(line))
    
    return objects[0][0], objects[0][1], objects[0][2], objects[0][3], objects[0][4], objects[0][5]