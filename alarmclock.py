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
audio_path = '/home/pi/musics/chinese'
alarm1time = '06:30'
alarm_path1 = '/home/pi/musics/alarms'
alarm1file = ''
username = 'common.frameworks@gmail.com'#your email
password = 'qazx0987'#your password

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
    print "---AlarmClock---",command
    os.system(command)

def RandomPlay(path):
    file = path + '/' + random.choice(os.listdir(path))
    PlayFile(file)

def CheckTime(event_date,local_date,range):
#    event=time.strptime(event_date,'%d-%m-%Y %H:%M')
#    local=time.strptime(local_date,'%d-%m-%Y %H:%M')
#    delta=int(time.mktime(local))-int(time.mktime(event))
    event=time.strftime('%d-%m-%Y %H:%M',event_date)
    local=time.strftime('%d-%m-%Y %H:%M',local_date)
    print "event:",event,"local:",event
    delta=int(time.mktime(local_date))-int(time.mktime(event_date))
#    print "event:",event_date,"local:",event_date
    print "delta:",delta," range:", range
    if abs(delta) <= range:
        RandomPlay(audio_path)

def FullTextQuery(calendar_service, text_query='wake'):
    query = gdata.calendar.service.CalendarEventQuery\
        ('default', 'private', 'full', text_query)
    init(query)

    feed = calendar_service.CalendarQuery(query)
    for i, an_event in enumerate(feed.entry):
        for a_when in an_event.when:
#            event_date = time.strftime('%d-%m-%Y %H:%M',\
#                time.localtime(tf_from_timestamp(a_when.start_time)))
#            current_date = time.strftime('%d-%m-%Y %H:%M')
#            CheckTime(event_date,current_date,180)
            CheckTime(time.localtime(tf_from_timestamp(a_when.start_time)),time.localtime(),180)
def LocalAlarmClock():
    current_time= time.strftime('%H:%M')
    if current_time == alarm1time:
        #PlayFile(alarm1file)
        RandomPlay(alarm_path1)
    else:
        print "Comparison:Fail, local alarm:",alarm1time,\
            ", current time:",current_time

def QueryEvent(event):
    print "------------start event query,", event, "-----------"
    FullTextQuery(calendar_service,event)
    print "-------------end event query,",event, "------------"

def callable_func():
    QueryEvent("wake")
    QueryEvent("champion")
    print "------------start query local alarm-----------"
    LocalAlarmClock()
    print "-------------end query local alarm------------"

print "start ... ... ."
calendar_service = gdata.calendar.service.CalendarService()
setup(calendar_service)
login(calendar_service)
scheduler = Scheduler(standalone=True)
scheduler.add_interval_job(callable_func,seconds=50)
print "start scheduler."
scheduler.start() #runs the program indefinatly on an interval of 5 seconds

