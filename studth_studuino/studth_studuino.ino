#include <Servo.h>

const int offset = 10;

const int offset_0 = 0;
const int offset_1 = 0;


/* for arm 2 and 3 */
const int grb[2] = {100+offset_0, 105+offset_1};
const int rls[2] = {75+offset_0, 70+offset_1};
const int rls_big[2] = {25+offset_0, 30+offset_1};
const int rot_l[2] = {180, 180};
const int rot_r[2] = {85, 85};

/* for arm 0 and 1 
const int grb[2] = {105, 100};
const int rls[2] = {65, 70};
const int rls_big[2] = {30, 30};
const int rot_l[2] = {180, 180};
const int rot_r[2] = {75, 85};
*/

char buf[30];
int idx = 0;
long data[2];

Servo arm_grab[2];
Servo arm_rot[2];


void move_motor(int num, int gl) {
  if(gl == 1)arm_rot[num].write(rot_r[num]);
  else arm_rot[num].write(rot_l[num]);
}


void release_arm(int num) {
  arm_grab[num].write(rls[num]);
}

void grab_arm(int num) {
  arm_grab[num].write(grb[num]);
}

void release_big_arm(int num) {
  arm_grab[num].write(rls_big[num]);
}


void setup() {
  Serial.begin(115200);
  arm_rot[0].attach(7);
  arm_grab[0].attach(8);
  arm_rot[1].attach(11);
  arm_grab[1].attach(12);
  for (int i = 0; i < 2; i++) arm_rot[i].write(rot_l[i]);
  for (int i = 0; i < 2; i++) arm_grab[i].write(grb[i]);
}

void loop() {
  while (1) {
    if (Serial.available()) {
      buf[idx] = Serial.read();
      if (buf[idx] == '\n') {
        buf[idx] = '\0';
        data[0] = atoi(strtok(buf, " "));
        data[1] = atoi(strtok(NULL, " "));
        if (data[1] == 1000) grab_arm(data[0]);
        else if (data[1] == 2000) release_arm(data[0]);
        else if (data[1] == 3000) release_big_arm(data[0]);
        else move_motor(data[0], data[1]);
        idx = 0;
      }
      else {
        idx++;
      }
    }
  }
  /*
  delay(1000);
  arm_rot[0].write(rot_r[0]);
  delay(300);
  arm_grab[0].write(rls[0]);
  delay(100);
  arm_rot[0].write(rot_l[0]);
  delay(300);
  arm_grab[0].write(grb[0]);
  */
}
