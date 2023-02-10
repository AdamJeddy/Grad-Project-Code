# ASL Gloss to English Translator <!-- omit in toc -->

This is a script for translating American Sign Language (ASL) gloss to English. It uses a neural machine translation (NMT) model built with the Keras library. The NMT model is a combination of an encoder and a decoder, both implemented using Long Short-Term Memory (LSTM) networks. The script loads pre-trained model weights and perform inference to translate a given ASL gloss sentence.

## Table of Contents <!-- omit in toc -->

- [Prerequisites](#prerequisites)
- [File descriptions](#file-descriptions)
- [How it works](#how-it-works)
- [How to use](#how-to-use)


## Prerequisites

- Python 3.x
- Keras
- Numpy

## File descriptions

- `NLP_Model.py`: The main code file that contains the code to translate ASL gloss to English.
- `myVars.txt`: The file that contains the variables required for the code to run.
- `nmt_weights_v4.h5`: The trained model weights file.

## How it works

When the script is run, it will prompt the user to input an ASL gloss sentence. The input sentence is then processed by the encoder to obtain the thought vector, which is then passed to the decoder to generate the translated English sentence. The generated sentence is then printed to the console.

## How to use

1. Clone the repository to your local machine or have the 3 files downloaded mentioned under [File descriptions](#file-descriptions)

    ``` bash
    https://github.com/AdamJeddy/Grad-Project-Stuff.git
    ```

2. Navigate to the directory where the code is located. (if downloaded separately then make sure all the files are in the same directory)

    ``` bash
    cd Scripts/Model
    ```

3. If you want to use the terminal make sure python is added to PATH variable

    ``` bash
    python NLP_Model.py "[ASl text you want to translate]"
    ```

4. There is a loop that allows you to keep translating, if you want to exit/end the program just type `exit`

    ``` bash
    Input ASL sentence: [Enter ASl text you want to translate]
    # or 
    Input ASL sentence: exit # to exit/end the program
    ```

___
**Note**: The model's performance may be improved by fine-tuning the model on a larger and more diverse training dataset, or by using a more advanced NMT architecture (which will increase processing time). Additionally, the script uses a greedy decoding strategy, meaning that it always chooses the most likely English word at each time step without considering the full context of the sentence. More sophisticated decoding strategies, such as beam search, could be implemented to generate more accurate translations.
