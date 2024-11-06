import socket

def send_string_to_arduino(message, arduino_ip, arduino_port):
    try:
        # Crea un socket TCP/IP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Connessione al server
            sock.connect((arduino_ip, arduino_port))
            print("Connesso al server Arduino.")

            # Invia il messaggio come bytes
            sock.sendall((message + "\n").encode('utf-8'))  # Aggiungi il terminatore di riga

            print(f"Messaggio inviato: {message}")

    except Exception as e:
        print(f"Errore nella connessione: {e}")