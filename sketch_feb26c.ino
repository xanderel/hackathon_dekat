#include <LedControl.h>

// set up the LED display
LedControl lc = LedControl(11, 13, 10, 1);

void setup() {
  Serial.begin(9600); // initialize serial communication
  lc.shutdown(0, false); // turn on the LED display
  lc.setIntensity(0, 8); // set the brightness of the display (0-15)
  lc.clearDisplay(0); // clear the display
}

void loop() {
  if (Serial.available() > 0) { // check if there is incoming serial data
    String command = Serial.readStringUntil('\n'); // read the incoming command
    if (command.startsWith("s")) { // if the command is to set an LED
      int row = command.substring(2, 3).toInt(); // extract the row from the command
      int col = command.substring(4, 5).toInt(); // extract the column from the command
      int state = command.substring(6, 7).toInt(); // extract the LED state from the command
      lc.setLed(0, row, col, state); // set the state of the specified LED
    }
    else if (command.startsWith("c")) { // if the command is to clear the display
      lc.clearDisplay(0); // clear the display
    }
  }
}
