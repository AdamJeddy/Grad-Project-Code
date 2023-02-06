from sklearn.model_selection import train_test_split
from keras.layers import Input, LSTM, Embedding, Dense
from keras.models import Model
import tensorflow as tf
import pandas as pd
import time

from sklearn.utils import shuffle
from functions import *

class bcolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    UNDERLINE_OKGREEN = '\033[4m' + '\033[92m'

df = pd.read_csv('..\..\Data\Double_Dataset_EnglishToGloss.csv')

# get the start time
st_final = time.time()
st = time.time()

df = preprocess_data(df)

print(bcolors.UNDERLINE_OKGREEN + 'Importing and Preprocess Data Execution time:' + bcolors.ENDC, round(time.time() - st, 2), 'seconds\n')
st = time.time()

"""
max_length_src, max_length_tar, num_decoder_tokens, input_token_index, target_token_index, reverse_target_char_index= get_variables(df)
var_list = [max_length_src, max_length_tar, num_decoder_tokens, input_token_index, target_token_index, reverse_target_char_index]
write_list_to_file(var_list)
"""

max_length_src, max_length_tar, num_decoder_tokens, input_token_index, target_token_index, reverse_target_char_index = read_list_from_file()

# Train - Test Split
X, y = df['ASL Gloss'], df['English']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1)

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
We set up our decoder to return full output sequences,
and to return internal states as well. We don't use the
return states in the training model, but we will use them in inference.
'''
decoder_lstm = LSTM(latent_dim, return_sequences=True, return_state=True)
decoder_outputs, _, _ = decoder_lstm(dec_emb, initial_state=encoder_states)

# Use a softmax to generate a probability distribution over the target vocabulary for each time step
decoder_dense = Dense(2086, activation='softmax')
decoder_outputs = decoder_dense(decoder_outputs)

# Define the model that will turn
# `encoder_input_data` & `decoder_input_data` into `decoder_target_data`
model = Model([encoder_inputs, decoder_inputs], decoder_outputs)


model.load_weights('nmt_weights_v4.h5')

### INFERENCING ###
# Encode the input sequence to get the "thought vectors"
encoder_model = Model(encoder_inputs, encoder_states)

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


def generate_batch(X = X_train, y = y_train, batch_size = 128):
    ''' Generate a batch of data '''
    while True:
        for j in range(0, len(X), batch_size):
            encoder_input_data = np.zeros((batch_size, max_length_src),dtype='float32')
            decoder_input_data = np.zeros((batch_size, max_length_tar),dtype='float32')
            decoder_target_data = np.zeros((batch_size, max_length_tar, num_decoder_tokens),dtype='float32')
            for i, (input_text, target_text) in enumerate(zip(X.iloc[j:j+batch_size], y.iloc[j:j+batch_size])):
                for t, word in enumerate(input_text.split()):
                    encoder_input_data[i, t] = input_token_index[word] # encoder input seq
                for t, word in enumerate(target_text.split()):
                    if t < len(target_text.split())-1:
                        decoder_input_data[i, t] = target_token_index[word] # decoder input seq
                    if t > 0:
                        # decoder target sequence (one hot encoded)
                        # does not include the START_ token
                        # Offset by one timestep
                        decoder_target_data[i, t - 1, target_token_index[word]] = 1.
            yield([encoder_input_data, decoder_input_data], decoder_target_data)

def decode_sequence(input_seq):
    # Encode the input as state vectors.
    states_value = encoder_model.predict(input_seq)
    # Generate empty target sequence of length 1.
    target_seq = np.zeros((1,1))
    # Populate the first character of target sequence with the start character.
    target_seq[0, 0] = target_token_index['START_']

    # Sampling loop for a batch of sequences (to simplify, here we assume a batch of size 1).
    stop_condition = False
    decoded_sentence = ''
    
    while not stop_condition:
        output_tokens, h, c = decoder_model.predict([target_seq] + states_value)

        # Sample a token
        sampled_token_index = np.argmax(output_tokens[0, -1, :])
        sampled_char = reverse_target_char_index[sampled_token_index]
        decoded_sentence += ' '+sampled_char

        # Exit condition: either hit max length or find stop character.
        if (sampled_char == '_END' or
           len(decoded_sentence) > 50):
            stop_condition = True

        # Update the target sequence (of length 1).
        target_seq = np.zeros((1,1))
        target_seq[0, 0] = sampled_token_index

        # Update states
        states_value = [h, c]

    return decoded_sentence

train_gen = generate_batch(X_train, y_train, batch_size = 1)
k=-1

k+=1
(input_seq, actual_output), _ = next(train_gen)
# print("Input Sequence", input_seq)
decoded_sentence = decode_sequence(input_seq)
print('Input ASL sentence:', X_train.iloc[k:k+1].values[0])
print('Actual English Translation:', y_train.iloc[k:k+1].values[0][6:-4])
print('Predicted English Translation:', decoded_sentence[:-4])

"""
print("\n\n")

print('Input ASL sentence:', "i want to go to the bathroom")
print('Actual English Translation:', )
print('Predicted English Translation:', decode_sequence("START_ i want to go to the bathroom _END"))
"""

print(bcolors.UNDERLINE_OKGREEN + '\nTotal Execution time:' + bcolors.ENDC, round(time.time() - st_final, 2), 'seconds')