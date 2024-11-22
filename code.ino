#define TRIG_PIN 7 // Trigger pin of the ultrasonic sensor
#define ECHO_PIN 6 // Echo pin of the ultrasonic sensor

const int thresholdDistance = 10; // Distance (in cm) to determine if the slot is occupied

void setup() {
  Serial.begin(9600); // Start serial communication at 9600 baud rate
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
}

void loop() {
  long duration, distance;

  // Generate a pulse on the Trigger pin``
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

      // Measure the time it takes for the echo to return
  duration = pulseIn(ECHO_PIN, HIGH);

  // Calculate distance in centimeters
  distance = duration * 0.034 / 2;

  // Determine the parking slot status
  if (distance <= thresholdDistance && distance > 0) {
    Serial.println("occupied"); // Send "occupied" to the Python server
  } else {
    Serial.println("available"); // Send "available" to the Python server
  }

  delay(2000); // Check every 2 seconds
}