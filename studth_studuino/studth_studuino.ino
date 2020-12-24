#include <Servo.h>
Servo servo0;
Servo servo1;



void setup() {
  servo0.attach(7);
  servo1.attach(8);
  
  servo0.write(180);
  servo1.write(70);
  delay(500);
  servo0.write(180);
  servo1.write(100);
  delay(500);
  servo0.write(90);
  servo1.write(100);
  delay(500);
  servo0.write(90);
  servo1.write(70);
  delay(500);
  servo0.write(180);
  servo1.write(70);
  delay(500);
  servo0.write(180);
  servo1.write(100);
  delay(500);
}

void loop() {
}
