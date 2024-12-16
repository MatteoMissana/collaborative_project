#include<Servo.h>
#include <WiFiNINA.h>
#include<math.h>

Servo myservo;
const int servoAnalogInPin = A7;
float posIs, posIsDeg,
      posServo1 = 0, posServo2 = 90,
      posSensor1 = 800, posSensor2 = 373;
const int servoPin = 9;

int angle = 0;
int init_angle = 0;

int pos_fin = 0;
int delta = 0;

int numSteps = 100;

// Configurazioni WiFi
const char* ssid = "POCO";
const char* password = "11111111";
int data = 1;
int totalTime = 5000;
int stepDelay = 5000;
//WiFiServer server(80);

void setup() {
  // put your setup code here, to run once:

  Serial.print("Connecting to WiFi...");
*while (WiFi.begin(ssid, password) != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nConnected!");

  Serial.begin(9600);
  while(!Serial);
  
  //pinMode(servoOnPin, OUTPUT);
  //digitalWrite(servoOnPin, HIGH);

  // Avvio del server
  //server.begin();
  //Serial.print("Server started. IP address: ");
  //Serial.println(WiFi.localIP());
  myservo.attach(servoPin);
  myservo.write(10);
  delay(1000);
  myservo.write(0);
  delay(1000);
  

}

void loop() {
  // put your main code here, to run repeatedly:
  float mu = numSteps / 2.0;
  float sigma = 60; 
  
  //WiFiClient client = server.available();

  if(data == 0) {
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
  } else if(data == 1 || data == 2) { // data = 1 up slow e 2 up fast
    delay(3000);
    pos_fin = 100;
    //init_angle = ((posServo2-posServo1)/(posSensor2-posSensor1))*(analogRead(servoAnalogInPin)-posSensor1)+posServo1;
    myservo.write(0);
    for(int i = 0 ; i <= numSteps ; i++) {

      angle = i*(pos_fin)/numSteps;

      myservo.write(angle);
      if(data == 1) {
        stepDelay = totalTime * (1 - exp(-(i - mu)*(i - mu) / (2 * (sigma*sigma)))) / (sigma * sqrt(2 * 3.1415));
      } elif(data == 2) {
        stepDelay = totalTime/3 * (1 - exp(-(i - mu)*(i - mu) / (2 * (sigma*sigma)))) / (sigma * sqrt(2 * 3.1415));
      }
      if (stepDelay<5){stepDelay=5;}
      Serial.print(stepDelay); Serial.print(";"); Serial.println(angle);
      delay(stepDelay);
      if((((posServo2-posServo1)/(posSensor2-posSensor1))*(analogRead(servoAnalogInPin)-posSensor1)+posServo1) >= pos_fin) {
        break;
      }
    }
    data = 2;
  } else if(data == 2) {
    delay(3000);
    pos_fin = 10;
    init_angle = ((posServo2-posServo1)/(posSensor2-posSensor1))*(analogRead(servoAnalogInPin)-posSensor1)+posServo1;
    for(int i = 0 ; i <= numSteps ; i++) {
      angle = init_angle - i*(pos_fin - init_angle)/numSteps;

      myservo.write(angle);
      int stepDelay = totalTime * (1 - exp(-(i - mu)*(i - mu) / (2 * (sigma*sigma)))) / (sigma * sqrt(2 * 3.1415));
      if (stepDelay<5){stepDelay=5;}
      Serial.print(stepDelay); Serial.print(";"); Serial.println(angle);
      delay(stepDelay);
      if((((posServo2-posServo1)/(posSensor2-posSensor1))*(analogRead(servoAnalogInPin)-posSensor1)+posServo1) <= pos_fin) {
        break;
      }
    }
    data = 0;
  } else if (data != 1 || data != 2) {
    data = 0;
  } 
}

int setTotaltime(int set_1, int set_2, int current_set, int total_time){
  if(current_set == set_1) {
    return total_time;
  } elif(current_set == set_2) {
    return total_time/3;
  }
}

int decode(String data) {
  if()
}
