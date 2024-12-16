import pvporcupine
import sounddevice as sd
import utils.general as utils  # Import utils file with the needed functions
from utils.movements import Repetitive, Other_movement
from utils.wifi_connection import send_string_to_arduino
import whisper

# Commands definition
#robotic arm
commands = ["up fast", "up slow", "down fast", "down slow", "repetitive", "movement 1",
            "movement 2", "movement 3", "movement 4", "movement 5", "movement one", "movement two", "movement three",
            "movement four", "movement five"]

# save movement
commands_1 = ["position one", "position two", "position three", "position four", "position five",
              'position 1', 'position 2', 'position 3', 'position 4', 'position 5']

# amplitude change
commands_amplitude = ["shorter", "longer"]

#velocity change
commands_velocity = ["slower", "faster"]

# Use the Whisper model to transcribe the filtered audio
model = whisper.load_model("base")  # Load the Whisper transcription model


# Server configuration
arduino_ip = ("192.168.157.135")  # Insert Arduino IP address
arduino_port = 80           # Deve corrispondere alla porta configurata su Arduino

# Porcupine variables
access_key = "kIFt32liwTiKAA/2PW7z2BrsSh81BNsbi8wGk/Y8ss5coKZINR4Epg=="

keyword_paths = [r'rob_arm_weights\robotic-arm_en_windows_v3_0_0.ppn',
                 r'rob_arm_weights/robot-stop_en_windows_v3_0_0.ppn',
                 r'rob_arm_weights/save-movement_en_windows_v3_0_0.ppn',
                 r'rob_arm_weights/amplitude-change_en_windows_v3_0_0.ppn',
                 r'rob_arm_weights/velocity-change_en_windows_v3_0_0.ppn'] #change them if you have a mac

# txt path for saving movements
txtpath = 'movements/movements.txt'

#definisco
handle = pvporcupine.create(access_key=access_key, keyword_paths=keyword_paths)
sample_rate = handle.sample_rate
frame_length = handle.frame_length

