import timinggeneration as tg
import random
import noisegeneration as ng
import math
from pydub import AudioSegment
from pydub.playback import play
import datetime

time_signature, measure_pulses = tg.generate_timing()

bpm = random.randint(20,60)

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

music_measures = create_measures(time_signature, bpm)

# print(music_measures)

# generate noise wav files for each 1, and silent wav files for each 0
def make_some_noise():
    filename_list = []
    for i in range(len(music_measures)):
        for j in range(len(music_measures[i])):
            if music_measures[i][j] == 1:
                filename = datetime.datetime.now()
                ng.generate_noise(int(beat_length), int(random.randint(10,16)), 44100, filename)
                filename_list.append(str(filename)+'.wav')
            elif music_measures[i][j] == 0:
                filename = datetime.datetime.now()
                ng.generate_noise(int(beat_length), 0, 44100, filename)
                filename_list.append(str(filename)+'.wav')

    for h in range(len(filename_list)):
        filename_list[h] = AudioSegment.from_wav(filename_list[h])

    final_song = AudioSegment.empty()
    for k in range(len(filename_list)):
        final_song = final_song + filename_list[k]
        # print(final_song)

    final_song.export('output.wav', format='wav')

make_some_noise()