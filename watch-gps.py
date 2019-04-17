#!/usr/bin/python3

# Displays GPS location fix information from the gpsd daemon on a
# "Display-O-Tron 3000" LCD attached to a Raspberry Pi

# Copyright (c) 2019 Chris Lawrence

# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Uses: dot3k, gps

EMULATE = False

if EMULATE:
    from dot3k_emu import lcd, backlight
else:
    from dot3k import lcd, backlight
    
import gpsd
import time
import math

USE_METRIC = True
#USE_METRIC = False

if USE_METRIC:
    distance_unit = "m"
    distance_factor = 1.0
    speed_unit = "km/h"
    speed_factor = 3.6
else:
    distance_unit = "'"
    distance_factor = 3.28084
    speed_unit = "mph"
    speed_factor = 2.23694

connected = False
while not connected:
    try:
        gpsd.connect()
        connected = True
    except:
        time.sleep(1)

lcd.clear()
backlight.rgb(255,255,255)
backlight.set_graph(0.0)

while True:
    packet = gpsd.get_current()

    #print(packet)
    #lcd.set_cursor_position(11,2)
    #lcd.write('%2d/%02d' % (packet.sats_valid, packet.sats))

    lcd.set_cursor_position(13, 2)
    lcd.write('%2d@' % (packet.sats_valid))

    if packet.mode >= 2:
        lat = packet.lat
        lon = packet.lon
        
        ns = ('N' if lat >= 0 else 'S')
        ew = ('E' if lon >= 0 else 'W')

        lcd.set_cursor_position(0,0)
        lcd.write('%9.5f' % (abs(lat)) + ns)
        lcd.set_cursor_position(0,1)
        lcd.write('%9.5f' % (abs(lon)) + ew)
        lcd.set_cursor_position(0,2)
        speed = packet.speed() * speed_factor
        direction = ('N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW')[round(packet.track/45.0) % 8]
        
        lcd.write('%3.0f %s %-2.2s' % (speed, speed_unit, direction))

        precision = packet.position_precision()
        lcd.set_cursor_position(11, 1)
        lcd.write(chr(0xf9)+'%3.0f%s' % (precision[0] * distance_factor,
                                         distance_unit))

        # Convert this to a vague signal quality metric
        # Use sqrt(1/HDOP) instead?
        
        pval = math.expm1(math.e/(precision[0]+1))
        backlight.set_graph(pval)
        #print(precision[0], pval)
        
        if packet.mode >= 3:
            lcd.set_cursor_position(10, 0)
            lcd.write('%5.0f%s' % (packet.alt * distance_factor,
                                   distance_unit))
        else:
            lcd.set_cursor_position(10, 0)
            lcd.write(' 2D fix')
    else:
        lcd.clear()
        lcd.set_cursor_position(10, 0)
        lcd.write(' No fix')
        backlight.set_graph(0.0)

    # Don't poll too much
    time.sleep(0.2)
