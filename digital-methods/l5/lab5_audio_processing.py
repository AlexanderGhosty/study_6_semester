import librosa
import librosa.display
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
import speech_recognition as sr
import os

print("Starting Lab 5...")

# 1. Load and Visualize audio
audio = 'music.wav'
print(f"Loading {audio}...")
waveform, sample_rate = librosa.load(audio)

plt.figure(figsize=(14, 5))
librosa.display.waveshow(waveform, sr=sample_rate)
plt.title('Waveform')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.savefig('waveform.png')
plt.close()
print("Saved waveform.png")

# 2. Harmonic and Percussive Separation
print("Separating harmonic and percussive sounds...")
y_harmonic, y_percussive = librosa.effects.hpss(waveform)

harmonic_file = 'harmonic.wav'
sf.write(harmonic_file, y_harmonic, sample_rate)
print(f"Saved {harmonic_file}")

percussive_file = 'percussive.wav'
sf.write(percussive_file, y_percussive, sample_rate)
print(f"Saved {percussive_file}")

# Visualizing Harmonic and Percussive Sounds (Combined)
plt.figure(figsize=(14, 5))
librosa.display.waveshow(y_harmonic, sr=sample_rate, alpha=0.5, label='Harmonic (Тональные)')
librosa.display.waveshow(y_percussive, sr=sample_rate, color='r', alpha=0.5, label='Percussive (Ударные)')
plt.title('Разделение: Гармонические и Ударные звуки (Совмещено)')
plt.xlabel('Время (с)')
plt.ylabel('Амплитуда')
plt.legend()
plt.savefig('hpss_waveform.png')
plt.close()
print("Saved hpss_waveform.png")

# Visualizing Harmonic Sound (Separate)
plt.figure(figsize=(14, 5))
librosa.display.waveshow(y_harmonic, sr=sample_rate, color='b')
plt.title('Гармонические (Тональные) звуки')
plt.xlabel('Время (с)')
plt.ylabel('Амплитуда')
plt.savefig('harmonic_waveform.png')
plt.close()
print("Saved harmonic_waveform.png")

# Visualizing Percussive Sound (Separate)
plt.figure(figsize=(14, 5))
librosa.display.waveshow(y_percussive, sr=sample_rate, color='r')
plt.title('Ударные (Перкуссионные) звуки')
plt.xlabel('Время (с)')
plt.ylabel('Амплитуда')
plt.savefig('percussive_waveform.png')
plt.close()
print("Saved percussive_waveform.png")

# 3. Create a Tone Sequence (Do-Re-Mi-Fa-Sol-La-Si)
print("Synthesizing tone sequence...")
duration = 0.5
frequencies = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88] # C D E F G A B
scale_sr = 44100
t = np.linspace(0, duration, int(scale_sr * duration), endpoint=False)

sequence = []
for freq in frequencies:
    tone = np.sin(2 * np.pi * freq * t)
    sequence.extend(tone)

sequence_np = np.array(sequence)
scale_file = 'scale.wav'
sf.write(scale_file, sequence_np, scale_sr)
print(f"Saved {scale_file}")

# 4. Spectrograms
print("Generating spectrograms...")
X = librosa.stft(waveform)
Xdb = librosa.amplitude_to_db(abs(X))

# Logarithmic
plt.figure(figsize=(14, 5))
librosa.display.specshow(Xdb, sr=sample_rate, x_axis='time', y_axis='log')
plt.colorbar()
plt.title('Spectrogram (Logarithmic scale)')
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.savefig('spectrogram_log.png')
plt.close()
print("Saved spectrogram_log.png")

# Linear
plt.figure(figsize=(14, 5))
librosa.display.specshow(Xdb, sr=sample_rate, x_axis='time', y_axis='linear')
plt.colorbar()
plt.title('Spectrogram (Linear scale)')
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.savefig('spectrogram_linear.png')
plt.close()
print("Saved spectrogram_linear.png")

# 5. Speech Recognition
print("Recognizing speech from voice.wav...")
r = sr.Recognizer()
voice_audio = "voice.wav"
if os.path.exists(voice_audio):
    with sr.AudioFile(voice_audio) as source:
        audio_data = r.record(source)
    try:
        text = r.recognize_google(audio_data, language="ru-RU")
        print(f"Recognized text: {text}")
    except sr.UnknownValueError:
        print("Could not recognize speech")
    except sr.RequestError as e:
        print(f"Speech recognition service error; {e}")
else:
    print(f"{voice_audio} not found.")

print("Lab 5 complete.")
