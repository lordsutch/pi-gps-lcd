#!/usr/bin/python3

# Uses: dot3k, gps

USE_METRIC = True
#USE_METRIC = False
EMULATE = False

if EMULATE:
    from dot3k_emu import lcd, backlight
else:
    from dot3k import lcd, backlight
    
import gpsd
import time
import math

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

    lcd.set_cursor_position(13,2)
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
        if USE_METRIC:
            speed = packet.speed() * 3.6
            units = 'km/h'
        else:
            speed = packet.speed() * 2.23694
            units = 'mph'
        direction = ('NW', 'N', 'NE', 'E', 'SE', 'S', 'SW', 'W')[int((packet.track + 22.5)/45.0) % 8]
        
        lcd.write('%3.0f %-4.4s %-2.2s' % (speed, units, direction))

        precision = packet.position_precision()
        lcd.set_cursor_position(11, 1)
        if USE_METRIC:
            lcd.write(chr(0xf9)+'%3.0fm' % precision[0])
        else:
            lcd.write(chr(0xf9)+"%3.0f'" % (precision[0] * 3.28084))

        pval = math.expm1(math.e/(precision[0]+1))
        backlight.set_graph(pval)
        #print(precision[0], pval)
        
        if packet.mode >= 3:
            lcd.set_cursor_position(10, 0)
            if USE_METRIC:
                lcd.write('%5.0fm' % packet.alt)
            else:
                lcd.write("%5.0f'" % (packet.alt * 3.28084))
        else:
            lcd.set_cursor_position(14, 0)
            lcd.write('2D')
            
    else:
        lcd.clear()
        lcd.set_cursor_position(0,0)
        lcd.write('No fix.')
        backlight.set_graph(0.0)

    # Don't poll too much
    time.sleep(0.2)
