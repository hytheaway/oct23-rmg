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
                ng.generate_noise(int(beat_length), int(random.randint(10,16)), 44100, filename)
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


# main function
# asks the user how many voices of noise they want to generate, then how many voices of sine waves they want to generate
# generates the user-determined number of noise files, and the user-determined number of sine wave files. 
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