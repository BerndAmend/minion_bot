# Minion Bot
The ultimate surveillance eye for your Raspberry Pi!

# Instructions
0) Be a good guy and update everything:
  ```
sudo apt-get update
sudo apt-get upgrade
sudo rpi-update
  ```
1) Install Telegram on your mobile device and create your very first bot referring to your good friend the 'BotFather':

[Create your Telegram Bot!](https://core.telegram.org/bots)

2) We want to control the Pi via the Telegram API:
  ```
git clone https://github.com/python-telegram-bot/python-telegram-bot --recursive
cd python-telegram-bot
sudo python3 setup.py install
  ```
3) We need a converter before we can send recorded videos to our Telegram account:
  ```
sudo apt-get install gpac
  ```
4) We save some time and install a precompiled version of OpenCV:

[Get precompiled OpenCV!](https://github.com/jabelone/OpenCV-for-Pi)

5) Copy minion_bot.json file to /home/pi/ directory and adapt it to your needs:
  ```
copy /home/pi/minion_bot/minion_bot.json /home/pi/.minion_bot.json
sudo nano /home/pi/.minion_bot.json
  ```
6) Add our Minion Bot as service to Pi's autostart:
  ```
mkdir /home/pi/.config/systemd
mkdir /home/pi/.config/systemd/user
cp /home/pi/minion_bot/minion_bot.service /home/pi/.config/systemd/user
cd /home/pi/.config/systemd/user
systemctl --user enable minion_bot
  ```
7) Start your Minion Bot:
  ```
cd /home/pi/.config/systemd/user
systemctl --user start minion_bot
  ```
8) Ask your bot about what you can ask him via the command 'So what?'  and have fun!
