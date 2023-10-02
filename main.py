import timinggeneration as tg
import random
import noisegeneration as ng
import math
from pydub import AudioSegment
import datetime
import wavegeneration as wg

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

noise_measures = create_measures(time_signature, bpm)

# print(noise_measures)

# generate noise wav files for each 1, and silent wav files for each 0
def make_some_noise():
    filename_list = []
    for i in range(len(noise_measures)):
        for j in range(len(noise_measures[i])):
            if noise_measures[i][j] == 1:
                filename = datetime.datetime.now()
                ng.generate_noise(int(beat_length), int(random.randint(10,16)), 44100, filename)
                filename_list.append(str(filename)+'.wav')
            elif noise_measures[i][j] == 0:
                filename = datetime.datetime.now()
                ng.generate_noise(int(beat_length), 0, 44100, filename)
                filename_list.append(str(filename)+'.wav')

    for h in range(len(filename_list)):
        filename_list[h] = AudioSegment.from_wav(filename_list[h])

    final_noise = AudioSegment.empty()
    for k in range(len(filename_list)):
        final_noise = final_noise + filename_list[k]
        # print(final_noise)

    final_noise.export('make-some-noise.wav', format='wav')

make_some_noise()

def make_some_music():
    note_measures = create_measures(time_signature, bpm)
    filename_list = []
    for i in range(len(note_measures)):
        for j in range(len(note_measures[i])):
            if note_measures[i][j] == 1:
                filename = 'note' + str(datetime.datetime.now())
                wg.generate_note(int(beat_length), 44100, filename)
                filename_list.append(str(filename)+'.wav')
            elif note_measures[i][j] == 0:
                filename = 'note' + str(datetime.datetime.now())
                ng.generate_noise(int(beat_length), 0, 44100, filename)
                filename_list.append(str(filename)+'.wav')
    
    for h in range(len(filename_list)):
        filename_list[h] = AudioSegment.from_wav(filename_list[h])

    final_note = AudioSegment.empty()
    for k in range(len(filename_list)):
        final_note = final_note + filename_list[k]

    final_note.export('make-some-music.wav', format='wav')

make_some_music()