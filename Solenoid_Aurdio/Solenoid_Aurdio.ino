int Solenoid = 6;

void setup() {
  // put your setup code here, to run once:
  pinMode(Solenoid, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(Solenoid, HIGH); 
  //delay(2000); //2s
  //digitalWrite(Solenoid,LOW);
  //delay(2000);

}
