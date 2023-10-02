import os
import random
import math
import datetime
import numpy as np
from scipy.io import wavfile
from pydub import AudioSegment
import timinggeneration as tg
import noisegeneration as ng
import wavegeneration as wg

time_signature, measure_pulses = tg.generate_timing()
bpm = random.randint(20,60)
beat_length = math.ceil(60 / bpm)


# generates the blueprint of which beats will get sound, writes this information to a metadata txt file
def create_measures(time_signature, bpm, prefix_string):
    prefix_string = str(prefix_string)

    # given the time signature and bpm, calculate how many measures would be needed to reach about a minute in length
    total_measures = math.ceil(bpm / time_signature[0])

    # create an empty list, create a blueprint for each measure (in terms of which beats will have sound and which will not), and then append the created measure
    # (represented as a list) to the larger list of all the measures
    list_of_measures = []
    for i in range(0, total_measures):
        list_of_measures.append(tg.generate_measure_pulses(time_signature[0]))
    
    # create a new txt file and fill in all the information about each file's generated measures
    f = open('outputs/metadata/' + prefix_string + str(datetime.datetime.now()) + '.txt', 'a')
    f.write('time signature: ' + str(time_signature))
    f.write('\nbpm: ' + str(bpm))
    f.write('\ntotal measures: ' + str(total_measures))
    f.write('\n' + str(list_of_measures))

    return(list_of_measures)


# generate individual noise wav files for each 1, and silent wav files for each 0
def make_some_noise():
    noise_measures = create_measures(time_signature, bpm, 'noise_')
    filename_list = []
    for i in range(len(noise_measures)):
        for j in range(len(noise_measures[i])):
            if noise_measures[i][j] == 1:
                filename = 'inputs/noise' + str(datetime.datetime.now())
                ng.generate_noise(int(beat_length), int(random.randint(1,10)), 44100, filename)
                filename_list.append(str(filename)+'.wav')
            elif noise_measures[i][j] == 0:
                filename = 'inputs/noise' + str(datetime.datetime.now())
                ng.generate_noise(int(beat_length), 0, 44100, filename)
                filename_list.append(str(filename)+'.wav')

    # cast each .wav file to an AudioSegment object
    for h in range(len(filename_list)):
        filename_list[h] = AudioSegment.from_wav(filename_list[h])

    # combine all the AudioSegment objects into one large AudioSegment object
    final_noise = AudioSegment.empty()
    for k in range(len(filename_list)):
        final_noise = final_noise + filename_list[k]

    # export the combined AudioSegment object as a .wav file
    output_filename = str(datetime.datetime.now()) + 'make-some-noise.wav'
    final_noise.export('outputs/' + output_filename, format='wav')


# generate individual sine wave wav files for each 1, and silent wav files for each 0
def make_some_music():
    note_measures = create_measures(time_signature, bpm, 'notes_')
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
    
    # cast each .wav file to an AudioSegment object
    for h in range(len(filename_list)):
        filename_list[h] = AudioSegment.from_wav(filename_list[h])

    # combine all the AudioSegment objects into one large AudioSegment object
    final_note = AudioSegment.empty()
    for k in range(len(filename_list)):
        final_note = final_note + filename_list[k]

    # export the combined AudioSegment object as a .wav file
    output_filename = str(datetime.datetime.now()) + 'make-some-music.wav'
    final_note.export('outputs/' + output_filename, format='wav')

# gives option to clear last results
def clear_previous():
    clear_option = str(input('clear previous? y/n '))
    if clear_option == 'y':
        inputs_dir_name = 'inputs/'
        inputs_dir_list = os.listdir(inputs_dir_name)
        for item in inputs_dir_list:
            if item.endswith('.wav'):
                os.remove(os.path.join(inputs_dir_name, item))

        outputs_dir_name = 'outputs/'
        outputs_dir_list = os.listdir(outputs_dir_name)
        for item in outputs_dir_list:
            if item.endswith('.wav'):
                os.remove(os.path.join(outputs_dir_name, item))

        meta_dir_name = 'outputs/metadata/'
        meta_dir_list = os.listdir(meta_dir_name)
        for item in meta_dir_list:
            if item.endswith('.txt'):
                os.remove(os.path.join(meta_dir_name, item))
    
        continue_option = str(input('continue? y/n '))
        if continue_option == 'n':
            return('n')


# main function
# asks the user how many voices of noise they want to generate, then how many voices of sine waves they want to generate
# generates the user-determined number of noise files, and the user-determined number of sine wave files. 
def lets_do_this_thing():
    
    if clear_previous() == 'n':
        return

    # does this thing
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
    
    # turn .wav files into numpy arrays and adds them together to create one .wav file by the end of it, IS NOT THE SAME AS PLAYING ALL WAV FILES INDIVIDUALLY
    output_wav_file_list = []
    for item in os.listdir('outputs/'):
        if item.endswith('.wav'):
            output_wav_file_list.append(item)

    object_list = []
    for audio_file in output_wav_file_list:
        a = wavfile.read('outputs/' + audio_file)
        object_list.append(a[1])

    for index in range(len(object_list)):
        object_list[index] = object_list[index] + object_list[index-1]
        combined_song = object_list[index]
        
    wavfile.write('outputs/destruct-o-matic.wav', 44100, combined_song.astype(np.int16))

lets_do_this_thing()