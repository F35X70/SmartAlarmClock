#!/usr/bin/python
#-*- coding:utf-8 -*-
#These are the imports google said to include
import gdata.calendar.service
import gdata.service
import atom.service
import gdata.calendar
import gdata.calendar
import atom
import getopt
import sys
import string
import time

import xe #for the time comparator
from feed.date.rfc3339 import tf_from_timestamp #also for the comparator
from datetime import datetime #for the time on the rpi end
from apscheduler.scheduler import Scheduler #this will let us check the calender on a regular interval
import os, random #to play the mp3 later

#EDIT THIS PART BY YOURSELF
ac_log = "/var/log/alarmclock/ac.log"
audio_path = '/home/pi/musics/chinese'
alarm1time = '06:30'
alarm_path1 = '/home/pi/musics/alarms'
alarm1file = ''
username = 'common.frameworks@gmail.com'#your email
password = 'qazx0987'#your password

#intern variable
durationtime = 12 #unit mintue
durationstart =''
durationflag = 'False'

def setup(calendar_service):
    #this is more stuff google told me to do, but essentially it handles the login credentials
    calendar_service.email = username
    calendar_service.password = password
    calendar_service.source = 'Google-Calendar_SmartAlarmClock-1.0'

def login(calendar_service):
    calendar_service.ProgrammaticLogin()

def init(query):
    query.orderby = 'starttime'
    query.singleevents = 'true'
    query.sortorder = 'a'
    query.futureevents = 'true'
    query.max_attendees = '7'

def PlayFile(file):
    command = "mpg321" + " " + file + " -g 100"
    print "+++PlayFile---",command
    os.system(command)

def RandomPlay(path):
    print "@@@@@@@@@@@ RandomPlay"
    file = path + '/' + random.choice(os.listdir(path))
    PlayFile(file)

def RandomPlayDuration(path):
    print "@@@@@@@@@@@ RandomPlayDuration"
    global durationstart,durationflag
    durationstart = time.localtime()
    print "@@@@@@@@@@@ Set True"
    durationflag = 'True'
    file = path + '/' + random.choice(os.listdir(path))
    PlayFile(file)

def CheckDuration():
    print "++++++++++++start check duration", "-----------"
    global durationtime,durationstart
    CheckTime(durationstart,time.localtime(),durationtime)
    print "------------end check duration", "-----------"

def CheckTime(event_date,local_date,range):
    delta=(int(time.mktime(local_date))-int(time.mktime(event_date)))/60
    if (delta >= 0 and delta <= range):
        RandomPlay(audio_path)
    else:
        print "@+@+@+@+ set False"
        global durationflag
        durationflag = 'False'

def FullTextQuery(calendar_service, text_query='wake'):
    query = gdata.calendar.service.CalendarEventQuery\
        ('default', 'private', 'full', text_query)
    init(query)

    feed = calendar_service.CalendarQuery(query)
    for i, an_event in enumerate(feed.entry):
        for a_when in an_event.when:
            event_date = time.strftime('%d-%m-%Y %H:%M',\
                time.localtime(tf_from_timestamp(a_when.start_time)))
            current_date = time.strftime('%d-%m-%Y %H:%M')
            if current_date == event_date:
                RandomPlayDuration(audio_path)
#            else:
#                print "R:",event_date,"L:",current_date

def QueryEvent(event):
    print "++++++++++++start event query,", event, "-----------"
    FullTextQuery(calendar_service,event)
    print "------------end event query,",event, "------------"

def LocalAlarmClock():
    print "++++++++++++start query local alarm-----------"
    current_time= time.strftime('%H:%M')
    if current_time == alarm1time:
        #PlayFile(alarm1file)
        RandomPlay(alarm_path1)
    else:
        print "Local alarm:",alarm1time,", current time:",current_time
    print "------------end query local alarm------------"

def CalendarAlarms():
    global durationflag
    if durationflag == 'True':
        CheckDuration()
    else:
        QueryEvent("wake")
        QueryEvent("champion")

def callable_func():
    CalendarAlarms()
    LocalAlarmClock()
# redirect output to file
print ac_log
sys.stdout = open(ac_log,'w+')

print "main start ... ... "
calendar_service = gdata.calendar.service.CalendarService()
setup(calendar_service)
login(calendar_service)
scheduler = Scheduler(standalone=True)
scheduler.add_interval_job(callable_func,seconds=50)
print "start scheduler."
scheduler.start() #runs the program indefinatly on an interval of 5 seconds

