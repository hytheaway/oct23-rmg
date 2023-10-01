import timinggeneration as tg
import random
import noisegeneration as ng
import math

time_signature, measure_pulses = tg.generate_timing()

bpm = random.randint(20,250)

beat_length = 60 / bpm

# print('bpm: ', bpm)
# print('beat length: ', beat_length)

# how long is the song going to be? at least one minute. how many measures is that? depends on the bpm. 

# measures_to_get_to_one_minute = bpm / time_signature[1]
# measures_to_get_to_one_minute_ceil = math.ceil(bpm / time_signature[1])

# print('time signature: ', time_signature)
# print('measures to get to a minute: ', measures_to_get_to_one_minute)
# print('rounded up: ', measures_to_get_to_one_minute_ceil)

def create_measures(time_signature, bpm):
    total_measures = math.ceil(bpm / time_signature[0])

    list_of_measures = []
    for i in range(0, total_measures):
        list_of_measures.append(tg.generate_measure_pulses(time_signature[0]))
    return(list_of_measures)

