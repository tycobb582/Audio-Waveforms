# the foundation for this code was taken from https://www.youtube.com/watch?v=4rzpMA6CUPg
# and https://stackoverflow.com/questions/23154400/read-the-data-of-a-single-channel-from-a-stereo-wave-file-in-python
import scipy.io.wavfile as wf
import numpy as np
import time
import sys
import random
import math
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot
import WAVparse as WAVp
##################################INITIALIZATION##############################
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.win_width = 800
        self.win_height = 600
        self.rate = 44100
        self.final_wave_array = []
        self.save_file_name = "output"
        self.eigs = []
        self.eig_vals = []
        self.setGeometry(400, 400, self.win_width, self.win_height)
        #self.setLayout(QVBoxLayout)
        self.in_folder = "Audio files"
        self.out_folder = "Outputs"
        self.setWindowTitle("Eigenwave 9000")
        self.buttons = []
        self.cov = []

        self.in_folder_button = QPushButton("INPUT FOLDER", self)
        self.in_folder_button.setToolTip("Default = Audio files")
        self.buttons.append(self.in_folder_button)
        self.in_folder_button.move(1, 1) # col, row
        self.in_folder_button.clicked.connect(self.in_pick)

        self.test_button = QPushButton("CREATE TEST WAVE", self)
        self.buttons.append(self.test_button)
        self.test_button.move(2, 1)
        self.test_button.clicked.connect(self.linear_combination)

        self.output_button = QPushButton("CREATE FILES", self)
        self.output_button.setToolTip("Default Name = output")
        self.buttons.append(self.output_button)
        self.output_button.move(3, 1)
        self.output_button.clicked.connect(self.do_output)

        self.out_pick_button = QPushButton("OUTPUT FOLDER", self)
        self.out_pick_button.setToolTip("Default = Outputs")
        self.buttons.append(self.out_pick_button)
        self.out_pick_button.move(1, 2)
        self.out_pick_button.clicked.connect(self.out_pick)

        self.play_audio_button = QPushButton("PLAY AUDIO", self)
        self.play_audio_button.setToolTip("Must have created file same as output name before playing")
        self.buttons.append(self.play_audio_button)
        self.play_audio_button .move(3, 2)
        self.play_audio_button .clicked.connect(self.play_audio)

        self.average_button = QPushButton("CREATE AVERAGE SOUND", self)
        self.buttons.append(self.average_button)
        self.average_button.move(2, 2)
        self.average_button.clicked.connect(self.average)

        # apply standard transformations
        for b in self.buttons:
            b.setGeometry(b.x(), b.y(), 200, 100)# set new size
            b.setGeometry(b.width() * b.x() - b.width() // 2, b.y() * b.height(), b.width(), b.height())# center

        self.show()

    @pyqtSlot()
    def in_pick(self):
        self.in_folder, done1 = QInputDialog.getText(
            self, 'Input Dialog', 'Source Folder Name:')
        print(f"changed input folder to \"{self.in_folder}\"")

    @pyqtSlot()
    def linear_combination(self):
        self.cov, self.rate = WAVp.build_cov_matrix(self.in_folder)
        self.eig_vals, self.final_wave_array = WAVp.get_eigen_vecs(self.cov)
        # output
        self.save_file_name, _ = QInputDialog.getText(self, 'Input Dialog', 'Output File Name:')
        wf.write(self.out_folder + "/" + self.save_file_name + ".wav", self.rate, self.final_wave_array)
        print("created wave file")

    @pyqtSlot()
    def out_pick(self):
        self.out_folder, _ = QInputDialog.getText(self, 'Input Dialog', 'Output Folder Name:')
        print(f"set output folder to \"{self.out_folder}\"")

    @pyqtSlot()
    def do_output(self):
        self.save_file_name, _ = QInputDialog.getText(self, 'Input Dialog', 'Output File Name:')
        # try:
        wf.write(self.out_folder + "/" + self.save_file_name + ".wav", self.rate, self.final_wave_array)
        print("created wave file")
        # except:
        #    print(self.out_folder+"/"+self.save_file_name+".wav" + " is not a valid output directory. Change it or else")

    @pyqtSlot()
    def play_audio(self):
        WAVp.play_output(self.out_folder + "/" + self.save_file_name + ".wav")

    @pyqtSlot()
    def average(self):
        self.final_wave_array, self.rate = WAVp.average_of_sounds(self.in_folder, self.out_folder, file_name=self.save_file_name, write_file=True)

app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())
