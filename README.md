# Minion Bot
The ultimate surveillance eye for your beloved Raspberry Pi!

# Instructions
0) Be a good guy and update everything:
  ```
sudo apt-get update
sudo apt-get upgrade
sudo rpi-update
  ```
1) Install additional dependencies
on arch python-picamera python-numpy opencv
  
2) Install Telegram on your mobile device and create your very first bot referring to your good friend the 'BotFather':

[Create your Telegram Bot!](https://core.telegram.org/bots)

3) We want to control the Pi via the Telegram API:
  ```
git clone https://github.com/python-telegram-bot/python-telegram-bot --recursive
cd python-telegram-bot
sudo python3 setup.py install
  ```
4) We need a converter before we can send recorded videos to our Telegram account:
  ```
sudo apt-get install gpac
  ```
5) If we use Raspbian Jessie, we can save some time and install a precompiled version of OpenCV:

[Get precompiled OpenCV!](https://github.com/jabelone/OpenCV-for-Pi)

Otherwise, you have to compile OpenCV by yourself, unfortunately. We run our code using OpenCV 3.1.0.

[Get OpenCV source code!](https://opencv.org/releases.html)

You even can skip the installation of OpenCV and continue, but then you cannot use our cool motion detection algorithm.

5) Copy minion_bot.json file to /home/pi/ directory and adapt it to your needs:
  ```
cp ~/minion_bot/minion_bot.json ~/.minion_bot.json
nano ~/.minion_bot.json
  ```
6) Add our Minion Bot as service to Pi's autostart:
  ```
mkdir -p ~/.config/systemd/user
cp ~/minion_bot/minion_bot.service ~/.config/systemd/user
systemctl --user enable minion_bot.service
  ```
7) Start your Minion Bot:
  ```
systemctl --user start minion_bot.service
  ```
8) Ask your bot about what you can ask him via the command 'So what?'  and have fun!
