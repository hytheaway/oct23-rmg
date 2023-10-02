import numpy as np
from scipy.io import wavfile
import random

# given desired length of time, sample rate, and filename, generate a sine wave and write it to a wav file. 
def generate_note(seconds, sample_rate, filename):
    # choose a random frequency within the key
    fs = random.choice([329.628, 369.994, 391.995, 440, 493.88, 523.25, 587.33])

    # flip a 3 sided coin (lol)
    # if 0, do nothing (keeps the frequency at its fundamental)
    # if 1, double the chosen frequency (place it one octave up)
    # if 2, halve the chosen frequency (place it one octave lower)
    coin_flip = random.randint(0,2)
    if coin_flip == 1:
        fs *= 2
    elif coin_flip == 2:
        fs = fs / 2
    
    # determine how long (how many samples) should be in the resulting audio file
    t = np.linspace(0, seconds, (seconds * sample_rate), endpoint=False)

    # create a numpy array object with the values provided
    note = np.iinfo(np.int16).max * np.sin(2 * np.pi * fs * t)

    # convert all values in the numpy array to 16 bit integers and use them as the basis for writing the wav file
    wavfile.write(str(filename)+'.wav', sample_rate, note.astype(np.int16))