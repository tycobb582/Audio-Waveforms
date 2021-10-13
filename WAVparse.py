# the foundation for this code was taken from https://www.youtube.com/watch?v=4rzpMA6CUPg
# and https://stackoverflow.com/questions/23154400/read-the-data-of-a-single-channel-from-a-stereo-wave-file-in-python
import wave as pywav
import scipy.io.wavfile as wf
import numpy as np
import sys
import time

start_time = time.time()

def get_wave_sci(file_name_str):
    data = wf.read(file_name_str)
    wave = data[:,0]
    return wave
                            
def get_wave(file_name_str):
    wave=pywave.open("test.wav", "r")
    raw = pywav.readframes(-1)
    raw = np.frombuffer(raw, int16)
                        

def print_wave(wave):
    np.set_printoptions(threshold=sys.maxsize)
    print(wav)

    
#if wav.getnchannels()==2:
#    print("Stereo Files are not accepted")
#    sys.exit(0)


wav = get_wave_sci("input.wav")
print_wave(wav)
print(f"Program executed in {time.time()-start_time} seconds")

