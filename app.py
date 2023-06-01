from gtts import gTTS
from functools import partial
from pathlib import Path
import argparse
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import scipy.signal as sig
import psola
import sys
import os
from pydub import AudioSegment
from flask import Flask, send_file, request
from urllib import parse

app = Flask(__name__)

frame_length_input = 2048
fmin_input = librosa.note_to_hz('C2')
fmax_input = librosa.note_to_hz('C7')

pitch = 8  # I like the voice on 8, but feel free to experiment around!


# Function to correct the pitch of a fundamental frequency value
def correct(f0):
    if np.isnan(f0):
        return np.nan

    # Define the degrees of the musical notes in a scale
    note_degrees = librosa.key_to_degrees('C#:min')
    note_degrees = np.concatenate((note_degrees, [note_degrees[0] + 12]))

    # Convert the fundamental frequency to MIDI note value and calculate the closest degree
    midi_note = librosa.hz_to_midi(f0)
    degree = midi_note % 12
    closest_degree_id = np.argmin(np.abs(note_degrees - degree))

    # Correct the MIDI note value based on the closest degree and convert it back to Hz
    midi_note = midi_note - (degree - note_degrees[closest_degree_id])

    return librosa.midi_to_hz(midi_note - pitch)


# Function to correct the pitch of an array of fundamental frequencies
def correctpitch(f0):
    corrected_f0 = np.zeros_like(f0)
    for i in range(f0.shape[0]):
        corrected_f0[i] = correct(f0[i])
    return corrected_f0


# Function to perform pitch correction and autotune
def autotune(y, sr):
    # Estimate the fundamental frequency using the PYIN algorithm
    f0, _, _ = librosa.pyin(y, frame_length=frame_length_input, hop_length=(frame_length_input // 4),
                            sr=sr, fmin=fmin_input, fmax=fmax_input)
    # Correct the pitch of the estimated fundamental frequencies
    corrected_pitch = correctpitch(f0)
    # Perform PSOLA-based pitch shifting to match the corrected pitch
    return psola.vocode(y, sample_rate=int(sr), target_pitch=corrected_pitch, fmin=fmin_input, fmax=fmax_input)


# Main function to perform text-to-speech and pitch correction
def main(speakthis):
    # Generate the speech audio file using gTTS (Google Text-to-Speech)
    tts = gTTS(speakthis, tld="de", lang="de")
    tts.save('hello.mp3')

    # Convert the MP3 file to WAV format using pydub
    audio = AudioSegment.from_mp3('hello.mp3')
    audio.export('hello.wav', format="wav")

    # Load the WAV file using librosa
    y, sr = librosa.load("hello.wav", sr=None, mono=False)
    if y.ndim > 1:
        y = y[0, :]

    # Perform pitch correction by shifting the pitch by 2 semitones using librosa.effects.pitch_shift
    pitch_corrected_y = librosa.effects.pitch_shift(y, sr=sr, n_steps=2)
    
    pitch_corrected_y = autotune(y, sr)

    filepath = Path("hello.wav")
    output_filepath = (filepath.stem + "_pitch_corrected" + filepath.suffix)

    # Save the pitch-corrected audio file using soundfile
    sf.write(str(output_filepath), pitch_corrected_y, sr)

    # Remove the temporary audio files
    os.remove("hello.mp3")
    os.remove("hello.wav")


@app.route('/process', methods=['POST'])
def process():
    # Parse the request data and extract the text to be spoken
    debugdata = parse.parse_qs(request.data.decode('utf-8'))
    sprich = str(debugdata["INPUT_TEXT"])
    sprich = sprich.replace("['", "")
    sprich = sprich.replace("']", "")

    # Perform text-to-speech and pitch correction
    main(sprich)

    # Send the pitch-corrected audio file as a response
    return send_file("hello_pitch_corrected.wav", mimetype='audio/wav')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="59125")
