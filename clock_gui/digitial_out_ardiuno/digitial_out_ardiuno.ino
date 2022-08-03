
#define TRIGGER_PIN 12
byte trigger;


void setup() {
 pinMode(TRIGGER_PIN, OUTPUT);
 
 Serial.begin(115200);
 Serial.setTimeout(1);
// while (!Serial) {};  // wait for connection
 digitalWrite(TRIGGER_PIN, LOW);
}


void loop() {
 while (!Serial.available());
 trigger = Serial.read();
 Serial.print(trigger);
 if (trigger == 1) {
  digitalWrite(TRIGGER_PIN, HIGH);
//  Serial.print("High");
 }
 else if (trigger == 0) {
  digitalWrite(TRIGGER_PIN, LOW);
//  Serial.print("Low");
 }
}
