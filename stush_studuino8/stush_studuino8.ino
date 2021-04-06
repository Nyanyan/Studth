#include <Servo.h>

// [No.1, No.2, No.3, No.4]
const int cgrb[4] = {105, 105, 100, 105};
const int crls[4] = {80, 80, 75, 70};
const int crls_big[4] = {40, 40, 25, 30};
const int crot_l[4] = {180, 180, 180, 180};
const int crot_r[4] = {85, 85, 85, 85};

//const int coffset_grb[4] = {-15, -15, -10, -10};
const int coffset_grb[4] = {0, 0, 0, 0};
const int coffset_rot[4] = {-10, -10, 0, -10};

int grb[4];
int rls[4];
int rls_big[4];
int rot_l[4];
int rot_r[4];

char buf[30];
int idx = 0;
long data[2];

Servo arm_grab[4];
Servo arm_rot[4];


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

  for (int i = 0;i < 4;i++) {
    grb[i] = cgrb[i] + coffset_grb[i];
    rls[i] = crls[i] + coffset_grb[i];
    rls_big[i] = crls_big[i] + coffset_grb[i];
    rot_l[i] = crot_l[i] + coffset_rot[i];;
    rot_r[i] = crot_r[i] + coffset_rot[i];;
  }
  
  arm_rot[0].attach(11, 500, 2500);
  arm_grab[0].attach(12, 500, 2500);
  arm_rot[1].attach(7, 500, 2500);
  arm_grab[1].attach(8, 500, 2500);
  arm_rot[2].attach(9, 500, 2500);
  arm_grab[2].attach(10, 500, 2500);
  arm_rot[3].attach(2, 500, 2500);
  arm_grab[3].attach(4, 500, 2500);

  
  for (int i = 0; i < 4; i++) arm_rot[i].write(rot_l[i]);
  for (int i = 0; i < 4; i++) arm_grab[i].write(grb[i]);
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
