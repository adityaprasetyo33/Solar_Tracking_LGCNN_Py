#include <Servo.h>

Servo servoAtas;  // create servo object to control a servo
Servo servoBawah;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 0;    // variable to store the servo position
int kelasLama = 0;
int atas = 0;
int atasLama = 0;
int bawah = 0;
int bawahLama = 0;

void setup() {
  Serial.begin(9600);
  servoAtas.attach(9);  // attaches the servo on pin 9 to the servo object
  servoBawah.attach(10);  // attaches the servo on pin 9 to the servo object
}

void loop() {
  for (int kelas = 1; kelas <= 9; kelas += 1) { // goes from 0 degrees to 180 degrees
    if (kelas == 1) {
      atas = 90;
      bawah = 135;
    }
    if (kelas == 2) {
      atas = 45;
      bawah = 135;
    }
    if (kelas == 3) {
      atas = 45;
      bawah = 90;
    }
    if (kelas == 4) {
      atas = 45;
      bawah = 45;
    }
    if (kelas == 5) {
      atas = 45;
      bawah = 0;
    }
    if (kelas == 6) {
      atas = 135;
      bawah = 135;
    }
    if (kelas == 7) {
      atas = 135;
      bawah = 90;
    }
    if (kelas == 8) {
      atas = 135;
      bawah = 45;
    }
    if (kelas == 9) {
      atas = 135;
      bawah = 0;
    }
    Serial.println(kelas);
    if (kelas != kelasLama) {
      if (bawah > bawahLama) {
        for (pos = bawahLama; pos <= bawah; pos += 5) { // goes from 180 degrees to 0 degrees
          servoBawah.write(pos);
          delay(15);                       // waits 15 ms for the servo to reach the position
        }
      }
      if (bawah < bawahLama) {
        for (pos = bawahLama; pos >= bawah; pos -= 5) { // goes from 180 degrees to 0 degrees
          servoBawah.write(pos);
          delay(15);                       // waits 15 ms for the servo to reach the position
        }
      }
      if (atas > atasLama) {
        for (pos = atasLama; pos <= atas; pos += 5) {
          servoAtas.write(pos);
          delay(15);
        }
      }
      if (atas < atasLama) {
        for (pos = atasLama; pos >= atas; pos -= 5) { // goes from 180 degrees to 0 degrees
          servoAtas.write(pos);
          delay(15);                       // waits 15 ms for the servo to reach the position
        }
      }
      Serial.println(atas);
      Serial.println(atasLama);
      Serial.println(bawah);
      Serial.println(bawahLama);
      atasLama = atas;
      bawahLama = bawah;
      kelasLama = kelas;
    }
    delay(1000);
  }
}
