import numpy as np
from scipy.io import wavfile
import random

def generate_note(seconds, sample_rate, filename):
    fs = random.choice([329.628, 369.994, 391.995, 440, 493.88, 523.25, 587.33])
    coin_flip = random.randint(0,2)
    if coin_flip == 1:
        fs *= 2
    elif coin_flip == 2:
        fs = fs / 2
    t = np.linspace(0, seconds, int(seconds * sample_rate), endpoint=False)
    note = np.iinfo(np.int16).max * np.sin(2 * np.pi * fs * t)
    wavfile.write(str(filename)+'.wav', sample_rate, note.astype(np.int16))