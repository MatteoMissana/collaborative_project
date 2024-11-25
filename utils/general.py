import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav
import whisper
from scipy.signal import butter, lfilter


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

#definizione del filtro passa banda e del filtraggio
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyquist = 0.5 * fs  # Frequenza di Nyquist
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

# Applicare il filtro al segnale
def bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def on_keyword_detected(keyword_index, sample_rate):
    print(f"Keyword {keyword_index + 1} detected! Now recording for 3 seconds...")

    # Registra per 3 secondi
    duration = 1 # in secondi
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()  # Attendi la fine della registrazione
    #wav.write("audio/detected_audio.wav", sample_rate, recording)  # Salva l'audio come file WAV

    #filtriamo l'audio con un passa banda
    filtered_audio = bandpass_filter(recording, 300, 3400, sample_rate)
    wav.write("filtered_audio.wav", sample_rate, filtered_audio.astype(np.int16))

    # Trascrivi l'audio con Whisper
    model = whisper.load_model("base") # Scegli il modello che preferisci
    result = model.transcribe("filtered_audio.wav")
    return result["text"]