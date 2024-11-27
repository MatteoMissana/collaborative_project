import pvporcupine
import sounddevice as sd
import utils.general as utils  # Importa il file utils con le funzioni
from utils.movements import Repetitive
from utils.wifi_connection import send_string_to_arduino

# commands
commands = ["up fast", "up intermediate", "up slow", "down fast", "down intermediate", "down slow", "repetitive", "movement 1",
            "movement 2", "movement 3", "movement 4", "movement 5", "save movement"]

commands_1 = ["position one", "position two", "position three", "position four", "position five",
              'position 1', 'position 2', 'position 3', 'position 4', 'position 5']


# Configurazioni del server
arduino_ip = "192.168.157.29"  # Inserisci l'indirizzo IP di Arduino
arduino_port = 80           # Deve corrispondere alla porta configurata su Arduino

# porcupine variables
access_key = "kIFt32liwTiKAA/2PW7z2BrsSh81BNsbi8wGk/Y8ss5coKZINR4Epg=="

keyword_paths = [r'rob_arm_weights\robotic-arm_en_windows_v3_0_0.ppn',
                 r'rob_arm_weights/robot-stop_en_windows_v3_0_0.ppn',
                 r'rob_arm_weights/save-movement_en_windows_v3_0_0.ppn'] #change them if you have a mac

# txt path for saving movements
txtpath = 'movements/movements.txt'

#definisco
handle = pvporcupine.create(access_key=access_key, keyword_paths=keyword_paths)
sample_rate = handle.sample_rate
frame_length = handle.frame_length

with sd.InputStream(samplerate=sample_rate, channels=1, dtype='int16') as stream:
    print("Listening...")
    while True:
        pcm_frame = utils.get_next_audio_frame(stream, frame_length) # Richiama la funzione dal file utils
        keyword_index = handle.process(pcm_frame)

        #if keyword is detected
        if keyword_index >= 0:
            print(keyword_index)
            if keyword_index == 0:
                #functions that returns the detected message
                detection = utils.on_keyword_detected(keyword_index, sample_rate)  # Richiama la funzione dal file utils

                if detection != '':

                    # extract the best match from the commands list
                    index, match = utils.compare_with_commands(commands, detection)

                    if match:
                        comando_riconosciuto = commands[index]
                        print(f"Riconosciuto: {comando_riconosciuto}")

                        if comando_riconosciuto == 'up slow':
                            send_string_to_arduino('0', arduino_ip, arduino_port)

                        if comando_riconosciuto == 'up fast':
                            send_string_to_arduino('1', arduino_ip, arduino_port)

                        if comando_riconosciuto == 'up intermediate':
                            send_string_to_arduino('2', arduino_ip, arduino_port)

                        if comando_riconosciuto == 'down slow':
                            send_string_to_arduino('3', arduino_ip, arduino_port)

                        if comando_riconosciuto == 'down fast':
                            send_string_to_arduino('4', arduino_ip, arduino_port)

                        if comando_riconosciuto == 'down intermediate':
                            send_string_to_arduino('5', arduino_ip, arduino_port)

                        if comando_riconosciuto == 'repetitive':
                            rep_mov = Repetitive(speed=3, amplitude=3, txt_path=txtpath)
                            send_string_to_arduino('6', arduino_ip, arduino_port)

                        if comando_riconosciuto == 'save movement':
                            print('nothing')
                            #TODO: pensare a come cazzo fare per salvare il movimento

                else:
                    print("Comando non riconosciuto. Ripeti, per favore.")
            elif keyword_index == 1:
                print('stoooooooooooooooop')
                send_string_to_arduino('s', arduino_ip, arduino_port)

            elif keyword_index == 2:
                # functions that returns the detected message
                detection = utils.on_keyword_detected(keyword_index, sample_rate)  # Richiama la funzione dal file utils

                print(f"Riconosciuto: {detection}")

                if detection != '':
                    # extract the best match from the commands list
                    index, match = utils.compare_with_commands(commands_1, detection,0.8)
                    print(match, index)
                    if match:
                        comando_riconosciuto = commands_1[index]
                        print(comando_riconosciuto)
                        if comando_riconosciuto == 'position one' or comando_riconosciuto == 'position 1':
                            print("elisone")
                        if comando_riconosciuto == 'position two' or comando_riconosciuto == 'position 2':
                            print("elistwo")
                        if comando_riconosciuto == 'position three' or comando_riconosciuto == 'position 3':
                            print("elisthtree")
                        if comando_riconosciuto == 'position four' or comando_riconosciuto == 'position 4':
                            print("elisfour")
                        if comando_riconosciuto == 'position five' or comando_riconosciuto == 'position 5':
                            print("elisfive")


#TODO:
# 1 nel paper che abbiamo visto io e matteo fanno una sorta di validation in 
# cui valutavano la precisione nel riconoscimento di ognuno dei comandi delineati, 
# facendo ripetere da soggetti non madrelingua (ergo noi eccetto sofia) il comando per 30 volte e 
# poi hanno mostrato l'accuratezza per far vedere quanto bene funzionava il loro modello
