# some of the foundation for this code was made with the help of these resources
# https://www.youtube.com/watch?v=4rzpMA6CUPg
# https://stackoverflow.com/questions/23154400/read-the-data-of-a-single-channel-from-a-stereo-wave-file-in-python
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
    print(file_name_str)
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


def average_of_sounds(input_folder, output_folder, write_file=True, file_name="average"):
    """
     Takes a folder containing .wav files of the exact same length, converts them into NumPy array,
     averages these arrays, and creates a new .wav file from this average.
     :param folder: The name of the folder with the .wav files to average, in string form
     :return average wav array: Elijah added this so I could use it with the MainInterface
     """
    audio_folder = os.path.join(os.path.dirname(__file__), input_folder)
    audio_set = os.listdir(audio_folder)
    rate = None
    max_len = 1000000000000
    waves = []
    for file in audio_set:
        path = os.path.join(audio_folder, file)
        wav, rate = get_wave_array(path)
        max_len = min(len(wav), max_len)
        waves.append(wav)
    wave_average = np.asarray(waves).mean(0, int)
    if write_file:
        create_wave(wave_average, rate, output_folder + "/" + file_name + ".wav")
    return wave_average, rate   # Elijah - added this so I could use it with the MainInterface


def pca(folder):
    """
    Performs principal component analysis on a set of .wav files
    :param folder: The folder for the training data
    :return: The mean array and the principal components
    """
    OM = wav_observation_mat(folder)
    data_average = OM.mean(0, int)  # Average values through each column, keeps them int type
    if os.path.exists("Data Files/" + folder + ".npy"):
       eigs = read_vecs(folder) 
    else:
        eigs = cov_eig(OM, folder)
    T = np.zeros((len(OM), np.shape(OM[0])[0]))
    for i in range(len(OM)):
        T[i] = np.matmul((OM[i] - data_average), eigs)
    return data_average, eigs

def wav_observation_mat(folder):
    """
    Converts .wav files into numpy arrays and constructs an observation matrix from those arrays
    :param folder: The folder with the files you want to build the matrix out of
    :return: The observation matrix in numpy array form
    """
    search_folder = os.path.join(os.path.dirname(__file__), folder)
    observation_vectors = os.listdir(search_folder)
    observation_matrix = None
    count = 0
    wave_sum = None
    for file in observation_vectors:
        path = os.path.join(search_folder, file)
        wav, rate = get_wave_array(path)
        if wave_sum is None:
            wave_sum = wav
        else:
            wave_sum += wav
        if observation_matrix is None:
            observation_matrix = np.zeros((len(observation_vectors), np.shape(wav)[0]))
            observation_matrix[0] = wav
        else:
            observation_matrix[count] = wav
        count += 1
    return observation_matrix, rate

def cov_eig(om, write_to_name, keep=50):
    """
    Finds the eigenvectors of a covariance matrix, sorts them by importance, and delivers the specified amount
    :param om: The observation matrix to build the covariances from
    :param keep: Number of eigenvectors to keep
    :return: The requested set of eigenvectors
    """
    print("Loading eigen vectors...")
    covariance = np.cov(np.transpose(om))
    eigen = np.linalg.eig(covariance)
    print("Done loading eigen vectors")
    vecs = np.transpose(eigen[1])   # Transposed to collect all eigenvector components in a single array
    dict = {}   # Dictionary to keep track of which values correspond to which vectors
    for i in range(len(eigen[0])):
        dict[eigen[0][i]] = vecs[i]
    vals = -np.sort(-eigen[0])  # Sort values, biggest ones first
    count = 0
    for i in vals:  # Sort array of vectors to match sorted array of values
        vecs[count] = dict[i]
        count += 1
    vecs = vecs[0:keep]   # Keep only the 50 most important components
    write_vecs(vecs, write_to_name) #save them to a file
    return vecs

def combine(eigs, coefficients, rate=44100, write_file=False, file_name="new_combination"):
    """
    Creates a numpy array that is a linear combination of a set of eigenvectors
    :param eigs: The set of eigenvectors to combine
    :param coefficients: A numpy array of coefficients to multiple the eigenvectors by. Must be the same length as the set of eigs.
    :return: The resulting sum
    """
    if isinstance(coefficients, np.ndarray) and np.shape(coefficients)[1] == np.shape(eigs)[0]:
        pass
    else:
        raise TypeError("Coefficients must be provided as a numpy array with the same length as the number of eigenvectors.")
    sum = 0
    eigs = eigs.real    # Convert from complex to real numbers
    for i in range(len(eigs)):
        sum += np.multiply(eigs[i], coefficients[0][i])
    sum = np.transpose(np.asarray(sum)) # Return vectors to numpy form
    if write_file:
        create_wave(sum, rate, "Linear Combinations/" + file_name + ".wav")
    return np.around(sum)   # Sum must be rounded to create a .wav

def write_vecs(vecs, file_name="pca vectors"):
    """Writes a .npy file containing the given numpy array in the Data Files folder"""
    np.save("Data Files/" + file_name, vecs)

def read_vecs(file_name="pca vectors"):
    """Reads a numpy array from the .npy file in the Data Files Folder"""
    vecs = np.load("Data Files/" + file_name + ".npy")
    return vecs

def play_output(filename):
    """
    Takes the filename of a .wav file and plays the sound
    """
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()


##################################MAIN#######################################
if __name__ == "__main__":
    vecs = read_vecs("Train")
    coeff = np.random.randint(1, 3, (1, np.shape(vecs)[0]))
    sum = combine(vecs, coeff, write_file=True, file_name="Train Eigs 50 Coeffs Random 1-2")
    # wav, rate = get_wave_array(input)
    # #wav = clip_start_and_end(wav)
    # print_wave(wav)
    # #wave = test(wav)
    #
    print(f"Program executed in {time.time()-start_time} seconds")
    # create_wave(wav, rate=rate, file_name=input[:-4]+"out"+".wav")
    #play_output(f"{input[:-4]}out.wav")
