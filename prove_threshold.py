import pvporcupine
import sounddevice as sd
import utils.general as utils  # Importa il file utils con le funzioni
#from utils.wifi_connection import send_string_to_arduino
import difflib
# Configurazioni del server
arduino_ip = "192.168.157.29"  # Inserisci l'indirizzo IP di Arduino
arduino_port = 80              # Deve corrispondere alla porta configurata su Arduino

# Definisci i comandi e le pose predefiniti
commands = ['up', 'down']
poses = ['home', 'mouth']

# Porcupine variables
access_key = "kIFt32liwTiKAA/2PW7z2BrsSh81BNsbi8wGk/Y8ss5coKZINR4Epg=="
keyword_paths =[ '/Users/home/Desktop/collaborative_project/rob_arm_weights/robotic_arm.ppn' ]

handle = pvporcupine.create(access_key=access_key, keyword_paths=keyword_paths)

sample_rate = handle.sample_rate
frame_length = handle.frame_length


with sd.InputStream(samplerate=sample_rate, channels=1, dtype='int16') as stream:
    print("Listening...")
    while True:
        pcm_frame = utils.get_next_audio_frame(stream, frame_length)  # Richiama la funzione dal file utils
        keyword_index = handle.process(pcm_frame)

        if keyword_index >= 0:
            # `on_keyword_detected` restituisce il testo del comando rilevato
            messaggio = utils.on_keyword_detected(keyword_index, sample_rate)  # Funzione nel file utils
            print("Detected message:", messaggio)

            # Trova il comando o la posa più simile al messaggio rilevato
            match = difflib.get_close_matches(
                messaggio, commands + poses, n=1, cutoff=0.8  # Soglia alta per accuratezza
            )
            
            if match:
                comando_riconosciuto = match[0]
                print(f"Riconosciuto: {comando_riconosciuto}")
                
                # Manda il comando riconosciuto ad Arduino
                #send_string_to_arduino(comando_riconosciuto, arduino_ip, arduino_port)
            else:
                print("Comando non riconosciuto. Ripeti, per favore.")
