# Seeed_Elink_Raspberry_calendar

随着科技的发展，我们平时接触消息咨询也都是通过手机获取的了。手机取代了传统的书本报纸，在地铁通勤的时候也都是用手机看电子书和浏览网页。不过手机屏幕其实不适合长时间阅读文字，传统的液晶屏发出的蓝光会令眼睛感到疲劳。
而水墨屏就不一样了，虽然颜色单调了一点，但是由于水墨屏的特性，它发出的光是不会伤害到眼睛的，同时光线越强显示反而越清楚。所以对于我想设计的万年历水墨屏或许是一个不错的选择。


## 硬件构成

### Raspberry3b

为了得到当地天气情况和时间，采用性能强悍的树莓派3b+来做主控制器是在好不过的事情了，因为[Raspberry3b](https://www.seeedstudio.com/Raspberry-Pi-3-Model-B-p-2625.html)不仅有wifi功能而且支持python代码开发。

### 2.7'' Triple-Color E-Ink Display for Raspberry Pi

显示当然是使用水墨屏，经过全方位的性价比考察采用Seeed提供的[2.7'' Triple-Color E-Ink Display for Raspberry Pi](https://www.seeedstudio.com/2-7-Triple-Color-E-Ink-Display-for-Raspberry-Pi-p-4042.html)


## 软件设计

### 2.7'' Triple-Color E-Ink Display for Raspberry Pi 驱动设计

由于官方只有C++库没有python库，通过查阅相关的资料，最终我找到了与之类似的[python驱动代码](https://github.com/waveshare/e-Paper/tree/master/Raspberry%20Pi/python3/examples),由于硬件之间的差异我们通过修改引脚的编号，成功的将网上找的python驱动代码移植到我们的硬件上，具体操作如下：

第一步:下载对应的库文件
```shell
cd ~
git clone https://github.com/waveshare/e-Paper.git 
```

第二步：打开`epdconfig.py`文件上面那四个引脚编号分别修改成`RST_PIN = 13`，`DC_PIN = 6`，`CS_PIN = 5`，`BUSY_PIN = 19`

```shell
cd ~
nano ~/e-Paper/Raspberry\ Pi/python3/lib/epdconfig.py
```

第三步：运行测试代码
```shell
cd ~/e-Paper/Raspberry\ Pi/python3/examples/
python3 epd_2in7b_test.py
```

效果如下图
![](https://github.com/hansonCc/Seeed_Elink_Raspberry_calendar/raw/master/pic/demo.jpg)


### 日历软件设计

本设计是参考[Inky-Calendar](https://github.com/aceisace/Inky-Calendar/blob/Stable/Calendar/settings.py.sample)上面的内容我们可以运行下面的命令去安装所以的依赖项

```shell
bash -c "$(curl -sL https://raw.githubusercontent.com/aceisace/Inky-Calendar/Stable/Installer-with-debug.sh)"
```

安装依赖项的详细流程请参考[Inky-Calendar](https://github.com/aceisace/Inky-Calendar/blob/Stable/Calendar/settings.py.sample)，下面我将简述我的设计流程，首先，我们需要做的将云端的天气采集到我们的设备上面，显然[OpenWeatherMap](https://openweathermap.org/)就非常适合我们。
第一步：点击[详细指南](https://openweathermap.org/guide)，将导航到`OpenWeatherMap`的指南页，上面的会教你如何订阅一个免费的服务。

![](https://github.com/hansonCc/Seeed_Elink_Raspberry_calendar/raw/master/pic/How_to_start_Registration_process.JPG)

第二步：您可以根据[Seeed_Elink_Raspberry_calendar](https://github.com/hansonCc/Seeed_Elink_Raspberry_calendar/tree/master/python3)提供的`Settings.py`文件设置`OpenWeatherMap`相关的参数并将其保存到对应的文件夹。

![](https://github.com/hansonCc/Seeed_Elink_Raspberry_calendar/raw/master/pic/settings.JPG)

第三步：您可以运行下面的代码查看相应的天气信息
```shell
git clone https://github.com/hansonCc/Seeed_Elink_Raspberry_calendar.git
cd ~/Seeed_Elink_Raspberry_calendar/python3
python3 Calendar.py
```

![](https://github.com/hansonCc/Seeed_Elink_Raspberry_calendar/raw/master/pic/weather_conduct.JPG)

然后，我们需要将采集到时间和天气信息显示到`2.7'' Triple-Color E-Ink Display for Raspberry Pi`上面，为了做出想要的GUI的特意参考了[Inky-Calendar](https://github.com/aceisace/Inky-Calendar/blob/Stable/Calendar/settings.py.sample)上面模型，实际运行的效果如下：

![](https://github.com/hansonCc/Seeed_Elink_Raspberry_calendar/raw/master/pic/conduct.jpg)

最后，为了防止树莓派掉电后，程序运行停止，我们将进行开机自启动

第一步：新建一个`startup.sh`文件
```shell
cd ~/Seeed_Elink_Raspberry_calendar
nano startup.sh
```
第二步：在`startup.sh`文件里面加入下面的内容
```shell
#!/bin/bash
python3 /home/pi/Seeed_Elink_Raspberry_calendar/python3/Calendar.py
```
第三步：打开`/etc/rc.local`文件，并在`exit 0`前面添加
```shell
sudo -u pi /home/pi/Seeed_Elink_Raspberry_calendar/startup.sh
```

## 成果展示
![](https://github.com/hansonCc/Seeed_Elink_Raspberry_calendar/raw/master/pic/conduct.jpg)

