#include <Servo.h>
#include <WiFiNINA.h>
#include <math.h>

#define PIN_POSITION A1  //A7

Servo myservo;

float posIs, posIsDeg,
  posServo1 = 0, posServo2 = 90,
  posSensor1 = 870, posSensor2 = 480;
const int servoPin = 5;  //era 9
const int servoOnPin = 7;
int angle = 0;
int init_angle = 0;

int pos_fin = 0;

int numSteps = 100;
bool flag = false;

// Configurazioni WiFi
const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";
String data;
int totalTime = 1500;
int delta = 5000;
float mu = numSteps / 2.0;
float sigma = 100;
int repetitive = 0;  //shows if we are doing a repetitive movement
int up = 0;          //going up or down (0 is down)
int command = 0;     // derivato da data
int amp, vel;        //movement amplitude
int init_time;

WiFiServer server(80);


int GaussDelay(int totaltime, int i) {
  int stepDelay;
  if (totaltime < 1400) {
    stepDelay = totaltime * 4.6050 * ((1.003 - exp(-(i - mu) * (i - mu) / (2 * (40 * 40)))) / (40 * sqrt(2 * 3.1415)));
  } else if (totaltime > 2000) {
    stepDelay = totaltime * 252000 * (((1.0001 - exp(-(i - mu) * (i - mu) / (2 * (2500 * 2500)))) / (2500 * sqrt(2 * 3.1415))) + 9 / totalTime / 252000);
  } else {
    stepDelay = totaltime * 4.3857 * ((1.003 - exp(-(i - mu) * (i - mu) / (2 * (40 * 40)))) / (40 * sqrt(2 * 3.1415)));
  }
  if (stepDelay < 2) {
    stepDelay = 2;
  }
  return stepDelay;
}

int decodeVel(int command) {
  if (command > 17) {
    command = (command - 17) / 5 + 1;
    if (command == 3) {
      return 1500;
    } else if (command < 3) {
      return 3000;
    } else {
      return 800;
    }
  } else {
    vel = 800;
    if (command % 2) {
      vel = 3000;
    }
    return vel;
  }
}
int readAngle() {
  return (((posServo2 - posServo1) / (posSensor2 - posSensor1)) * (analogRead(PIN_POSITION) - posSensor1) + posServo1);
}

void setup() {
  // put your setup code here, to run once:
  pinMode(servoOnPin, OUTPUT);
  digitalWrite(servoOnPin, HIGH);
  myservo.attach(servoPin);
  myservo.write(40);
  delay(1000);
  myservo.write(0);
  delay(1000);
  Serial.print("Connecting to WiFi...");
  while (WiFi.begin(ssid, password) != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nConnected!");

  Serial.begin(9600);
  while (!Serial)
    ;

  // Avvio del server
  server.begin();
  Serial.print("Server started. IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  // put your main code here, to run repeatedly:
  WiFiClient client = server.available();

  if (command == 0) {

    //Serial.println("Client connected!");

    // Legge i dati dal client e li inoltra alla seriale
    while (client.connected()) {
      if (client.available()) {

        data = client.readStringUntil('\n');  // Legge fino al terminatore di riga
        Serial.print("Received: ");
        Serial.println(data);  // Invia i dati ricevuti alla seriale
        //command = 1000;
        flag = true;
        client.flush();
      }
    }
  }
  if (flag) {
    flag = false;
    command = data[0] - '0';

    Serial.println(command);
    // Serial.print(",");
    //Serial.println(data);
    if (command < 17) {
      amp = 3;
      vel = decodeVel(command);
      repetitive = 0;
      up = 1;
      if (command > 2) {
        up = 0;
      }
    } else {
      vel = decodeVel(command);
      amp = (command - 17) % 5 + 1;
      repetitive = 1;
      up = 1;
    }
  }
  if (command > 0) {
    Serial.println(amp);
    Serial.println(command);
    Serial.println(repetitive);  // data = 1 up slow e 2 up fast
    //myservo.write(0);
    if (up) {
      init_angle = readAngle();
      pos_fin = init_angle + amp * 20;
      if (pos_fin > 90) {
        pos_fin = 90;
      }
      init_time = millis();
      for (int i = 0; i <= numSteps; i++) {

        angle = i * (pos_fin) / numSteps + init_angle;
        myservo.write(angle);
        delta = GaussDelay(vel, i);
        delay(delta);
        Serial.print(readAngle());
        Serial.print(",");
        Serial.print(delta);
        Serial.print(",");
        Serial.println((millis() - init_time));
        if (readAngle() >= pos_fin) {  //se posizione per approssimazione super posifn mi fermo
          break;
        }
      }
      if (repetitive) {
        up = 0;
      } else {
        command = 0;
      }
    }

    if (!up) {

      init_angle = readAngle();
      pos_fin = init_angle - amp * 20;
      if (pos_fin < 0) {
        pos_fin = 0;
      }
      init_time = millis();
      for (int i = 0; i <= numSteps; i++) {
        angle = init_angle - i * (init_angle - pos_fin) / numSteps;
        myservo.write(angle);
        delta = GaussDelay(vel, i);
        delay(delta);
        Serial.print(readAngle());
        Serial.print(",");
        Serial.print(delta);
        Serial.print(",");
        Serial.println((millis() - init_time));
        if (readAngle() <= pos_fin) {  //se posizione per approssimazione e' mano posifn mi fermo
          break;
        }
      }

      if (repetitive) {
        Serial.println("sono qui");
        up = 1;
        if (client.available()) {
          Serial.println("sono qua");
          data = client.readStringUntil('\n');
          command = data[0] - '0';
          Serial.print("New Command: ");
          Serial.println(command);
          client.flush();
          vel = decodeVel(command);
          amp = (command - 17) % 5 + 1;
          if (command < 17) {
            repetitive = 0;
          }
          if (command == 0) {
            myservo.write(0);
          }
        }
      } else {
        command = 0;
      }
    }
  }
}
