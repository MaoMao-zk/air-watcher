
## Pre-install
* Python3
* sgp30 python library
  > pip3 install adafruit-circuitpython-sgp30

## Configuration
* Serial Port
  > Enable "Serial Port", Disable "Serial Console"
* I2C Port
  > Enable "I2C Port"

## Running
  > /usr/bin/python3 /home/pi/git_repos/air-watcher/Main.py

## Config auto start after boot on
* Config file `/etc/systemd/system/air-watcher.service` as:
  ```
  [Unit]
  Description=air watcher service
  After=network.target
  Wants=network.target

  [Service]
  TimeoutStartSec=30
  ExecStart=/usr/bin/python3 /home/pi/git_repos/air-watcher/Main.py
  Restart=always

  [Install]
  WantedBy=multi-user.target
  ```
* Run command `systemctl enable air-watcher` to enable service
* Run command `systemctl daemon-reload` and reboot
* Check whether service started
  ``` shell
   $ service air-watcher status
  ● air-watcher.service - air watcher service
     Loaded: loaded (/etc/systemd/system/air-watcher.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2019-08-28 22:50:00 CST; 5min ago
   Main PID: 1523 (python3)
      Tasks: 3 (limit: 2200)
     Memory: 12.8M
     CGroup: /system.slice/air-watcher.service
             └─1523 /usr/bin/python3 /home/pi/git_repos/air-watcher/Main.py

  ```
