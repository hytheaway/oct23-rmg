import numpy as np
from scipy.io import wavfile
from scipy import stats

sample_rate = 441000
length_in_seconds = 3
amplitude = 11
noise = stats.truncnorm(-1, 1, scale=min(2**16, 2**amplitude)).rvs(sample_rate * length_in_seconds)
wavfile.write('noise.wav', sample_rate, noise.astype(np.int16))

