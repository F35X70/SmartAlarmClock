#!/bin/bash
# Install gdata
sudo apt-get install python-gdata moc

log="/var/log/alarmclock"
if [ ! -d $log ];then
    sudo mkdir -p $log
fi
#Add service
sudo cp alarmclock.py /usr/local/sbin/
sudo cp alarmclock /etc/init.d/alarmclock
sudo chkconfig -add alarmclock
