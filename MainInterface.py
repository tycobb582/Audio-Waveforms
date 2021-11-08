# the foundation for this code was taken from https://www.youtube.com/watch?v=4rzpMA6CUPg
# and https://stackoverflow.com/questions/23154400/read-the-data-of-a-single-channel-from-a-stereo-wave-file-in-python
import scipy.io.wavfile as wf
import numpy as np
import time
import sys
import random
import math
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QInputDialog
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
        self.in_folder = "Audio files"
        self.out_folder = "Outputs"
        self.setWindowTitle("Eigenwave 9000")

        self.in_folder_button = QPushButton("Input Folder", self)
        self.in_folder_button.move(self.win_width // 4, self.win_height // 20 * 2)
        self.in_folder_button.clicked.connect(self.in_pick)

        self.build_mat_button = QPushButton("Build Matrix", self)
        self.build_mat_button.move(self.win_width // 4 * 2, self.win_height // 20 * 2)
        self.cov = []
        self.build_mat_button.clicked.connect(self.build_matrix)

        self.output_button = QPushButton("Create File", self)
        self.output_button.move(self.win_width // 4 * 2, self.win_height // 20 * 4)
        self.output_button.clicked.connect(self.do_output)

        self.out_pick_button = QPushButton("Output Folder", self)
        self.out_pick_button.move(self.win_width // 4, self.win_height // 20 * 4)
        self.out_pick_button.clicked.connect(self.out_pick)

        self.out_pick_button = QPushButton("Play Audio", self)
        self.out_pick_button.move(self.win_width // 4 * 3, self.win_height // 20 * 2)
        self.out_pick_button.clicked.connect(self.play_audio)

        self.out_pick_button = QPushButton("Create Average Sound", self)
        self.out_pick_button.move(self.win_width // 4 * 3, self.win_height // 20 * 4)
        self.out_pick_button.clicked.connect(self.average)

        self.show()

    @pyqtSlot()
    def in_pick(self):
        self.in_folder, done1 = QInputDialog.getText(
            self, 'Input Dialog', 'Source Folder Name:')
        print(f"changed input folder to \"{self.in_folder}\"")

    @pyqtSlot()
    def build_matrix(self):
        self.cov, self.rate = WAVp.build_cov_matrix(self.in_folder)
        self.eig_vals, self.final_wave_array = WAVp.get_eigen_vecs(self.cov)

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
        self.final_wave_array, self.rate = WAVp.average_of_sounds(self.in_folder, self.out_folder, file_name=self.save_file_name)

app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())
