#code taken from https://developers.google.com/calendar/quickstart/python
"""
Shows basic usage of the Google Calendar API. Creates a Google Calendar API
service object and outputs a list of the next 10 events on the user's calendar.
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime

#code taken from https://github.com/google/google-api-python-client/issues/325
class MemoryCache(object):
    _CACHE = {}
    def get(self, url):
        return MemoryCache._CACHE.get(url)
    def set(self, url, content):
        MemoryCache._CACHE[url] = content

def calendar(id):
    # Setup the Calendar API
    SCOPES = 'https://www.googleapis.com/auth/calendar'    
    store = file.Storage('credentials.json')    
    creds = store.get()    
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()),cache = MemoryCache())
        
        # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    
    events_result = service.events().list(calendarId=id, timeMin=now, maxResults=15, singleEvents=True,orderBy='startTime').execute()
    
    events = events_result.get('items', [])
    
    #add next 10 events and info to a list
    lstOfEvents = []
    if not events:
        lstOfEvents.append('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        lstOfEvents.append((start,end,event['summary']))
    return lstOfEvents
    
    
    