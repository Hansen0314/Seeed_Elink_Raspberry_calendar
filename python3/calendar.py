#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sys
from Library import epd2in7b
from Library import epdconfig
from settings import *
from image_data import *
from datetime import datetime, date, timedelta
import pyowm
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import arrow
from pytz import timezone
import numpy as np
from time import sleep
owm = pyowm.OWM(api_key, language=language)
font18 = ImageFont.truetype('/home/pi/Seeed_Elink_Raspberry_calendar/python3/Library/Font.ttc', 18)
font45 = ImageFont.truetype('/home/pi/Seeed_Elink_Raspberry_calendar/python3/Library/Font.ttc', 45)
w_font_l = ImageFont.truetype('/home/pi/Seeed_Elink_Raspberry_calendar/python3/Library/weathericons-regular-webfont.ttf', 60)
w_font_s = ImageFont.truetype('/home/pi/Seeed_Elink_Raspberry_calendar/python3/Library/weathericons-regular-webfont.ttf', 22)
im_open = Image.open
EPD_WIDTH = 176
EPD_HEIGHT = 264

'''Get system timezone and set timezone accordingly'''
with open('/etc/timezone','r') as file:
    lines = file.readlines()
    system_tz = lines[0].rstrip()
    local_tz = timezone(system_tz)
"""Custom function to display text on the E-Paper"""
def write_text(box_width, box_height, text, tuple, font=font18, alignment='middle'):
    text_width, text_height = font.getsize(text)
    while (text_width, text_height) > (box_width, box_height):
        text=text[0:-1]
        text_width, text_height = font.getsize(text)
    if alignment is "" or "middle" or None:
        x = int((box_width / 2) - (text_width / 2))
    if alignment is 'left':
        x = 0
    y = int((box_height / 2) - (text_height / 1.7))
    space = Image.new('RGB', (box_width, box_height), color='white')
    ImageDraw.Draw(space).text((x, y), text, fill='black', font=font)
    image.paste(space, tuple)
try:
    now = arrow.now(tz=system_tz)
    print("epd2in7b Demo")
    epd = epd2in7b.EPD()
    print("init and Clear")
    epd.init()
    epd.Clear()
    while True:
        time = datetime.now().replace(tzinfo=local_tz)
        image = Image.new('RGB', (EPD_HEIGHT, EPD_WIDTH), 'white')
        try:
            print("Connecting to Openweathermap API servers...")
            observation = owm.weather_at_place(location)
            weather = observation.get_weather()
            weathericon = weather.get_weather_icon_name()
            Humidity = str(weather.get_humidity())
            cloudstatus = str(weather.get_clouds())
            weather_description = (str(weather.get_detailed_status()))
            Temperature = str(int(weather.get_temperature(unit='celsius')['temp']))
            windspeed = str(int(weather.get_wind()['speed']))
            sunrisetime = arrow.get(weather.get_sunrise_time()).to(system_tz)
            sunsettime = arrow.get(weather.get_sunset_time()).to(system_tz)
        except Exception as e:
            print('__________OWM-ERROR!__________'+'\n')
            print('Reason: ',e,'\n')
            print("And,We will keep the last data")
            pass
        print("weather data:")
        """Show the fetched weather data"""
        print('Temperature:',Temperature, '°C')
        print('Humidity:', Humidity, '%')
        print('Wind speed:', windspeed, 'km/h')
        print('Sunrise-time:', sunrisetime.format('HH:mm'))
        print('Sunset time:', sunsettime.format('HH:mm'))
        print('Cloudiness:', cloudstatus, '%')
        print('Weather description:', weather_description, '\n')
        write_text(70,70, weathericons[weathericon], wiconplace, font = w_font_l)
        write_text(150,60, time.strftime("%H:%M"), (90, 10),font = font45)
        write_text(200,60, time.strftime("%y-%m-%d"), (25, 75),font = font45)
        write_text(50,50, '\uf051', sunriseplace, font = w_font_s)
        write_text(50,50, sunrisetime.format('H:mm'), (40, 130))
        write_text(50,50, '\uf052', sunsetplace , font = w_font_s)
        write_text(50,50, sunsettime.format('H:mm'), (200, 130))
        image.paste(seperator, seperatorplace_H1)
        image.paste(seperator, seperatorplace_H2)
        
        """
        Map all pixels of the generated image to red, white and black
        so that the image can be displayed 'correctly' on the E-Paper
        """
        buffer = np.array(image)
        r,g,b = buffer[:,:,0], buffer[:,:,1], buffer[:,:,2]
        buffer[np.logical_and(r > 245, g > 245)] = [255,255,255] #white
        buffer[np.logical_and(r > 245, g < 245)] = [255,255,255] #red
        buffer[np.logical_and(r != 255, r == g )] = [0,0,0] #black
        B_image = Image.fromarray(buffer)
        buffer = np.array(image)
        r,g,b = buffer[:,:,0], buffer[:,:,1], buffer[:,:,2]
        buffer[np.logical_and(r > 245, g > 245)] = [255,255,255] #white
        buffer[np.logical_and(r > 245, g < 245)] = [255,0,0] #red
        buffer[np.logical_and(r != 255, r == g )] = [255,255,255] #white
        R_image = Image.fromarray(buffer)
        print('Converting image to data and sending it to the display')
        epd.display(epd.getbuffer(B_image),epd.getbuffer(R_image))
        del buffer
        del B_image
        del R_image
        del image
        sleep(200)
    
except IOError as e:
    print(e)
    
except KeyboardInterrupt:    
    print("ctrl + c:")
    print("Goto Sleep...")
    epd.sleep()
    epdconfig.module_exit()
    exit()
