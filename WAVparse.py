# the foundation for this code was taken from https://www.youtube.com/watch?v=4rzpMA6CUPg
# and https://stackoverflow.com/questions/23154400/read-the-data-of-a-single-channel-from-a-stereo-wave-file-in-python
import scipy.io.wavfile as wf
import numpy as np
import time
import sys
import random
import math

##################################INITIALIZATION##############################

start_time = time.time()
    
try:
    input = sys.argv[1]
except:
    input = "input.wav"


##################################FUNCTIONS##################################

def get_wave_array(file_name_str):
    rate, data = wf.read(file_name_str)
    wave = data[:,0]
    return wave, rate
                        
def print_wave(wave):
    np.set_printoptions(threshold=sys.maxsize)
    print(wav)

def create_wave(wave, rate=44100, file_name="output.wav"):
    wf.write(file_name, rate, wave)

def noise(wave, static_factor=10000):
    for i in range(len(wave)):
        wave[i] += random.randint(-static_factor,static_factor)
    return wave

def sin(wave, sin_factor=2000):
    j = 0
    for i in range(len(wave)):
        tmp = math.sin(j) * sin_factor
        #print(f"tmp{tmp} wave{wave[i]}")
        wave[i] += tmp
        j += 0.0006
    return wave

def test(wave):
    for i in range(len(wave)):
        step = wave[i] - wave[i-1]
        wave[i] += step
    return wave

##################################MAIN#######################################

wav, rate = get_wave_array(input)
#print_wave(wav)
wave = test(wav)

print(f"Program executed in {time.time()-start_time} seconds")
create_wave(wav, rate=rate, file_name=input[:-4]+"out"+".wav")
