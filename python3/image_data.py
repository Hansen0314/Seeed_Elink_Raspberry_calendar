#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
This file contains all the locations of the icons used.
It also contains the positions of these icons on the E-Paper display
"""

from PIL import Image
im_open = Image.open
import os

seperator = im_open('/home/pi/Seeed_Elink_Raspberry_calendar/python3/pic/seperator.jpeg')

wiconplace = (0, 0)
humplace = (0, 80)
tempplace = (150, 80)
windiconspace = (0, 90)
sunriseplace = (0, 130)
sunsetplace = (160, 130)
seperatorplace_H1 = (0, 75)
seperatorplace_H2 = (0, 130)

weathericons = {
    '01d': '\uf00d', '02d': '\uf002', '03d': '\uf013',
    '04d': '\uf012', '09d': '\uf01a', '10d': '\uf019',
    '11d': '\uf01e', '13d': '\uf01b', '50d': '\uf014',
    '01n': '\uf02e', '02n': '\uf013', '03n': '\uf013',
    '04n': '\uf013', '09n': '\uf037', '10n': '\uf036',
    '11n': '\uf03b', '13n': '\uf038', '50n': '\uf023'
    }
