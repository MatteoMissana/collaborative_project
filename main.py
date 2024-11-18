import pvporcupine
import sounddevice as sd
import utils.general as utils  # Importa il file utils con le funzioni
from utils.wifi_connection import send_string_to_arduino
from utils.nlp import calculate_wer

#inizialize the error
error = []

#initilize the threshold
threshold = 0.5

#comandi
commands = ['move the arm up', 'move the arm down']

# Configurazioni del server
arduino_ip = "192.168.157.29"  # Inserisci l'indirizzo IP di Arduino
arduino_port = 80           # Deve corrispondere alla porta configurata su Arduino

#%% porcupine variables
access_key = "kIFt32liwTiKAA/2PW7z2BrsSh81BNsbi8wGk/Y8ss5coKZINR4Epg=="
keyword_paths = [r'rob_arm_weights\robotic-arm_en_windows_v3_0_0.ppn'] #change it if you have a mac

#definisco
handle = pvporcupine.create(access_key=access_key, keyword_paths=keyword_paths)
sample_rate = handle.sample_rate
frame_length = handle.frame_length

with sd.InputStream(samplerate=sample_rate, channels=1, dtype='int16') as stream:
    print("Listening...")
    while True:
        pcm_frame = utils.get_next_audio_frame(stream, frame_length)  # Richiama la funzione dal file utils
        keyword_index = handle.process(pcm_frame)

        if keyword_index >= 0:
            detection = utils.on_keyword_detected(keyword_index, sample_rate)  # Richiama la funzione dal file utils

            print(detection)

            # for each command, verify the distance from the detected message
            for i, command in enumerate(commands):
                error[i] = calculate_wer(detection, command)
                if error < threshold:
                    match=True

            #if more than a command is similar to the detection i select the one with the lowest error
            best_error = min(error)  # get the minimum value
            index = error.index(best_error)  # get the index of the minimum


            if match:
                comando_riconosciuto = commands[index]
                print(f"Riconosciuto: {comando_riconosciuto}")

                if comando_riconosciuto == 'move the arm down':
                    send_string_to_arduino('down', arduino_ip, arduino_port)

                if comando_riconosciuto == 'move the arm up':
                    send_string_to_arduino('up', arduino_ip, arduino_port)
            else:
                print("Comando non riconosciuto. Ripeti, per favore.")

            match = False


#TODO:
# 1 nel paper che abbiamo visto io e matteo fanno una sorta di validation in 
# cui valutavano la precisione nel riconoscimento di ognuno dei comandi delineati, 
# facendo ripetere da soggetti non madrelingua (ergo noi eccetto sofia) il comando per 30 volte e 
# poi hanno mostrato l'accuratezza per far vedere quanto bene funzionava il loro modello
