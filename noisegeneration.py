import numpy as np
from scipy.io import wavfile
from scipy import stats

sample_rate = 441000

def generate_noise(seconds, amplitude, filename):
    noise = stats.truncnorm(-1, 1, scale=min(2**16, 2**amplitude)).rvs(sample_rate * seconds)
    wavfile.write(str(filename), sample_rate, noise.astype(np.int16))
