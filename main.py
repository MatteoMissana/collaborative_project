import pvporcupine
import sounddevice as sd
import utils.general as utils  # Importa il file utils con le funzioni

access_key = "kIFt32liwTiKAA/2PW7z2BrsSh81BNsbi8wGk/Y8ss5coKZINR4Epg=="
keyword_paths = [r'C:\Users\User\cartelle_matteo\collaborative_project\rob_arm_weights\robotic-arm_en_windows_v3_0_0.ppn']

handle = pvporcupine.create(access_key=access_key, keyword_paths=keyword_paths)
sample_rate = handle.sample_rate
frame_length = handle.frame_length

with sd.InputStream(samplerate=sample_rate, channels=1, dtype='int16') as stream:
    print("Listening...")
    while True:
        pcm_frame = utils.get_next_audio_frame(stream, frame_length)  # Richiama la funzione dal file utils
        keyword_index = handle.process(pcm_frame)

        if keyword_index >= 0:
            utils.on_keyword_detected(keyword_index, sample_rate)  # Richiama la funzione dal file utils