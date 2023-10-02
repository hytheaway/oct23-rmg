import random
import math
import datetime
from pydub import AudioSegment
import timinggeneration as tg
import noisegeneration as ng
import wavegeneration as wg

time_signature, measure_pulses = tg.generate_timing()
bpm = random.randint(40,70)
beat_length = 60 / bpm

def create_measures(time_signature, bpm):
    total_measures = math.ceil(bpm / time_signature[0])
    list_of_measures = []
    for i in range(0, total_measures):
        list_of_measures.append(tg.generate_measure_pulses(time_signature[0]))
    return(list_of_measures)

# generate noise wav files for each 1, and silent wav files for each 0
def make_some_noise():
    noise_measures = create_measures(time_signature, bpm)
    filename_list = []
    for i in range(len(noise_measures)):
        for j in range(len(noise_measures[i])):
            if noise_measures[i][j] == 1:
                filename = 'inputs/noise' + str(datetime.datetime.now())
                ng.generate_noise(int(beat_length), int(random.randint(10,16)), 44100, filename)
                filename_list.append(str(filename)+'.wav')
            elif noise_measures[i][j] == 0:
                filename = 'inputs/noise' + str(datetime.datetime.now())
                ng.generate_noise(int(beat_length), 0, 44100, filename)
                filename_list.append(str(filename)+'.wav')

    for h in range(len(filename_list)):
        filename_list[h] = AudioSegment.from_wav(filename_list[h])

    final_noise = AudioSegment.empty()
    for k in range(len(filename_list)):
        final_noise = final_noise + filename_list[k]

    output_filename = str(datetime.datetime.now()) + 'make-some-noise.wav'
    final_noise.export('outputs/' + output_filename, format='wav')

def make_some_music():
    note_measures = create_measures(time_signature, bpm)
    filename_list = []
    for i in range(len(note_measures)):
        for j in range(len(note_measures[i])):
            if note_measures[i][j] == 1:
                filename = 'inputs/note' + str(datetime.datetime.now())
                wg.generate_note(int(beat_length), 44100, filename)
                filename_list.append(str(filename)+'.wav')
            elif note_measures[i][j] == 0:
                filename = 'inputs/note' + str(datetime.datetime.now())
                ng.generate_noise(int(beat_length), 0, 44100, filename)
                filename_list.append(str(filename)+'.wav')
    
    for h in range(len(filename_list)):
        filename_list[h] = AudioSegment.from_wav(filename_list[h])

    final_note = AudioSegment.empty()
    for k in range(len(filename_list)):
        final_note = final_note + filename_list[k]

    output_filename = str(datetime.datetime.now()) + 'make-some-music.wav'
    final_note.export('outputs/' + output_filename, format='wav')

def lets_do_this_thing():
    amount_of_noise = int(input('how much noise do ya wanna make? '))
    amount_of_music = int(input('how much music do ya wanna make? '))
    i = 0
    while i < amount_of_noise:
        make_some_noise()
        i += 1
    j = 0
    while j < amount_of_music:
        make_some_music()
        j += 1

lets_do_this_thing()