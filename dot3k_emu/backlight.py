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

# This is just dummy/copied code for now to get the thing working

# Eventually render this on the fake LCD:
# - "LEDs" will be positioned like on device.
# - Backlight as background color?

def set_graph(value):
    pass

def set(index, value):
    pass

def set_bar(index, value):
    pass

def hue_to_rgb(hue):
    """Convert a hue to RGB brightness values
    :param hue: hue value between 0.0 and 1.0
    """

    rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)

    return [int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)]


def hue(hue):
    """Set the backlight LEDs to supplied hue
    :param hue: hue value between 0.0 and 1.0
    """

    col_rgb = hue_to_rgb(hue)
    rgb(col_rgb[0], col_rgb[1], col_rgb[2])

def sweep(hue, range=0.08):
    """Set the backlight LEDs to a gradient centered on supplied hue
    Supplying zero to range would be the same as hue()
    :param hue: hue value between 0.0 and 1.0
    :param range: range value to deviate the left and right hue
    """

    left_hue((hue - range) % 1)
    mid_hue(hue)
    right_hue((hue + range) % 1)


def left_hue(hue):
    """Set the left backlight to supplied hue
    :param hue: hue value between 0.0 and 1.0
    """

    col_rgb = hue_to_rgb(hue)
    left_rgb(col_rgb[0], col_rgb[1], col_rgb[2])
    update()


def mid_hue(hue):
    """Set the middle backlight to supplied hue
    :param hue: hue value between 0.0 and 1.0
    """

    col_rgb = hue_to_rgb(hue)
    mid_rgb(col_rgb[0], col_rgb[1], col_rgb[2])
    update()


def right_hue(hue):
    """Set the right backlight to supplied hue
    :param hue: hue value between 0.0 and 1.0
    """

    col_rgb = hue_to_rgb(hue)
    right_rgb(col_rgb[0], col_rgb[1], col_rgb[2])
    update()

def left_rgb(r, g, b):
    """Set the left backlight to supplied r, g, b colour
    :param r: red value between 0 and 255
    :param g: green value between 0 and 255
    :param b: blue value between 0 and 255
    """
    pass

def mid_rgb(r, g, b):
    """Set the middle backlight to supplied r, g, b colour
    :param r: red value between 0 and 255
    :param g: green value between 0 and 255
    :param b: blue value between 0 and 255
    """
    pass

def right_rgb(r, g, b):
    """Set the right backlight to supplied r, g, b colour
    :param r: red value between 0 and 255
    :param g: green value between 0 and 255
    :param b: blue value between 0 and 255
    """
    pass

def rgb(r, g, b):
    """Set all backlights to supplied r, g, b colour
    :param r: red value between 0 and 255
    :param g: green value between 0 and 255
    :param b: blue value between 0 and 255
    """
    left_rgb(r, g, b)
    mid_rgb(r, g, b)
    right_rgb(r, g, b)

def off():
    """Turn off the backlight."""
    rgb(0, 0, 0)

def update():
    """Update backlight with changes to the LED buffer"""
    pass
