import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav
import whisper


def registra_audio(durata=3, frequenza=44100, nome_file="registrazione.wav"):
    """
    Registra un audio di durata specificata e lo salva in un file .wav.

    Parametri:
    - durata (int): Durata della registrazione in secondi.
    - frequenza (int): Frequenza di campionamento in Hz.
    - nome_file (str): Nome del file audio da salvare.
    """
    print("Inizio registrazione...")
    audio = sd.rec(int(durata * frequenza), samplerate=frequenza, channels=1, dtype='int16')
    sd.wait()  # Attende la fine della registrazione
    wav.write(nome_file, frequenza, audio)
    print(f"Registrazione salvata come '{nome_file}'.")

def get_next_audio_frame(stream, frame_length):
    pcm = stream.read(frame_length)[0]
    pcm = np.squeeze(pcm)
    return pcm

def on_keyword_detected(keyword_index, sample_rate):
    print(f"Keyword {keyword_index + 1} detected! Now recording for 3 seconds...")

    # Registra per 3 secondi
    duration = 3  # in secondi
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()  # Attendi la fine della registrazione
    wav.write("audio/detected_audio.wav", sample_rate, recording)  # Salva l'audio come file WAV

    # Trascrivi l'audio con Whisper
    model = whisper.load_model("tiny")  # Scegli il modello che preferisci
    result = model.transcribe("audio/detected_audio.wav")
    return result["text"]