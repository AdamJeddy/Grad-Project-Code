from keras.layers import Input, LSTM, Embedding, Dense
from keras.models import Model
import numpy as np
import time
import ast
import sys

# from functions import *

class colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    UNDERLINE_GREEN = '\033[4m' + '\033[92m'

def read_list_from_file():
    inputFile = open( "myVars.txt", "r")
    lines = inputFile.readlines()

    objects = []
    for line in lines:
        objects.append(ast.literal_eval(line))
    
    return objects[0][0], objects[0][1], objects[0][2], objects[0][3], objects[0][4], objects[0][5]

# get the start time
st_final = time.time()
st = time.time()

max_length_src, max_length_tar, num_decoder_tokens, input_token_index, target_token_index, reverse_target_char_index = read_list_from_file()

print(colors.UNDERLINE_GREEN + 'Importing Variables:' + colors.ENDC, round(time.time() - st, 2), 'seconds')
st = time.time()

latent_dim = 50

# Encoder
encoder_inputs = Input(shape=(None,))
enc_emb =  Embedding(2036, latent_dim, mask_zero = True)(encoder_inputs)
encoder_lstm = LSTM(latent_dim, return_state=True)
encoder_outputs, state_h, state_c = encoder_lstm(enc_emb)
# We discard `encoder_outputs` and only keep the states.
encoder_states = [state_h, state_c]

# Set up the decoder, using `encoder_states` as initial state.
decoder_inputs = Input(shape=(None,))
dec_emb_layer = Embedding(2086, latent_dim, mask_zero = True)
dec_emb = dec_emb_layer(decoder_inputs)

'''
We set up our decoder to return full output sequences, and to return internal states as well. 
We don't use the return states in the training model, but we will use them in inference.
'''
decoder_lstm = LSTM(latent_dim, return_sequences=True, return_state=True)
decoder_outputs, _, _ = decoder_lstm(dec_emb, initial_state=encoder_states)
decoder_dense = Dense(2086, activation='softmax')
decoder_outputs = decoder_dense(decoder_outputs)
# Define the model that will turn `encoder_input_data` & `decoder_input_data` into `decoder_target_data`
model = Model([encoder_inputs, decoder_inputs], decoder_outputs)

print(colors.UNDERLINE_GREEN + 'Setting up Model:' + colors.ENDC, round(time.time() - st, 2), 'seconds')
st = time.time()

model.load_weights('nmt_weights_v4.h5')

print(colors.UNDERLINE_GREEN + 'Loading Weights:' + colors.ENDC, round(time.time() - st, 2), 'seconds')
st = time.time()

### INFERENCING ###
encoder_model = Model(encoder_inputs, encoder_states) # Encode the input sequence to get the "thought vectors"

# Decoder setup - Below tensors will hold the states of the previous time step
decoder_state_input_h = Input(shape=(latent_dim,))
decoder_state_input_c = Input(shape=(latent_dim,))
decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
dec_emb2 = dec_emb_layer(decoder_inputs) # Get the embeddings of the decoder sequence

# To predict the next word in the sequence, set the initial states to the states from the previous time step
decoder_outputs2, state_h2, state_c2 = decoder_lstm(dec_emb2, initial_state=decoder_states_inputs)
decoder_states2 = [state_h2, state_c2]
decoder_outputs2 = decoder_dense(decoder_outputs2) # A dense softmax layer to generate prob dist. over the target vocabulary

# Final decoder model
decoder_model = Model(
    [decoder_inputs] + decoder_states_inputs,
    [decoder_outputs2] + decoder_states2)

print(colors.UNDERLINE_GREEN + 'Setting up Decoder:' + colors.ENDC, round(time.time() - st, 2), 'seconds')
st = time.time()

# Reverse-lookup token index to decode sequences back to something readable.
def decode_sequence(input_text):
    encoder_input_data = np.zeros((1, max_length_src), dtype='float32')

    for i, input_text in enumerate([input_text]):
        # print(colors.WARNING + "i:", i, " | input_text: ", input_text, "" + colors.ENDC)
        for t, word in enumerate(input_text.split()):
            encoder_input_data[i, t] = input_token_index[word]
    
    states_value = encoder_model.predict(encoder_input_data)
    
    target_seq = np.zeros((1, 1))
    target_seq[0, 0] = target_token_index['START_']
    stop_condition = False
    decoded_sentence = ''

    while not stop_condition:
        output_tokens, h, c = decoder_model.predict([target_seq] + states_value)
        sampled_token_index = np.argmax(output_tokens[0, -1, :])
        sampled_char = reverse_target_char_index[sampled_token_index]
        decoded_sentence += ' ' + sampled_char
        
        if (sampled_char == '_END' or
           len(decoded_sentence) > 50):
            stop_condition = True
        
        target_seq = np.zeros((1, 1))
        target_seq[0, 0] = sampled_token_index
        states_value = [h, c]
    
    return decoded_sentence[:-4]

# Add a for loop to run this on multiple sentences

if len(sys.argv) > 1:
    input_text = sys.argv[1].lower()
else:
    print(colors.RED + colors.BOLD + 'No input sentence provided. Using default sentence.' + colors.ENDC)
    input_text = "you live where".lower()

decoded_sentence = decode_sequence(input_text)
print(colors.WARNING + '\nInput ASL sentence:' + colors.ENDC, input_text)
print(colors.WARNING + 'Predicted English Translation:' + colors.ENDC, decoded_sentence)

print(colors.UNDERLINE_GREEN + 'Decoding Sequence:' + colors.ENDC, round(time.time() - st, 2), 'seconds')

while True:
    input_text = input(colors.WARNING + 'Input ASL sentence: ' + colors.ENDC)
    st = time.time()
    input_text = input_text.lower()
    if input_text == 'exit':
        break
    decoded_sentence = decode_sequence(input_text)
    print(colors.WARNING + 'Predicted English Translation:' + colors.ENDC, decoded_sentence)
    print(colors.UNDERLINE_GREEN + 'Decoding Sequence:' + colors.ENDC, round(time.time() - st, 2), 'seconds')


print(colors.UNDERLINE_GREEN + 'Total Execution time:' + colors.ENDC, round(time.time() - st_final, 2), 'seconds')