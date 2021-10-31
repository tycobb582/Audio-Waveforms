# the foundation for this code was taken from https://www.youtube.com/watch?v=4rzpMA6CUPg
# and https://stackoverflow.com/questions/23154400/read-the-data-of-a-single-channel-from-a-stereo-wave-file-in-python
# info on simple_audio https://realpython.com/playing-and-recording-sound-python/#simpleaudio
import scipy.io.wavfile as wf
import numpy as np
import simpleaudio as sa
import time
import sys
import random
import math
import os

##################################INITIALIZATION##############################

start_time = time.time()

try:
    input = sys.argv[1]
except:
    input = "input.wav"


##################################FUNCTIONS##################################

def get_wave_array(file_name_str):
    """
    Gets aa array from a given wav file simplifying to mono
    :param file_name_str: full file name and path
    :return: wav array, rate
    """
    rate, data = wf.read(file_name_str)
    wave = data[:, 0] # this is extracting the first column from each array in a 2D array containing the information
    # from both audio channels
    return wave, rate
                        
def print_wave(wave):
    """
    prints an entire wav array CAUTION THIS COULD OVERLOAD OUTPUT AND CRASH
    :param wave: wav array
    :return:
    """
    np.set_printoptions(threshold=sys.maxsize)
    print(wave)

def create_wave(wave, rate=44100, file_name="output.wav"):
    """
    Creates a wav file from the given wav array and information
    :param wave: 
    :param rate: 
    :param file_name: 
    :return: 
    """
    wf.write(file_name, rate, wave)

def noise(wave, static_factor=10000):
    """
    adds a static effect to the given wav array
    :param wave: array from wav file
    :param static_factor: The ammount of static
    :return: altered wav array
    """
    for i in range(len(wave)):
        wave[i] += random.randint(-static_factor, static_factor)
    return wave

def remove_silence(wave):
    """
    Significantly cuts out any silence in an audio file
    :param wave: A .wav file in numpy array form
    :return: A new array with certain values removed
    """
    temp = wave
    for i in range(-3, 4):
        clipped_wave = np.delete(temp, np.where(temp == i))
        temp = clipped_wave
    return clipped_wave

def clip_start_and_end(wave):
    """
    Removes all silence from the beginning and ending of an audio clip
    :param wave: A .wav file in numpy array form
    :return: The clipped .wav file
    """
    # Create a list of all indices where the value is less than -40 or greater than 40
    non_silence_indices = np.where(abs(wave) > abs(40))
    start_index = non_silence_indices[0][0]
    end_index = non_silence_indices[0][-1]
    clipped_wave = wave[start_index:end_index+1]
    return clipped_wave

def volume(wave, factor):
    """
    Function to adjust volume of a sound clip
    :param wave: A .wav file in numpy array form
    :param factor: The factor to adjust the volume by
    :return: The volume-adjusted wave array
    """
    for i in range(len(wave) - 1):
        wave[i] *= factor
    return wave

def sin(wave, sin_factor=2000):
    """
    Takes a wav array and modulates each point by a sin wave at the given frequency
    :param wave: array from wave file
    :param sin_factor:
    :return: altered wav array
    """
    j = 0
    for i in range(len(wave)):
        tmp = math.sin(j) * sin_factor
        #print(f"tmp{tmp} wave{wave[i]}")
        wave[i] += tmp
        j += 0.0006
    return wave


def average_of_sounds(folder):
    """
     Takes a folder containing .wav files of the exact same length, converts them into NumPy array,
     averages these arrays, and creates a new .wav file from this average.
     :param folder: The name of the folder with the .wav files to average, in string form
     :return: Void
     """
    audio_folder = os.path.join(os.path.dirname(__file__), folder)
    audio_set = os.listdir(audio_folder)
    rate = None
    wave_sum = None
    for file in audio_set:
        path = os.path.join(audio_folder, file)
        wav, rate = get_wave_array(path)
        if wave_sum is None:
            wave_sum = wav
        else:
            wave_sum += wav
    wave_average = wave_sum // len(audio_set)
    create_wave(wave_average, rate, "average.wav")

def play_output(filename):
    """
    Takes the filename of a .wav file and plays the sound
    """
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()

def build_cov_matrix(in_folder):
    """
    builds a covariance matrix out of the wav arrays of all files in a given folder
    :param in_folder: input folder of wav files
    :return: covariance matrix
    """
    start_time = time.time()
    max_length = 10000000000
    vecs = []  # blank list for wave vectors
    # try:
    for file in os.listdir(in_folder):
        file_name = os.path.join(in_folder, file)
        wav, rate = get_wave_array(file_name)  # find vector from file
        max_length = min(wav.size, max_length)
        vecs.append(wav)  # add the vector to the list]
    clamped_vecs = []
    for vec in vecs:
        clamped_vecs.append(vec[:max_length])
    mat = np.asarray(clamped_vecs)
    cov_mat = np.cov(mat)
    return cov_mat, rate

def get_eigen_vecs(cov):
    """
    create a
    :param cov: covariance matrix of multiple wav arrays
    :return:
    """
    eigs = np.linalg.eig(cov) # eigs[0] == eigne values list eigs[1] == 2D array of eigenvectors
    linear_combination = np.linalg.solve(eigs[1], eigs[0])
    print(linear_combination)
    final_wav_array = linear_combination
    return eigs, final_wav_array# this isn't really supposed to be here but I use it for testing

    #print(f"Program executed in {time.time() - start_time} seconds")


##################################MAIN#######################################

# wav, rate = get_wave_array(input)
# #wav = clip_start_and_end(wav)
# print_wave(wav)
# #wave = test(wav)
#
# print(f"Program executed in {time.time()-start_time} seconds")
# create_wave(wav, rate=rate, file_name=input[:-4]+"out"+".wav")
#play_output(f"{input[:-4]}out.wav")
