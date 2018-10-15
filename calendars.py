import checkWeather
#this file handles the functions necessary for the calendar screen

#changes number month to word
def calculateMonth(month):
    months = ['','january','february','march','april','may','june','july',
    'august','september','october','november','december']
    strMonth = months[month]
    return strMonth
    
#draw the calendar buttons
def drawCalendar(canvas,data):
    
    weath = "check today's weather"
    canvas.create_rectangle(110,15,490,75,fill='SlateGray1',outline='SlateGray1')
    canvas.create_text(data.width//2+3,48,text=weath,font='Calibri 30',fill='gray')
    canvas.create_text(data.width//2,45,text=weath,font='Calibri 30',fill='white')
    
    msg = 'go to calendar'
    canvas.create_rectangle(150,100,450,185, fill='SteelBlue3',outline='SteelBlue3')
    canvas.create_text(data.width//2+2,144,text=msg,font='Calibri 40',fill='black')
    canvas.create_text(data.width//2,140,text=msg,font='Calibri 40',fill='white')
    
    text = 'get events'
    canvas.create_rectangle(100,260,500,350,fill='SlateGray1',outline='SlateGray1')
    canvas.create_text(data.width//2+2,data.height//2+4,text=text,font='Calibri 50',fill='gray')
    canvas.create_text(data.width//2,data.height//2,text=text,font='Calibri 50',fill='white')
    
    msg2 = 'add event'
    canvas.create_rectangle(175,425,425,510,fill='SteelBlue3',outline = 'SteelBlue3')
    canvas.create_text(data.width//2+2,472,text=msg2,font='Calibri 40',fill='black')
    canvas.create_text(data.width//2,468,text=msg2,font='Calibri 40',fill='white')

#taken from https://stackoverflow.com/questions/31691007/0-23-hour-military-clock-to-standard-time-hhmm
#modified to fit project better
#changes military time to normal time
def timeConvert(miliTime):
    hours, minutes = miliTime.split(":")
    hours, minutes = int(hours), int(minutes)
    setting = "am"
    if hours == 12:
        setting = "pm"
    elif hours > 12:
        setting = "pm"
        hours -= 12
    elif hours == 0:
        setting = 'am'
        hours = 12
    return(("%02d:%02d" +' '+ setting) % (hours, minutes))

#makes the list of events more readable (dates and times)
def readable(lst):
    updateLst = []
    if lst[0] != "No upcoming events found.":
        for item in lst:
            date = item[0]
            year = date[:4]
            month = date[5:7]
            if month[0] == 0:
                month=month[1:]
            month = calculateMonth(int(month))
            day = date[8:10]
            startTime = date[11:16]
            startTime = timeConvert(startTime)
            ending = item[1]
            endTime = ending[11:16]
            endTime = timeConvert(endTime)
            summary = item[2]
            updateLst.append((month+' '+day+', '+year+' '+startTime+'-'+endTime+' ',summary))
    return updateLst

#displays the next 10 events
def createEvents(canvas,data):
    canvas.create_text(data.width//2, 54,text='Next 12 Events',font = 'Calibri 40', fill = 'SteelBlue3')
    canvas.create_text(data.width//2, 50,text='Next 12 Events',font = 'Calibri 40', fill = 'white')
    lstOfEvents = readable(data.lstOfEvents)
    font = 'Calibri 20'
    for i in range(len(lstOfEvents)):
        if i == 12:
            break
        x = data.width//6
        y = data.height//15 * i + 110
        event = lstOfEvents[i]
        text1 = event[0]
        text2 = event[1]
        canvas.create_text(x*2,y,text=text1,font=font,fill='white')
        canvas.create_text(x*5,y+3,text=text2,font=font,fill='SteelBlue3')
        canvas.create_text(x*5,y,text=text2,font=font,fill='white')
        

#update the weather accordingly and display it
def updateWeather(canvas,data):
    lstOfWeather = checkWeather.checkWeather(data.city)
    
    currently = lstOfWeather[0].lower()
    entire = lstOfWeather[1]
    date = data.month + ' '+str(data.day) + ' '+str(data.year)
    high = lstOfWeather[3]
    low = lstOfWeather[4]
    
    canvas.create_text(data.width//2+2, 103,text="today's weather",font='Calibri 50',fill='gray')
    canvas.create_text(data.width//2, 100,text="today's weather",font='Calibri 50',fill='white')
    
    canvas.create_text(data.width//2, 143,text=data.city,font='Calibri 25',fill='white')
    canvas.create_text(data.width//2, 140,text=data.city,font='Calibri 25',fill='SteelBlue')
    
    canvas.create_text(data.width//3, 203,text="date: ",font='Calibri 30',fill='SteelBlue2')
    canvas.create_text(data.width//3, 200,text="date: ",font='Calibri 30',fill='white')
    canvas.create_text(data.width//3  * 2, 200,text=date,font='Calibri 35',fill='white')
    
    canvas.create_text(data.width//3, 278,text="forecast: ",font='Calibri 30',fill='SteelBlue2')
    canvas.create_text(data.width//3, 275,text="forecast: ",font='Calibri 30',fill='white')
    canvas.create_text(data.width//3 * 2, 275,text=currently,font='Calibri 35',fill='white')
    
    canvas.create_text(data.width//3, 353,text="today's high: ",font='Calibri 30',fill='SteelBlue2')
    canvas.create_text(data.width//3, 350,text="today's high: ",font='Calibri 30',fill='white')
    canvas.create_text(data.width//3 * 2, 350,text=high+' F',font='Calibri 35',fill='white')
    
    canvas.create_text(data.width//3, 428,text="today's low: ",font='Calibri 30', fill='SteelBlue2')
    canvas.create_text(data.width//3, 425,text="today's low: ",font='Calibri 30', fill='white')
    canvas.create_text(data.width//3 * 2, 425,text=low+' F',font='Calibri 35', fill='white')
    
    
    
