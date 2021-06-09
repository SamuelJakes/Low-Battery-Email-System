# What this software does
This code is used for sending email alerts when a WiFi connected device is running low on battery. Battery percentage is determined using measure output voltages and the characteristc and sending alerts when the battery level falls below a specified level.
The code is written specifically for a ADS1015 (a 12-bit ADC with 4 channels) but can be easily adapted for any voltage measuring setup.

# Example
This repository includes example code using a Powertech Lithium battery, with the characteristic curve shown below.

![Characteristic Curve](PowertechLithiumGraph.png?raw=true "Characteristic Curve")

See the actual code for further info