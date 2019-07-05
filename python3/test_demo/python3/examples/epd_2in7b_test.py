#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
sys.path.append(r'../lib')

import epd2in7b
import epdconfig
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

try:
    print("epd2in7b Demo")
    
    epd = epd2in7b.EPD()
    print("init and Clear")
    epd.init()
    epd.Clear()
    time.sleep(1)
    
    # Drawing on the image
    print("Drawing")
    blackimage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    redimage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    
    font24 = ImageFont.truetype('../lib/Font.ttc', 24)
    font18 = ImageFont.truetype('../lib/Font.ttc', 18)
    

    # Drawing on the Horizontal image
    
    print("3.read bmp file")
    HBlackimage = Image.open('../pic/2in7b-b.bmp')
    HRedimage = Image.open('../pic/2in7b-r.bmp')
    epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRedimage))
    
    print("Goto Sleep...")
    epd.sleep()
        
except IOError as e:
    print(e)
    
except KeyboardInterrupt:    
    print("ctrl + c:")
    epdconfig.module_exit()
    exit()
