import random

# generates a random time signature, from 1 - 12 beats per measure, and with the whole, half, quarter, eighth, sixteenth, or thirty-second note getting the beat
def generate_time_signature():
    upper_numeral = random.randint(3,12)    #lower values here combined with a high bpm tend to result in non-functional wav files
    lower_numeral_array = [1,2,4,8,16,32]
    lower_numeral_array_index = random.randint(0,5)
    lower_numeral = lower_numeral_array[lower_numeral_array_index]
    time_signature = [upper_numeral,lower_numeral]

    return(time_signature)


# determines where the pulses in a measure should be distributed, on which beats should a pulse occur. 
# ensures that, as long as there are pulses to be distributed, they will only be distributed on beats that don't already have a pulse. 
def distribute_pulses(pulses, measure):
    while pulses > 0:
        for j in range(0, len(measure)):
            if measure[j] == 1:
                continue
            elif measure[j] == 0:
                if pulses > 0:
                    coin_flip = random.randint(0,1)
                    if coin_flip == 1:
                        measure[j] = 1
                        pulses -= 1
                    elif coin_flip == 0:
                        measure[j] = 0
                else:
                    break
            else:
                break
    return(measure)


# determines how many pulses there should be in a measure, given the amount of beats in the measure
def generate_measure_pulses(beats_per_measure):
    single_measure = []
    i = 0
    while i < beats_per_measure:
        single_measure.append(0)
        i += 1
    
    pulses_per_measure = random.randint(0, beats_per_measure)

    return(distribute_pulses(pulses_per_measure, single_measure))


# overall function that brings this all together
def generate_timing():
    time_signature = generate_time_signature()
    return(time_signature, generate_measure_pulses(time_signature[0]))

