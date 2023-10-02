import numpy as np
from scipy.io import wavfile
from scipy import stats

def generate_noise(seconds, amplitude, sample_rate, filename):
    noise = stats.truncnorm(-1, 1, scale=min(2**16, 2**amplitude)).rvs(sample_rate * seconds)
    wavfile.write((str(filename)+'.wav'), sample_rate, noise.astype(np.int16))
