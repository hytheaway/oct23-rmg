# nyu-acmc-sketch1

goal:
to create a program that randomly generates multi-voice noise music, consisting of noise files of varying amplitude and sine wave files. 

known problems:
- cant create functions to generate wav files with non-integer lengths (both rvs and linspace expect ints for length/amount of samples)
- combining the individual voice's wav files together does not create the same result as playing them all together at once. 
    - likely because combining the wav files results in the waveform being altered, whereas playing them all back at once does not.