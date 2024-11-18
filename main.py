import pvporcupine
import sounddevice as sd
import utils.general as utils  # Importa il file utils con le funzioni
from utils.wifi_connection import send_string_to_arduino
import difflib

#comandi
commands = ['move the arm up', 'move the arm down']

# Configurazioni del server
arduino_ip = "192.168.157.29"  # Inserisci l'indirizzo IP di Arduino
arduino_port = 80           # Deve corrispondere alla porta configurata su Arduino

#%% porcupine variables
access_key = "kIFt32liwTiKAA/2PW7z2BrsSh81BNsbi8wGk/Y8ss5coKZINR4Epg=="
keyword_paths = [r'rob_arm_weights\robotic-arm_en_windows_v3_0_0.ppn'] #change it if you have a mac

handle = pvporcupine.create(access_key=access_key, keyword_paths=keyword_paths)
sample_rate = handle.sample_rate
frame_length = handle.frame_length

with sd.InputStream(samplerate=sample_rate, channels=1, dtype='int16') as stream:
    print("Listening...")
    while True:
        pcm_frame = utils.get_next_audio_frame(stream, frame_length)  # Richiama la funzione dal file utils
        keyword_index = handle.process(pcm_frame)

        if keyword_index >= 0:
            messaggio = utils.on_keyword_detected(keyword_index, sample_rate)  # Richiama la funzione dal file utils

            print(messaggio)
            # TODO: qui serve tutta una parte in cui si verifica la similarità con i comandi (direi di mettere una soglia bella alta)
            # - poi bisogna fare un ii else lungo in cui per ogni comando si decide una stringa da inviare all'arduino
            # - (direi un solo carattere per stringa)
            # - per ora invio direttamente il messaggio registrato all'arduino, poi va modificato

            match = difflib.get_close_matches(
                messaggio, commands, n=1, cutoff=0.6  # Soglia alta per accuratezza
            )

            if match:
                comando_riconosciuto = match[0]
                print(f"Riconosciuto: {comando_riconosciuto}")

                if comando_riconosciuto == 'move the arm down':
                    send_string_to_arduino('down', arduino_ip, arduino_port)

                if comando_riconosciuto == 'move the arm up':
                    send_string_to_arduino('up', arduino_ip, arduino_port)
            else:
                print("Comando non riconosciuto. Ripeti, per favore.")


