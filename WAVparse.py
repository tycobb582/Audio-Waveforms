# the foundation for this code was taken from https://www.youtube.com/watch?v=4rzpMA6CUPg
# and https://stackoverflow.com/questions/23154400/read-the-data-of-a-single-channel-from-a-stereo-wave-file-in-python
import scipy.io.wavfile as wf
import numpy as np
import time
import sys

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
    return wave
                        
def print_wave(wave):
    np.set_printoptions(threshold=sys.maxsize)
    print(wav)

def create_wave(wave, speed=1, file_name="output.wav"):
    rate = 44100 * speed
    wf.write(file_name, rate, wave)

##################################MAIN#######################################

wav = get_wave_array(input)
print_wave(wav)
print(f"Program executed in {time.time()-start_time} seconds")
create_wave(wav)
