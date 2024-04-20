
const int RELAY_PIN = 7; // Pin number ot which the 5V Relay Module input is connected
int moist;

void setup() {
  while (!Serial);
  Serial.begin(9600);
  pinMode(RELAY_PIN, OUTPUT); // Set the 5V Relay Module pin as an output

}

void loop() {
  Serial.println("Initial reading...");
  moist = analogRead(A0);
  Serial.println(moist);

  if(moist > 470){
    Serial.println("Yowzah thats too dry.  Lets give this baby some water!");
    while(moist > 450){
      digitalWrite(RELAY_PIN, HIGH); // Turning on the relay--pump off
      delay(1000); // Wait for 1 second
      digitalWrite(RELAY_PIN, LOW); // Turn off the relay--pump on
      delay(1000); // Wait for 1 second

      moist = analogRead(A0);
      Serial.println("New reading:");
      Serial.print(moist);
      delay(10000);
    }

    Serial.println("Okay, that should be good for now...");
    
  }else if(moist < 450){
    Serial.println("All is good for now");
  }
  digitalWrite(RELAY_PIN, HIGH);
  delay(1000);

}
