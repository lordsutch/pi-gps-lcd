# pi-gps-lcd
Output GPS fix information from gpsd to an RPi-attached Displayotron 3000 LCD

Requires the following Python 3 packages, along with gpsd on the Pi:

- dot3k from https://github.com/pimoroni/displayotron
- python3-gpsd from https://github.com/MartijnBraam/gpsd-py3

(Considering switching to another gpsd client library.)

# To Do

- Add dot3k emulation code to simulate output for easier development
- Enable joystick button for something (metric/traditional switch?)
