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
alarm_path = '/home/pi/musics/smartAlarmClock/alarms'
toeic_path = '/home/pi/musics/smartAlarmClock/toeic'
champion_path = '/home/pi/musics/smartAlarmClock/champion'
username = 'common.frameworks@gmail.com'#your email
password = 'qazx0987'#your password

#Local Alarm
alarm1time = '06:30'
alarm1file = ''
alarm_path1 = '/home/pi/musics/alarms'

#intern variable
durationendtime=''
durationflag = 'False'
playtype = ''

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
    command = "mplayer" + " " + file + " "
    print "+++PlayFile---",command
    os.system(command)

def RandomPlay(path):
    print "@@@@@@@@@@@ RandomPlay, path:",path
    file = path + '/' + random.choice(os.listdir(path))
    PlayFile(file)

def PlayByType(type):
    paths_list = {
            'wake': 'alarm_path',
            'toeic':'toeic_path',
            'champion':'champion_path',
            }
    path = paths_list[type]
    print "@@@@@@@@@@@ PlayByType path:",path
    RandomPlay(path)

def RandomPlayDuration(event_type,endtime):
    print "@@@@@@@@@@@ RandomPlayDuration,End:",endtime
    global durationendtime,durationflag,playtype
    durationendtime = endtime
    print "@@@@@@@@@@@ Set True, Type:",event_type
    durationflag = 'True'
    playtype = event_type
    PlayByType(event_type)

def CheckDuration():
    print "++++++++++++start check duration", "-----------"
    CheckTime(durationendtime,time.localtime())
    print "--------------end check duration", "-----------"

def CheckTime(event_date,local_date):
    delta=(int(time.mktime(event_date))-int(time.mktime(local_date)))/60
    if (delta >= 0 ):
        print "delta:",delta,"continue play, L:",local_date
        PlayByType(playtype)
    else:
        print "@+@+@+@+ delta:",delta," set False"
        global durationflag
        durationflag = 'False'

def FullTextQuery(calendar_service, text_query):
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
                RandomPlayDuration(text_query,time.localtime(tf_from_timestamp(a_when.end_time)))
#            else:
#                print "R:",event_date,"L:",current_date

def QueryEvent(event):
    print "++++++++++++start event query,",event, "-----------"
    FullTextQuery(calendar_service,event)
    print "--------------end event query,",event, "-----------"

def LocalAlarmClock():
    print "++++++++++++start query local alarm-----------"
    current_time= time.strftime('%H:%M')
    if current_time == alarm1time:
        #PlayFile(alarm1file)
        RandomPlay(alarm_path1)
    else:
        print "Local alarm:",alarm1time,", current time:",current_time
    print "--------------end query local alarm-----------"

def CalendarAlarms():
    if durationflag == 'True':
        CheckDuration()
    else:
        QueryEvent("wake")
        QueryEvent("toeic")
        QueryEvent("champion")

def callable_func():
    CalendarAlarms()
#    LocalAlarmClock()

#set unbufferd output mode
sys.stdout = os.fdopen(sys.stdout.fileno(),'w',0)

print "main start ... ... "
calendar_service = gdata.calendar.service.CalendarService()
setup(calendar_service)
login(calendar_service)
scheduler = Scheduler(standalone=True)
scheduler.add_interval_job(callable_func,seconds=50)
print "start scheduler."
scheduler.start() #runs the program indefinatly on an interval of 5 seconds

