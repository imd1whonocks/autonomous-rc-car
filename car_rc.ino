int left_sideD2 = 11;//D2 on RF board
int right_sideD0 = 9; //D0 on RF board

// duration for output
int time = 1000;
// initial command
String command = "";

void setup() {
  // put your setup code here, to run once:
  Serial.begin(250000);
  pinMode(left_sideD2,OUTPUT);
  pinMode(right_sideD0,OUTPUT);
  
}

void loop() {
  if (Serial.available() > 0){
    command = Serial.readStringUntil('\n');
    Serial.print(command);
    if(command.equals("forward")){
      forward(time);
    }
    else if(command.equals("left")){
      left(time);
    }
    else if(command.equals("right")){
      right(time);
    }
    else if(command.equals("brake")){
      brake(time);
    }
  }
  else{
    reset();
    //Serial.print('reset');
  }
}

void forward(int time){
  digitalWrite(left_sideD2, HIGH);
  digitalWrite(right_sideD0, HIGH);
  delay(time);
}

void right(int time){
  digitalWrite(left_sideD2, HIGH);
  delay(time);
}

void left(int time){
  digitalWrite(right_sideD0, HIGH);
  delay(time);
}
void reset(){
  digitalWrite(left_sideD2, LOW);
  digitalWrite(right_sideD0, LOW);
}
void brake(int time){
  digitalWrite(left_sideD2, LOW);
  digitalWrite(right_sideD0, LOW);
  delay(time);  
}
