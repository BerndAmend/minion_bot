# Minion Bot
The ultimate surveillance eye for your beloved Raspberry Pi!

# Print the 3d parts

0) Generate the stl-files (optiona)
  ```
cd 3d\ printed\ parts
./export-to-stl.sh
  ```

1) Print the files
  ```
3d\ printed\ parts/foot.stl
3d\ printed\ parts/mount.stl
  ```

# Instructions for Arch

1) Install Arch Linux ARM
   Follow the installation instructions for your Raspberry Pi
     https://archlinuxarm.org/platforms/armv7/broadcom/raspberry-pi-2
     https://archlinuxarm.org/platforms/armv8/broadcom/raspberry-pi-3
     https://archlinuxarm.org/platforms/armv8/broadcom/raspberry-pi-4

0) Ensure the system is up-to-date
  ```
su
pacman -Syu
reboot
  ```

1) Install required dependencies
```
su
pacman -S python-numpy opencv hdf5 gpac wget 
```
Use yaourt or wget/makepkg to build the package python-picamera.
```
wget https://aur.archlinux.org/cgit/aur.git/snapshot/python-picamera.tar.gz
tar xf python-picamera.tar.gz
cd python-picamera
makepkg
su
pacman -U python-picamera*.pkg.tar.xz
```

2) We want to control the Pi via the Telegram API:
```
TODO
```

# Activate it

0) Ensure that your camera is activated by checking if the required options are set in `/boot/config.txt`.
```
gpu_mem=128
start_file=start_x.elf
fixup_file=fixup_x.dat
# optionally (only works on some hardware configurations)
disable_camera_led=1
```
If you change anything reboot.

1) Install Telegram on your mobile device and create your very first bot referring to your good friend the 'BotFather':

[Create your Telegram Bot!](https://core.telegram.org/bots)

2) Copy minion_bot.json file to /home/pi/ directory and adapt it to your needs:
  ```
cp ~/minion_bot/minion_bot.json ~/.minion_bot.json
nano ~/.minion_bot.json
  ```
3) Add our Minion Bot as service to Pi's autostart:
  ```
mkdir -p ~/.config/systemd/user
cp ~/minion_bot/minion_bot.service ~/.config/systemd/user
systemctl --user enable minion_bot.service
  ```
4) Start your Minion Bot:
  ```
systemctl --user start minion_bot.service
  ```
5) Enable linger
  ```
sudo loginctl enable-linger <username>
  ```
6) Ask your bot about what you can ask him via the command 'So what?'  and have fun!
