#include<Servo.h>
#include <WiFiNINA.h>

Servo myservo;
const int servoAnalogInPin = A7;
float posIs, posIsDeg,
      posServo1 = 0, posServo2 = 90,
      posSensor1 = 800, posSensor2 = 373;

float angle = 0;
float init_angle = 0;

float pos_fin = 0;
float delta = 0;

// Configurazioni WiFi
const char* ssid = "POCO";
const char* password = "11111111";
String data = "0";

WiFiServer server(80);

void setup() {
  // put your setup code here, to run once:

  Serial.print("Connecting to WiFi...");
  while (WiFi.begin(ssid, password) != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nConnected!");

  Serial.begin(9600);
  while(!Serial);
  //pinMode(servoOnPin, OUTPUT);
  //digitalWrite(servoOnPin, HIGH);

  // Avvio del server
  server.begin();
  Serial.print("Server started. IP address: ");
  Serial.println(WiFi.localIP());

}

void loop() {
  // put your main code here, to run repeatedly:
  
  WiFiClient client = server.available();

  if(data == "0") {
    if (client) {
        Serial.println("Client connected!");

        // Legge i dati dal client e li inoltra alla seriale
        while (client.connected()) {
          if (client.available()) {
            
            data = client.readStringUntil('\n'); // Legge fino al terminatore di riga
            Serial.print("Received: ");
            Serial.println(data);  // Invia i dati ricevuti alla seriale
          
          }
        }
    }
    client.stop();
    //Serial.println("Client disconnected.");
  } else if(data == "up") {
    pos_fin = 100;
    init_angle = ((posServo2-posServo1)/(posSensor2-posSensor1))*(analogRead(servoAnalogInPin)-posSensor1)+posServo1;
    
    for(int i = 0 ; i < 100 ; i++) {
      delta = (pos_fin - current_angle)/100;
      myservo.write(init_angle + delta);
      delay(10);
      if(analogRead(servoAnalogInPin) = pos_fin) {
        break;
      }
    }
    myservo.write();
    data = "0";
  } else if(data == "down") {
    
    data = "0";
  } else if (data != "up" || data != "down") {
    data = "0";
  } 
}
