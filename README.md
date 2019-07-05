# Seeed_Elink_Raspberry_calendar

![](https://www.seeedstudio.site/media/catalog/product/cache/ef3164306500b1080e8560b2e8b5cc0f/1/0/104990449-preview.png)

With the development of technology, our usual contact information consultation is also obtained through mobile phones. Mobile phones have replaced traditional books and newspapers, and they use mobile phones to read e-books and browse the web when commuting in the subway. However, the screen of the mobile phone is not suitable for reading text for a long time, and the blue light emitted by the traditional LCD screen may make the eyes feel tired. The ink screen is different. Although the color is monotonous, due to the characteristics of the ink screen, the light it emits will not harm the eyes, and the stronger the light, the clearer the display. So maybe it is a good choice for the calendar ink screen I want to design.

## Hardware composition

### Raspberry3B

In order to get local weather conditions and time, it is a good thing to use the powerful Raspberry Pi 3b+ as the main controller, because [Raspberry3b](https://www.seeedstudio.com/Raspberry-Pi-3-Model-B-p-2625.html) Not only has wifi functionality but also Python code development.

![](https://www.seeedstudio.site/media/catalog/product/cache/ef3164306500b1080e8560b2e8b5cc0f/h/t/httpsstatics3.seeedstudio.comseeedimg2016-08xuzp3msf6xehp96wpfjinzco.jpg)

### 2.7'' Triple-Color E-Ink Display for Raspberry Pi

The display is of course using an ink screen. After a comprehensive price/performance comparison, the [2.7'' Triple-Color E-Ink Display for Raspberry Pi](https://www.seeedstudio.com/2-7-Triple-Color-E-Ink-Display-for-Raspberry-Pi-p-4042.html) from Seeed is used.

![](https://www.seeedstudio.site/media/catalog/product/cache/ef3164306500b1080e8560b2e8b5cc0f/2/_/2.7_triple-color-e-ink-display-for-rasberry-pi-size.png)

## Software design

### 2.7'' Triple-Color E-Ink Display for Raspberry Pi Driver

Since the official C++ library does not have a python library, I found a similar [python driver code](https://github.com/waveshare/e-Paper/tree/master/Raspberry%20Pi/python3/examples) by consulting the relevant information, due to the difference between the hardware, we successfully transplanted the python driver code found on the Internet to our hardware by modifying the pin number. The specific operation is as follows:

step 1: download the corresponding library file

```shell
cd ~
git clone https://github.com/waveshare/e-Paper.git 
```
step 2: Open the four pin numbers in the `epdconfig.py` file and change them to `RST_PIN = 13`, `DC_PIN = 6`, `CS_PIN = 5`, `BUSY_PIN = 19`.

```shell
cd ~
nano ~/e-Paper/Raspberry\ Pi/python3/lib/epdconfig.py
```

step 2: Run the demo

```shell
cd ~/e-Paper/Raspberry\ Pi/python3/examples/
python3 epd_2in7b_test.py
```

![](https://github.com/hansonCc/Seeed_Elink_Raspberry_calendar/raw/master/pic/demo.jpg)

### Calendar Software Design

This design is based on [Inky-Calendar](https://github.com/aceisace/Inky-Calendar/blob/Stable/Calendar/settings.py.sample). We can run the following command to install the dependencies.

```shell
bash -c "$(curl -sL https://raw.githubusercontent.com/aceisace/Inky-Calendar/Stable/Installer-with-debug.sh)"
```

For detailed procedures for installing dependencies, please refer to [Inky-Calendar](https://github.com/aceisace/Inky-Calendar/blob/Stable/Calendar/settings.py.sample). Below I will briefly describe my design process. First, we need to do the cloud weather collection on our device, obviously [OpenWeatherMap](https://openweathermap.org/) is very suitable for us.

step 1:Click on [Detailed Guide](https://openweathermap.org/guide) to navigate to the 'OpenWeatherMap` guide page, which will teach you how to subscribe to a free service.

![](https://github.com/hansonCc/Seeed_Elink_Raspberry_calendar/raw/master/pic/How_to_start_Registration_process.JPG)

Step 2: You can set the `OpenWeatherMap`related parameters according to the`Settings.py` file provided by [Seeed_Elink_Raspberry_calendar](https://github.com/hansonCc/Seeed_Elink_Raspberry_calendar/tree/master/python3) and save it to the corresponding Folder.

![](https://github.com/hansonCc/Seeed_Elink_Raspberry_calendar/raw/master/pic/settings.JPG)

Step 3: You can run the code below to see the corresponding weather information.

```shell
git clone https://github.com/hansonCc/Seeed_Elink_Raspberry_calendar.git
cd ~/Seeed_Elink_Raspberry_calendar/python3
python3 Calendar.py
```

![](https://github.com/hansonCc/Seeed_Elink_Raspberry_calendar/raw/master/pic/weather_conduct.JPG)

Then, we need to display the collected time and weather information on the top of the '2.7'' Triple-Color E-Ink Display for Raspberry Pi. In order to make the desired GUI, we specifically refer to [Inky-Calendar](https://github.com/aceisace/Inky-Calendar/blob/Stable/Calendar/settings.py.sample) The above model, the actual running effect is as follows:

![](https://github.com/hansonCc/Seeed_Elink_Raspberry_calendar/raw/master/pic/conduct.jpg)

Finally, in order to prevent the Raspberry Pi from powering down, the program stops running, we will boot from the boot

Step 1: Create a new `startup.sh` file

```shell
cd ~/Seeed_Elink_Raspberry_calendar
nano startup.sh
```

Step 2: Add the following content to the `startup.sh` file.

```shell
#!/bin/bash
python3 /home/pi/Seeed_Elink_Raspberry_calendar/python3/Calendar.py
```

Step 3: Open the `/etc/rc.local` file and add it before `exit 0`

```shell
sudo -u pi /home/pi/Seeed_Elink_Raspberry_calendar/startup.sh
```

## Final result
