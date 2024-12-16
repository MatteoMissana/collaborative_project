import numpy as np  # For numerical operations and array handling
import sounddevice as sd  # For audio input/output (recording and playback)
import scipy.io.wavfile as wav  # For reading and writing .wav files
from scipy.signal import butter, lfilter  # For creating and applying signal filters
from jiwer import cer
from scipy.io.wavfile import read

# Function to record audio and save it to a .wav file
def registra_audio(durata=3, frequenza=44100, nome_file="registrazione.wav"):
    """
    Records audio for a specified duration and saves it to a .wav file.

    Parameters:
    - durata (int): Duration of the recording in seconds.
    - frequenza (int): Sampling rate in Hz.
    - nome_file (str): Name of the audio file to save.
    """
    print("Starting recording...")  # Notify user that recording is starting
    # Record audio with the specified duration and sampling rate, in mono (1 channel)
    audio = sd.rec(int(durata * frequenza), samplerate=frequenza, channels=1, dtype='int16')
    sd.wait()  # Wait for the recording to complete
    # Save the recorded audio as a .wav file
    wav.write(nome_file, frequenza, audio)
    print(f"Recording saved as '{nome_file}'.")  # Notify user that the file was saved

# Function to fetch the next audio frame from a stream
def get_next_audio_frame(stream, frame_length):
    """
    Reads the next audio frame from a real-time audio stream.

    Parameters:
    - stream: The audio stream to read from.
    - frame_length: The length of the audio frame.

    Returns:
    - A numpy array containing the audio frame.
    """
    pcm = stream.read(frame_length)[0]  # Read the frame from the stream
    pcm = np.squeeze(pcm)  # Remove single-dimensional entries for easier processing
    return pcm  # Return the processed audio frame

# Function to define a bandpass filter
def butter_bandpass(lowcut, highcut, fs, order=5):
    """
    Creates a bandpass filter with the specified parameters.

    Parameters:
    - lowcut (float): Lower cutoff frequency in Hz.
    - highcut (float): Upper cutoff frequency in Hz.
    - fs (int): Sampling rate in Hz.
    - order (int): Order of the filter.

    Returns:
    - b, a: The coefficients of the filter.
    """
    nyquist = 0.5 * fs  # Calculate the Nyquist frequency
    low = lowcut / nyquist  # Normalize the lower cutoff frequency
    high = highcut / nyquist  # Normalize the upper cutoff frequency
    b, a = butter(order, [low, high], btype='band')  # Create a bandpass filter
    return b, a  # Return the filter coefficients

# Function to apply a bandpass filter to an audio signal
def bandpass_filter(data, lowcut, highcut, fs, order=5):
    """
    Applies a bandpass filter to an audio signal.

    Parameters:
    - data: A numpy array containing the audio signal to filter.
    - lowcut: Lower cutoff frequency in Hz.
    - highcut: Upper cutoff frequency in Hz.
    - fs: Sampling rate in Hz.
    - order: Order of the filter.

    Returns:
    - The filtered audio signal.
    """
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)  # Get filter coefficients
    y = lfilter(b, a, data)  # Apply the filter to the audio signal
    return y  # Return the filtered signal

# Function triggered when a keyword is detected
def on_keyword_detected(keyword_index, sample_rate, model):
    """
    Action performed when a keyword is detected.

    Parameters:
    - keyword_index (int): Index of the detected keyword.
    - sample_rate (int): Sampling rate in Hz.
    """

    # Record a short audio segment upon keyword detection
    duration = 2  # Duration of the recording in seconds

    print(f"Keyword {keyword_index + 1} detected! Now recording for {duration} seconds...")

    # Read the WAV file
    samplerate, audio_data = read("beep_audio/short-beep-tone-47916.wav")

    extended_audio = np.concatenate([audio_data, audio_data])

    # Play the audio again (actual beep)
    sd.play(extended_audio, samplerate)
    sd.wait()

    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()  # Wait for the recording to finish

    # Apply a bandpass filter to the recorded audio
    filtered_audio = bandpass_filter(recording, 300, 3400, sample_rate)  # Filter human speech frequencies
    wav.write("filtered_audio.wav", sample_rate, filtered_audio.astype(np.int16))  # Save filtered audio

    result = model.transcribe("filtered_audio.wav")  # Perform transcription on the audio file
    print(f"Riconosciuto: {result['text']}")
    return result["text"]  # Return the transcribed text


def compare_with_commands(commands, detection, threshold=0.5):
    '''
    function that compares the detection of whisper model to a list of commands

    Parameters:
        - commands (list): List of commands to compare.
        - detection (string): detection that has to be compared to the commands
        - threshold (float): maximum error tolerated to have a match

    Outputs:
        - index (int): index of the command that has the minimum error
        - match (bool): True if there's a match
    '''
    match = False
    # inizialize the error
    error = [None] * len(commands)

    # for each command, verify the distance from the detected message
    for i, command in enumerate(commands):
        error[i] = cer(detection, command)
        if error[i] < threshold:
            match=True

    #if more than a command is similar to the detection i select the one with the lowest error
    best_error = min(error)  # get the minimum value
    index = error.index(best_error)  # get the index of the minimum

    return index, match

def beep():
    # Read the WAV file
    samplerate, audio_data = read("beep_audio/short-beep-tone-47916.wav")

    extended_audio = np.concatenate([audio_data, audio_data])

    # Play the audio again (actual beep)
    sd.play(extended_audio, samplerate)
    sd.wait()

def not_recognized():
    print("Comando non riconosciuto. Ripeti, per favore.")
    # Read the WAV file
    samplerate, audio_data = read("beep_audio/sofi_audio_4.wav")

    # Play the audio again (actual beep)
    sd.play(audio_data, samplerate)
    sd.wait()

def error_select_repetitive():
    print("Comando non riconosciuto. Ripeti, per favore.")
    # Read the WAV file
    samplerate, audio_data = read("beep_audio/repetitive_audio2.wav")

    # Play the audio again (actual beep)
    sd.play(audio_data, samplerate)
    sd.wait()