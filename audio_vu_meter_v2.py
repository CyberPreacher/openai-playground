"""
create a ui display volume in RMS from input mic audio signal with pyqt5
"""
import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider, QLabel
from PyQt5.QtCore import QThread, pyqtSignal, QTimer, Qt
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush
import wave
import sys
import pyaudio
import numpy as np
import math
from ctypes import *
import time
from collections import deque
import struct

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 20
WAVE_OUTPUT_FILENAME = "output.wav"

def get_rms(data):
    count = len(data) / 2
    format = "%dh" % (count)
    shorts = struct.unpack(format, data)
    sum_squares = 0.0
    for sample in shorts:
        n = sample * (1.0 / 32768)
        sum_squares += n * n
        rms = math.pow(sum_squares / count, 0.5)
        return rms * 1000


class Grapher(QMainWindow):
    def __init__(self):
        super(Grapher, self).__init__()

        self.setGeometry(200, 200, 500, 300)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(20)

        self.x_pos = 0
        self.y_pos = 0

        self.x_max = 500
        self.threshold_slider = QSlider(Qt.Horizontal, self)
        self.threshold_slider.setGeometry(30, 40, 200, 30)
        self.threshold_slider.setMinimum(1)
        self.threshold_slider.setMaximum(1000)
        self.threshold_slider.setValue(500)
        self.threshold_slider.setTickPosition(QSlider.TicksBelow)
        self.threshold_slider.setTickInterval(10)
        self.threshold_slider.valueChanged.connect(self.setThreshold)

        self.label_threshold = QLabel("threshold", self)
        self.label_threshold.move(30, 20)

        self.y_max = 250
        self.audio_level_danger_zone = 80

        self.rms_list = [0] * 500

        self.threshold = 0.05
        self.over_threshold = False

        # self.color = (0,255,0)

    def paintEvent(self, event):
        painter = QPainter()

        painter.begin(self)

        self.drawLines(event, painter)

        painter.end()

    def drawLines(self, event, painter):

        # pen = QPen(QColor('blue'), 1)



        for i in range(1, self.x_max):
            if self.y_max - self.rms_list[i - 1] < self.audio_level_danger_zone:
                painter.setPen(QPen(QColor('orange'), 1))
            else:
                painter.setPen(QPen(QColor('blue'), 1))
            painter.drawLine(i - 1, self.y_max - self.rms_list[i - 1], i, self.y_max - self.rms_list[i])

        if self.y_pos > 1:
            pen = QPen(QColor('red'), 1)

            painter.setPen(pen)

            painter.drawLine(self.x_pos - 1, self.y_max - self.rms_list[self.x_pos - 1], self.x_pos - 1, 0)

    def update(self):

        if self.x_pos >= 500:
            for i in range(500):
                if i < 499:
                    self.rms_list[i] = self.rms_list[i + 1]

            self.x_pos -= 1

        self.repaint()
    """keep a value between 10 and 250"""
    calculate_value_in_range = lambda self, value: max(min(value, 250), 10)


    def addPoint(self, point) -> bool:
        if point > self.threshold:
            self.over_threshold = True
            # self.y_pos = 250 - ((point / self.threshold))
            self.y_pos = ((point / 10) * 250)

            if self.y_pos < 10:
                self.y_pos = 10

            if self.y_pos > 240:
                self.y_pos = 240

            print("POINT =", point, "y position {}".format(self.y_pos))



            if point > 2.0:
                print("over threshold")

                print("POINT =", point, "y_pos =", self.y_pos)

                self.color = (255,0,0)

                # print("over threshold")

                # print(point)

                # self.setStyleSheet("QWidget { background-color: green }")

            else:
                self.color = (0,255,0)

                # self.setStyleSheet("QWidget { background-color: red }")


            if self.x_pos >= 500:
                for i in range(500):
                    if i < 499:
                        self.rms_list[i] = self.rms_list[i + 1]

                self.x_pos -= 1

            else:
                pass

            try:
                self.rms_list[self.x_pos] = int(self.y_pos)
            except Exception as e:
                print("error", e)

            self.x_pos += 1

            # print("added point")

        else:
            self.over_threshold = False

        return self.over_threshold

    def setThreshold(self, threshold):
        self.threshold = threshold / 100
        self.label_threshold.setText("threshold: " + str(self.threshold))

        print("threshold is", self.threshold)


class AudioThread(QThread):
    def __init__(self):
        super().__init__()

    def run(self):
        CHUNK = 1024 # CHUNKS of bytes to read each time from mic

        FORMAT = pyaudio.paInt16  # bytes per sample/channel (16bit=2bytes per channel)

        CHANNELS = 1  # stereo (2 channels) but mono is only 1 channel (2nd channel will be ignored)

        RATE = 44_100  # samples per second (Hz), eg: 44100 samples per second / second (or 44100 Hz)  (CD quality is 44100 Hz)

        p = pyaudio.PyAudio()  # create an interfacing object using pyaudio

        stream = p.open(format=FORMAT,
                        # 16bit per sample (2 bytes per sample/channel), 1 channel (mono), 44100 samples per second (CD quality is 44100 Hz) (stereo=2 channels/streams)
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)  # buffer size in number of frames (samples/channel * channels * seconds = bytes)

        print("* listening")
        sound_count_detected = 0
        number_of_file_recorded = 0
        sound_detected_list = []
        sound_recorded_dir = "sound_recorded"
        while True:
            data = stream.read(CHUNK)  # read audio stream data (CHUNK number of bytes)

            rms = get_rms(data)
            # sound_stream = np.fromstring(data, dtype=np.int16)

            sound_detected = grapher.addPoint(rms)
            if sound_detected:
                sound_count_detected += 1
                sound_detected_list.append(data)
            else:
                if sound_count_detected > 10:
                    if not os.path.exists(sound_recorded_dir):
                        os.mkdir(sound_recorded_dir)
                    with wave.open("{}/{}-{}".format(sound_recorded_dir, number_of_file_recorded, WAVE_OUTPUT_FILENAME,), 'wb') as f:
                        f.setnchannels(CHANNELS)
                        f.setsampwidth(p.get_sample_size(FORMAT))
                        f.setframerate(RATE)
                        f.writeframes(b''.join(sound_detected_list))
                    sound_count_detected = 0
                    sound_detected_list = []
                    number_of_file_recorded += 1
                else:
                    sound_count_detected = 0
                    sound_detected_list = []

        stream.stop_stream()  # stop the stream object
        stream.close()  # close and terminate the stream object
        p.terminate()  # terminate the interface


if __name__ == '__main__':
    app = QApplication([])

    grapher = Grapher()

    thread = AudioThread()

    thread.start()

    grapher.show()

    sys.exit(app.exec())


