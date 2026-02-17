import sounddevice as sd
import numpy as np

SILENT_THRESHOLD = 0.008
SINGLE_THRESHOLD = 0.02

def detect_audio(duration=0.5, fs=44100):
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float64')
    sd.wait()

    rms = np.sqrt(np.mean(recording**2))

    if rms < SILENT_THRESHOLD:
        return "Silent"
    elif rms < SINGLE_THRESHOLD:
        return "Single"
    else:
        return "Multiple"


# import sounddevice as sd
# import numpy as np

# def detect_audio(duration=0.5, fs=44100):
#     recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float64')
#     sd.wait()

#     volume = np.linalg.norm(recording)

#     # Tuned values for better detection
#     if volume < 0.015:
#         return "silent"
#     elif volume < 0.06:
#         return "single"
#     else:
#         return "multiple"

# import sounddevice as sd
# import numpy as np
# import time

# last_audio_time = 0

# def detect_audio(duration=0.5, fs=44100):
#     global last_audio_time

#     # 1 sec me sirf 1 baar audio read
#     if time.time() - last_audio_time < 1:
#         return None

#     last_audio_time = time.time()

#     recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float64')
#     sd.wait()

#     volume = np.linalg.norm(recording)

#     if volume < 0.02:
#         return "silent"
#     elif volume < 0.07:
#         return "single"
#     else:
#         return "multiple"
