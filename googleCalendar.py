from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from oauth2client.file import Storage
import datetime
import tkinter
from tkinter import simpledialog
from tkinter import messagebox

#convert time to military
def timeToMilitary(time):
    print(time)
    milTime = ""
    if len(time) == 7:
        milTime = time[0:1]+time[2:4]
    elif len(time) == 8:
        milTime = time[0:2] + time[3:5]
    milTime = int(milTime)
    if time[-2] == 'p':
        milTime += 1200
    elif time[-2] == 'a':
        pass
    
    milTime = str(milTime)
    if len(milTime) == 3:
        milTime = '0'+milTime
    elif len(milTime) == 4:
        pass
    milTime = milTime[0:2]+':'+milTime[2:]
    
    if time == '12:00 am':
        milTime = '00:00'
    elif time == '12:30 am':
        milTime = '00:30'
    elif time == '12:00 pm':
        milTime = '12:00'
    elif time == '12:30 pm':
        milTime = '12:30'
    return milTime

def getMonth(month):
    d = {'january':1,'february':2,'march':3,'april':4,'may':5,'june':6,'july':7,
    'august':8,'september':9,'october':10,'november':11,'december':12}
    for key in d:
        if key == month:
            month = d[key]
    if int(month) < 10:
        month = '0'+str(month)
    else:
        month= str(month)
    return month


class MemoryCache(object):
    _CACHE = {}
    def get(self, url):
        return MemoryCache._CACHE.get(url)
    def set(self, url, content):
        MemoryCache._CACHE[url] = content

#code taken from https://developers.google.com/calendar/create-events
#modified to fit project

def makeEvent(id,root,inputNeeded=True,summary = None, month = None, day = 
                            None, year = None, startTime= None, endTime = None):
    # Setup the Calendar API
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()),cache = MemoryCache())
    
    calendar_list_entry = service.calendarList().get(calendarId=id).execute()
    
    if inputNeeded:
        msg1 = 'name of event: '
        summary = simpledialog.askstring('name',msg1,parent=root)
        
        msg2 = 'what month?'
        msg3 = 'what day?'
        msg4 = 'what year?'
        month = simpledialog.askstring('month',msg2,parent=root)
        day = simpledialog.askstring('day',msg3,parent=root)
        year = simpledialog.askstring('year',msg4,parent=root)
        
        msg5 = 'when does this event start?'
        msg6 = 'when does this event end?'
        
        startTime = simpledialog.askstring('start',msg5,parent=root)
        endTime = simpledialog.askstring('end',msg6,parent=root)
    else:
        summary = summary
        month = month
        day = day
        year = year
        startTime = startTime
        endTime = endTime
    
    month = getMonth(month)
    startTime = timeToMilitary(startTime)
    first = year+'-'+month+'-'+day+'T'+startTime+':00-04:00'
    
    endTime = timeToMilitary(endTime)
    last = year+'-'+month+'-'+day+'T'+endTime+':00-04:00'
    
    event = {
    'summary': summary,
    'location': "",
    'description': "",
    'start':{
        'dateTime': first,
        'timeZone': "",
    },
    'end': {
        'dateTime': last,
        'timeZone': "",
    },
    'recurrence': [
    ],
    'attendees': [],
    'reminders': {
        'useDefault': False,
        'overrides': [
        {'method': 'email', 'minutes': 24 * 60},
        {'method': 'popup', 'minutes': 10},
        ],
    },
    }
    
    event = service.events().insert(calendarId=id, body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))

