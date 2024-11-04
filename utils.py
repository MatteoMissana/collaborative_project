import sounddevice as sd
from scipy.io.wavfile import write


def registra_audio(durata=3, frequenza=44100, nome_file="registrazione.wav"):
    """
    Registra un audio per un tempo specificato e lo salva in un file .wav.

    Parametri:
    - durata (int): Durata della registrazione in secondi.
    - frequenza (int): Frequenza di campionamento (in Hz).
    - nome_file (str): Nome del file audio da salvare.
    """
    print("Inizio registrazione...")
    audio = sd.rec(int(durata * frequenza), samplerate=frequenza, channels=2, dtype='int16')
    sd.wait()  # Aspetta che la registrazione finisca
    write(nome_file, frequenza, audio)  # Salva l'audio in un file WAV
    print(f"Registrazione salvata come '{nome_file}'.")