with sd.InputStream(samplerate=sample_rate, channels=1, dtype='int16') as stream:
    print("Listening...")
    mov = None # Initialize as None to avoid errors when trying to save a movements and no movement selected
    while True:
        pcm_frame = utils.get_next_audio_frame(stream, frame_length) # Recalls the function from the utils file
        keyword_index = handle.process(pcm_frame)

        # If the keyword is detected
        if keyword_index >= 0:
            print(keyword_index)
            if keyword_index == 0: #ROBOTIC ARM
                # Function that returns the detected message
                detection = utils.on_keyword_detected(keyword_index, sample_rate, model)  # Recalls the function from the utils file

                if detection != '':

                    # Extract the best match from the commands list
                    index, match = utils.compare_with_commands(commands, detection)

                    if match:
                        comando_riconosciuto = commands[index]
                        print(f"Riconosciuto: {comando_riconosciuto}")

                        if comando_riconosciuto == 'up slow':
                            send_string_to_arduino('1', arduino_ip, arduino_port)
                            mov = Other_movement()

                        if comando_riconosciuto == 'up fast':
                            send_string_to_arduino('2', arduino_ip, arduino_port)
                            mov = Other_movement()

                        if comando_riconosciuto == 'down slow':
                            send_string_to_arduino('3', arduino_ip, arduino_port)
                            mov = Other_movement()

                        if comando_riconosciuto == 'down fast':
                            send_string_to_arduino('4', arduino_ip, arduino_port)
                            mov = Other_movement()

                        if comando_riconosciuto == 'repetitive':
                            mov = Repetitive(speed=3, amplitude=3, txt_path=txtpath)
                            char = mov.encode_numbers()
                            send_string_to_arduino(message=char, arduino_ip=arduino_ip, arduino_port=arduino_port)

                        if comando_riconosciuto == 'movement 1':
                            mov = Repetitive(speed=3, amplitude=3, txt_path=txtpath)
                            mov.load_from_txt(line_number = 0)
                            char = mov.encode_numbers()
                            send_string_to_arduino(message=char, arduino_ip=arduino_ip, arduino_port= arduino_port)

                        if comando_riconosciuto == 'movement 2':
                            mov = Repetitive(speed=3, amplitude=3, txt_path=txtpath)
                            mov.load_from_txt(line_number = 1)
                            char = mov.encode_numbers()
                            send_string_to_arduino(message=char, arduino_ip=arduino_ip, arduino_port= arduino_port)

                        if comando_riconosciuto == 'movement 3':
                            mov = Repetitive(speed=3, amplitude=3, txt_path=txtpath)
                            mov.load_from_txt(line_number = 2)
                            char = mov.encode_numbers()
                            send_string_to_arduino(message=char, arduino_ip=arduino_ip, arduino_port= arduino_port)

                        if comando_riconosciuto == 'movement 4':
                            mov = Repetitive(speed=3, amplitude=3, txt_path=txtpath)
                            mov.load_from_txt(line_number = 3)
                            char = mov.encode_numbers()
                            send_string_to_arduino(message=char, arduino_ip=arduino_ip, arduino_port= arduino_port)

                        if comando_riconosciuto == 'movement 5':
                            mov = Repetitive(speed=3, amplitude=3, txt_path=txtpath)
                            mov.load_from_txt(line_number = 4)
                            char = mov.encode_numbers()
                            send_string_to_arduino(message=char, arduino_ip=arduino_ip, arduino_port= arduino_port)

                    else: # the command is not in the list of possible commands
                        utils.not_recognized()
                else: #no word recognized
                    utils.not_recognized()

            elif keyword_index == 1:  # IF ROBOT STOP
                send_string_to_arduino('0', arduino_ip, arduino_port)

            elif keyword_index == 2:  # IF SAVE MOVEMENT

                # functions that returns the detected message
                detection = utils.on_keyword_detected(keyword_index, sample_rate, model)  # Richiama la funzione dal file utils

                print(f"Riconosciuto: {detection}")

                if detection != '':
                    if mov is not None:
                        # Extract the best match from the commands list
                        index, match = utils.compare_with_commands(commands_1, detection,0.8)
                        print(match, index)
                        if match:
                            comando_riconosciuto = commands_1[index]
                            print(comando_riconosciuto)
                            if comando_riconosciuto == 'position one' or comando_riconosciuto == 'position 1':
                                mov.save_settings(line_number=0)
                            if comando_riconosciuto == 'position two' or comando_riconosciuto == 'position 2':
                                mov.save_settings(line_number=1)
                            if comando_riconosciuto == 'position three' or comando_riconosciuto == 'position 3':
                                mov.save_settings(line_number=2)
                            if comando_riconosciuto == 'position four' or comando_riconosciuto == 'position 4':
                                mov.save_settings(line_number=3)
                            if comando_riconosciuto == 'position five' or comando_riconosciuto == 'position 5':
                                mov.save_settings(line_number=4)
                        else: #the command is not in the list
                            utils.not_recognized()
                    else:
                        utils.error_select_repetitive()

                else: # no word recognized
                    utils.not_recognized()

            elif keyword_index == 3:  # IF AMPLITUDE CHANGE
                # functions that returns the detected message
                detection = utils.on_keyword_detected(keyword_index, sample_rate, model)  # Richiama la funzione dal file utils

                if detection != '':
                    if mov is not None:
                        # extract the best match from the commands list
                        index, match = utils.compare_with_commands(commands_amplitude, detection,0.8)
                        if match:
                            comando_riconosciuto = commands_amplitude[index]
                            if comando_riconosciuto == commands_amplitude[0]:  # thinner
                                mov.amplitude_down()
                                send_string_to_arduino(mov.encode_numbers(), arduino_ip, arduino_port)

                            if comando_riconosciuto == commands_amplitude[1]:  # wider
                                mov.amplitude_up()
                                send_string_to_arduino(mov.encode_numbers(), arduino_ip, arduino_port)
                        else: # the command is not in the list
                            utils.not_recognized()
                    else: #no repetitive movement selected
                        utils.error_select_repetitive()
                else: #string recognized is ''
                    utils.not_recognized()

            elif keyword_index == 4:  # IF VELOCITY CHANGE
                # functions that returns the detected message
                detection = utils.on_keyword_detected(keyword_index, sample_rate, model)  # Richiama la funzione dal file utils

                if detection != '':  # extract the best match from the commands list
                    if mov is not None:
                        index, match = utils.compare_with_commands(commands_velocity, detection, 0.8)
                        if match:
                            comando_riconosciuto = commands_velocity[index]
                            if comando_riconosciuto == commands_velocity[0]:  # slower
                                mov.speed_down()
                                send_string_to_arduino(mov.encode_numbers(), arduino_ip, arduino_port)

                            if comando_riconosciuto == commands_velocity[1]:  # faster
                                mov.speed_up()
                                send_string_to_arduino(mov.encode_numbers(), arduino_ip, arduino_port)
                        else: #no match
                            utils.not_recognized()
                    else: # no movement selected
                        utils.error_select_repetitive()
                else: # detection = ''
                    utils.not_recognized()

#TODO:
# 1 nel paper che abbiamo visto io e matteo fanno una sorta di validation in 
# cui valutavano la precisione nel riconoscimento di ognuno dei comandi delineati, 
# facendo ripetere da soggetti non madrelingua (ergo noi eccetto sofia) il comando per 30 volte e 
# poi hanno mostrato l'accuratezza per far vedere quanto bene funzionava il loro modello
