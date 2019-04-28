#!/usr/bin/python3.5

import numpy as np
from scipy.io import wavfile
import sys

raw_audio = np.fromfile("/tmp/sound.raw", np.int16)
wavfile.write("/tmp/sound.wav", rate=48000, data=raw_audio)


