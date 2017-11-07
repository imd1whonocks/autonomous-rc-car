int left_sideD0 = 8;        //D0 on RF board
int rev_left_sideD1 = 9;    //D1 on RF board
int right_sideD2 = 10;      //D2 on RF board
int rev_right_sideD3 = 11;  //D3 on RF board

// duration for output
int time = 1000;
// initial command
String command = "";

void setup() {
  // put your setup code here, to run once:
  Serial.begin(250000);
  pinMode(left_sideD0,OUTPUT);
  pinMode(rev_left_sideD1,OUTPUT);
  pinMode(right_sideD2,OUTPUT);
  pinMode(rev_right_sideD3,OUTPUT)
  
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
  digitalWrite(left_sideD0, HIGH);
  digitalWrite(right_sideD2, HIGH);
  delay(time);
}

void right(int time){
  digitalWrite(left_sideD0, HIGH);
  delay(time);
}

void left(int time){
  digitalWrite(right_sideD2, HIGH);
  delay(time);
}

void reset(){
  digitalWrite(left_sideD0, LOW);
  digitalWrite(rev_left_sideD1, LOW);
  digitalWrite(rev_right_sideD3, LOW);
  digitalWrite(right_sideD2, LOW);
}

void brake(int time){
  digitalWrite(rev_left_sideD1, HIGH);
  digitalWrite(rev_right_sideD3, HIGH);
  delay(time);  
}
