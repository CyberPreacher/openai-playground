"""
create a function who takes in input a sound from internal macbook pro microphone and trigger when a sound is detected
"""
import pyaudio
import wave
import time
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.io import wavfile
from scipy.fftpack import fft
from scipy.signal import find_peaks
from scipy.signal import butter, lfilter
from scipy.signal import freqz
from scipy.signal import correlate
from scipy.signal import argrelextrema

def capture_sound_from_microphone():
    """
        capture sound from microphone and save it in a wav file
        """
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 20
    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []
    sound_count_detected = 0
    last_sound_detected = 0
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
        sound_stream = np.fromstring(data, dtype=np.int16)
        sound_detected = trigger_event_from_sound_detected(sound_stream, 40.0)
        if sound_detected:

            sound_count_detected += 1
            with wave.open(WAVE_OUTPUT_FILENAME.format(sound_count_detected), 'wb') as f:
                f.setnchannels(CHANNELS)
                f.setsampwidth(p.get_sample_size(FORMAT))
                f.setframerate(RATE)
                f.writeframes(b''.join(frames[last_sound_detected:]))
                last_sound_detected = i


        # plot_sound_stream(frames)



    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def trigger_event_from_sound_detected(sound_stream, threshold):
    """
        trigger event when sound is detected in rms level
        """

    rms_sound_stream = np.sqrt(np.mean(sound_stream ** 2))
    if rms_sound_stream < threshold:
        print("sound detected")
        return True


def plot_sound_stream(sound_stream):
    """
        plot sound stream
        """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(sound_stream)
    plt.show()

if __name__ == '__main__':
    capture_sound_from_microphone()








