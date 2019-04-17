#!/usr/bin/python3

# Emulation for the Display-O-Tron 3000 LCD for a text console.
# Thus far it only has enough to do what I use... feel free to add more.

# Copyright (c) 2019 Chris Lawrence
# Copyright (c) 2017 Pimoroni Ltd.

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

import curses
import atexit
from . import st7036_codec

# If you have an LCD that has different dimensions, you can change this.
HEIGHT =  3
WIDTH  = 16

# Initialization code
stdscr = curses.initscr()

def cleanup():
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
    
atexit.register(cleanup)

curses.noecho()
curses.cbreak()
stdscr.keypad(True)
stdscr.clear()
curses.curs_set(0)

lcd_screen = curses.newwin(HEIGHT+2, WIDTH+2, 0, 0)
lcd_screen.border()
lcd_screen.move(1, 1)

def set_cursor_offset(offset):
    y, x = divmod(offset, 16)
    set_cursor_position(x, y)

def set_cursor_position(x, y):
    lcd_screen.move(y+1, x+1)

def write(text):
    # Handle character set conversion here - note that the input is in
    # the 'st7036' character set, not really Unicode
    
    bytetext = text.encode('iso-8859-1') # since 0..255 map 1:1 here
    text = bytetext.decode('st7036')
    
    lcd_screen.addstr(text)
    lcd_screen.refresh()

def clear():
    lcd_screen.clear()
    lcd_screen.border()
    lcd_screen.refresh()

def set_display_mode(enable=True, cursor=False, blink=False):
    if cursor:
        if blink:
            curses.curs_set(2)
        else:
            curses.curs_set(1)
    else:
        curses.curs_set(0)
    
# Things we don't (yet?) emulate
def set_contrast(contrast):
    pass

def create_animation(anim_pos, anim_map, frame_rate):
    pass

def update_animations():
    pass

def create_char(char_pos, char_map):
    pass

if __name__ == '__main__':
    set_display_mode(cursor=True)
    
    write('Hello world!')
    set_cursor_position(0, 2)
    write('Press any key.')
    lcd_screen.getkey()
    
    for i in range(0, 8):
        for row in range(2):
            set_cursor_position(0, row)
            row = ''.join(chr(j) for j in range(i*32+16*row, i*32+16*row+16))
            write(row)

        set_cursor_position(0, 2)
        write('Press any key.')
        lcd_screen.getkey()

    cleanup()
