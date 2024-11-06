#include <SPI.h>
#include <WiFiNINA.h>

// Configurazioni WiFi
const char* ssid = "TUA_RETE_WIFI";
const char* password = "TUA_PASSWORD";

// Configurazioni del server
WiFiServer server(80);  // Usa la porta 80 per HTTP

void setup() {
  Serial.begin(9600);

  // Connessione alla rete WiFi
  Serial.print("Connecting to WiFi...");
  while (WiFi.begin(ssid, password) != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nConnected!");

  // Avvio del server
  server.begin();
  Serial.print("Server started. IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  // Controlla se un client è connesso
  WiFiClient client = server.available();
  if (client) {
    Serial.println("Client connected!");

    // Legge i dati dal client e li inoltra alla seriale
    while (client.connected()) {
      if (client.available()) {
        String data = client.readStringUntil('\n'); // Legge fino al terminatore di riga
        Serial.print("Received: ");
        Serial.println(data);  // Invia i dati ricevuti alla seriale
      }
    }

    // Chiudi la connessione una volta che il client è disconnesso
    client.stop();
    Serial.println("Client disconnected.");
  }
}
