import datetime
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import quickstart
import webbrowser
import string
import googleCalendar
import copy
import times
import todoList
import schedule
import syllabus
import calendars
import start
import add
import checkWeather

####################################
# animation 
####################################
def init(data):
    #date
    data.month, data.year, data.day = None,None,None
    #time
    data.hour,data.minute = None,None
    data.city = add.addCity(root)
    #intro screen + basic information
    data.screen = 'intro'
    data.name,data.email = start.readInfo("nameAndEmail.txt")
    data.time = None
    data.rects = []
    data.prev = ['options']
    #to do list
    data.toDo = []
    data.toDoCopy = []
    data.checkLstCollision = []
    data.clickedOnToDo = None
    #schedule and events
    data.lstOfEvents = None
    data.schedule = schedule.startSchedule()
    data.sleepTime = None
    data.updateSleepTime = None
    data.classes = []
    data.foodAvail = False
    data.meals = []
    data.todoTimes = []
    data.empty = []
    data.addedEvents = False
    data.madeSched = False
    data.tasks = []
    #syllabus
    data.syllabi = []
    data.syllabiCoords= []

# #check if user clicked on a task on the to-do list
def checkCollision(data,x,y):
    for i in range(len(data.checkLstCollision)):
        check = data.checkLstCollision[i]
        x0= check[0]
        x1= check[2]
        y0= check[1]
        y1= check[3]
        if x0<=x<=x1 and y0<=y<=y1:
            data.checkLstCollision.pop(i)
            data.toDo.pop(i)
            data.clickedOnToDo = i
    
def mousePressed(event, data):
    x = event.x
    y = event.y
    #change the screen based on what the user clicks
    if data.screen == 'intro':
        data.screen = 'options'
    #changes the screen based on what the user clicks on
    elif data.screen == 'options':
        for i in range(len(data.rects)):
            rectangle = data.rects[i]
            x0 = rectangle[0]
            x1 = rectangle[2]
            y0 = rectangle[1]
            y1 = rectangle[3]
            if x0 <= x <= x1 and y0 <= y <= y1:
                if i == 0:
                    data.screen = 'calendar'
                elif i == 1:
                    data.screen = 'syllabus'
                elif i == 2:
                    data.screen = 'to do'
                elif i == 3:
                    data.screen = 'schedule'
                data.prev.append(data.screen)
    #if the user clicks on the "add" button, they can input a task
    #a list of all tasks is displayed
    elif data.screen == 'to do':
        if 510<=x<=590 and 10<=y<=80:
            task = add.askForTask(root)
            data.toDo.append(task)
            data.checkLstCollision.append((100,data.height//10 *(len(data.toDo)-1)
                            +175,500,data.height//10 * (len(data.toDo)-1)+225))
        #check that the user has clicked on a task
        checkCollision(data,x,y)
    #upload and display syllabus
    elif data.screen == 'syllabus':
        x0 = 100
        x1 = 500
        y0 = 150
        y1 = 250
        if x0 <= x <= x1 and y0 <= y <= y1:
            syllabus.uploadSyllabus(data,root)
        x0 = 100
        x1 = 500
        y0 = 350
        y1 = 450
        #go to current linked classes and their syllabi
        if x0 <= x <= x1 and y0 <= y <= y1:
            data.screen = 'currentSyllabi'
            data.prev.append(data.screen)
    elif data.screen == 'currentSyllabi':
        for i in range(len(data.syllabiCoords)):
            x0 = data.syllabiCoords[i][0]
            x1 = data.syllabiCoords[i][2]
            y0 = data.syllabiCoords[i][1]
            y1 = data.syllabiCoords[i][3]
            #if a class is clicked on, go to the online syllabus
            if x0 <= x <= x1 and y0 <= y <= y1:
                website = data.syllabi[i][1]
                webbrowser.open(website)
    elif data.screen == 'calendar':
        200,15,400,75
        x0 = 110
        x1 = 490
        y0 = 15
        y1 = 75
        #display today's weather
        if x0 <= x <= x1 and y0 <= y <= y1:
            data.screen = 'weather'
            data.prev.append(data.screen)
        x0 = 100
        x1 = 500
        y0 = 260
        y1 = 350
        #display the next 10 events
        if x0 <= x <= x1 and y0 <= y <= y1:
            data.lstOfEvents = quickstart.calendar(data.email)
            data.screen = 'displayEvents'
            data.prev.append(data.screen)
        x0 = 150
        x1 = 450
        y0 = 100
        y1 = 185
        #open the user's google calendar
        if x0 <= x <= x1 and y0 <= y <= y1:
            webbrowser.open('http://calendar.google.com')
        x0 = 175
        y0 = 425
        x1 = 425
        y1 = 510
        #add an event directly to user's google calendar
        if x0 <= x <= x1 and y0 <= y <= y1:
            googleCalendar.makeEvent(data.email,root)
    
    elif data.screen == 'schedule':
        x0 = 50
        y0 = 100
        x1 = 550
        y1 = 200
        #begin planning the user's schedule
        if x0 <= x <= x1 and y0 <= y <= y1:
            data.screen = 'planSchedule'
            data.prev.append(data.screen)
    elif data.screen == 'planSchedule':
        x0 = 60
        y0 = 140
        x1 = 160
        y1 = 180
        #while there is no valid sleep time, keep asking user for a sleeptime
        if x0 <= x <= x1 and y0 <= y <= y1:
            check = False
            while not check:
                data.updateSleepTime = add.addSleepTime(root)
                if data.updateSleepTime == '12:00 am':
                    data.sleepTime = '24:00'
                else:
                    data.sleepTime = googleCalendar.timeToMilitary(data.updateSleepTime)
                if schedule.checkTime(data.sleepTime):
                        message = "that's too late!"
                        title = "warning box"
                        messagebox.showwarning(title, message)
                else:
                    check = True
        x0 = 40
        y0 = 200
        x1 = 180
        y1 = 240
        #add class information
        if x0 <= x <= x1 and y0 <= y <= y1:
            info = add.addClass(root)
            c = info[0]
            starts = info[1]
            ends = info[2]
            data.classes.append((c,starts,ends))
            schedule.checkClasses(data)
        x0 = 40
        y0 = 260
        x1 = 180
        y1 = 300
        #add meal information
        if x0 <= x <= x1 and y0 <= y <= y1:
            meal = add.addMeal(root)
            while not data.foodAvail:
                info = add.addMealTimes(root,meal)
                start = info[0]
                end = info[1]
                if schedule.check(start,end,data):
                    data.meals.append((meal,start,end))
                    data.foodAvail = True
                else:
                    message = "schedule conflict!"
                    title = "warning box"
                    messagebox.showwarning(title, message)
            schedule.checkMeals(data)
        x0= 40
        y0 = 320
        x1 = 180
        y1 = 360
        #add information about tasks (how long it will take, priority, deadlines)
        if x0 <= x <= x1 and y0 <= y <= y1:
            for item in data.toDo:
                info = add.addPriority(root,item,data)
                time = info[0]
                time = int(2*float(time))
                priority = info[1]
                deadline = info[2]
                data.todoTimes.append((item,time,priority,deadline))
        x0 = 200
        y0 = 525
        x1 = 400
        y1 = 575
        #reset everything
        if x0 <= x <= x1 and y0 <= y <= y1:
            data.meals = []
            data.classes = []
            data.todoTimes = []
            data.updateSleepTime = None
            data.sleepTime = None
            data.schedule = schedule.clear(data.schedule)
            data.madeSched = False
        x0 = 100
        y0 = 400
        x1 = 500
        y1 = 500
        #while there isn't a valid schedule, split the longest
        #assignment into two assignments and try to make the schedule
        #again 
        if x0 <= x <= x1 and y0 <= y <= y1:
            origSched = data.schedule
            if not data.madeSched:
                madeSchedule = False
                data.toDoCopy = copy.deepcopy(data.toDo)
                data.empty = schedule.freeSpaces(data.schedule)
                #check if the schedule can even be mdae
                if schedule.checkValid(data.todoTimes,data.empty):
                    while not madeSchedule:
                        #data.empty = schedule.freeSpaces(data.schedule)
                        sched,c = schedule.generateSchedule(data.schedule,data.todoTimes,data.empty,data.toDoCopy)
                        if sched != None:
                            data.schedule = sched
                            data.toDoCopy = c
                            madeSchedule = True
                    data.madeSched = True
                    #once we have a valid schedule, we want to display this schedule
                    #for the user
                    data.screen = 'generatedSchedule'
                    data.tasks = schedule.makeTaskList(data)
                    data.prev.append(data.screen)
                #if the schedule cannot be made, everything is reset so the
                #user can try again
                else:
                    message = "not enough time to schedule everything!!!"
                    title = "warning box"
                    messagebox.showwarning(title, message)
                    data.meals = []
                    data.classes = []
                    data.todoTimes = []
                    data.updateSleepTime = None
                    data.sleepTime = None
                    data.schedule = schedule.clear(data.schedule)
            else:
                data.screen = 'generatedSchedule'
                data.prev.append(data.screen)
                    
    if data.screen == 'generatedSchedule':
        x0 = 100
        y0 = 500
        x1 = 500
        y1 = 550
        #add the schedule to your google calendar
        if x0 <= x <= x1 and y0 <= y <= y1:
            if not data.addedEvents:
                schedule.addToCalendar(data)
                data.addedEvents = True
    #if the user clicks the "back" button, they go back to the previous page
    if data.screen != 'intro' and data.screen != 'options':
        if 10<=x<=100 and 10<=y<=80:
            if len(data.prev)>0:
                data.screen = data.prev[-2]
                data.prev.pop()

def keyPressed(event, data):
    pass
    
def timerFired(data):
    #keep checking for the date and time
    now = datetime.datetime.now()
    data.year = now.year
    data.day = now.day
    data.month = times.calculateMonth(now.month)
    data.hour,data.minute,data.time = times.calculateTime(now.hour,now.minute)
    
    #if a task is clicked on, calculate new rectangle coordinates for the other
    #tasks that have been shifted up
    if data.clickedOnToDo != None:
        for i in range(data.clickedOnToDo,len(data.checkLstCollision)):
            check = data.checkLstCollision[i]
            x0= check[0]
            x1= check[2]
            y0= check[1]-60
            y1= check[3]-60
            data.checkLstCollision[i] = (x0,y0,x1,y1)
        data.clickedOnToDo = None

#display the intro screen 
def createIntro(canvas,data):
        canvas.create_text(data.width//2,(data.height//3)+3, text='welcome '+
                            str(data.name),font = 'Calibri 70',fill='SlateGray4')
        canvas.create_text(data.width//2,data.height//3, text='welcome '+
                                str(data.name),font = 'Calibri 70',fill='white')

#display date and time 
def displayDate(canvas,data,x,y,size):
    date = data.month+" "+ str(data.day)+" "+str(data.year)
    font = "Calibri "+str(size)
    canvas.create_text(x,y+4, text=date,font = font,fill='gray')
    canvas.create_text(x,y, text=date,font = font,fill='white')
    
def displayTime(canvas,data,x,y,size):
    time = str(data.hour)+":"+str(data.minute)+" "+data.time
    font = "Calibri "+str(size)
    canvas.create_text(x,y+4, text=time,font = font,fill='gray')
    canvas.create_text(x,y, text=time,font = font,fill='white')

#display the options that the user can click on
def createOptions(canvas,data):
    color = "SlateGray2"
    canvas.create_rectangle(100,25,500,125,fill=color,outline =color )
    canvas.create_rectangle(100,175,500,275,fill=color,outline=color)
    canvas.create_rectangle(100,325,500,425,fill=color,outline=color)
    canvas.create_rectangle(100,475,500,575,fill=color,outline=color)
    
    data.rects = [(100,25,500,125),(100,175,500,275),(100,325,500,475),(100,475,500,575)]
    
    msg1 = 'CALENDAR'
    msg2 = 'SYLLABUS'
    msg3 = 'TO-DO LIST'
    msg4 = 'SCHEDULE'
    
    font = 'Calibri 30 bold'
    
    canvas.create_text(data.width//2,75,text=msg1,font=font,fill='white')
    canvas.create_text(data.width//2,225,text=msg2,font=font,fill='white')
    canvas.create_text(data.width//2,375,text=msg3,font=font,fill='white')
    canvas.create_text(data.width//2,525,text=msg4,font=font,fill='white')

#display the to do list with all tasks, the date, time 
def toDoList(canvas,data):
    title = "Today's Agenda"
    displayDate(canvas,data,data.width//2,data.height//5,40)
    
    canvas.create_text(data.width//2,data.height//10+4,text=title,font='Calibri 50',fill='SlateGray3')
    canvas.create_text(data.width//2,data.height//10,text=title,font='Calibri 50',fill='white')
    
    canvas.create_rectangle(50,175,550,575,fill='SkyBlue',outline="SkyBlue")
    font = 'Calibri 30'
    for i in range(len(data.toDo)):
        x = data.width//2
        y = data.height//10 * i + 200
        canvas.create_rectangle(100,data.height//10 *i+175,500,data.height//10 * i+
                                            225,fill='SkyBlue2',outline='SkyBlue2')
        canvas.create_text(x,y,text="- "+data.toDo[i],font=font,fill='white')
    
    canvas.create_rectangle(510,10,590,80,fill='gray',outline='gray')
    canvas.create_text(552,42,text='add',font='Calibri 30',fill='black')
    canvas.create_text(550,40,text='add',font = 'Calibri 30',fill='white')

#display the back button that is on all pages
def backButton(canvas,data):
    canvas.create_rectangle(10,10,100,80,fill='gray',outline='gray')
    canvas.create_text(56,42,text='back',font='Calibri 30',fill='black')
    canvas.create_text(55,40,text='back',font='Calibri 30',fill='white')

#update time and date in the corners of the screen
def updateTime(canvas,data):
    date = data.month+" "+ str(data.day)+" "+str(data.year)
    time = str(data.hour)+":"+str(data.minute)+" "+data.time
    
    displayTime(canvas,data,550,data.height-20,20)
    displayDate(canvas,data,70,data.height-20,20)
    
def redrawAll(canvas, data):
    #based on what the screen is, display the proper information and visuals
    canvas.create_rectangle(0,0,data.width,data.height,fill='LightSkyBlue2',outline='LightSkyBlue2')
    if data.screen == 'intro':
        createIntro(canvas,data)
        displayTime(canvas,data,data.width//2,(data.height//3*2.5),50)
        displayDate(canvas,data,data.width//2,(data.height//3*2),50)
    elif data.screen == 'options':
        createOptions(canvas,data)
        updateTime(canvas,data)
    elif data.screen == 'calendar':
        backButton(canvas,data)
        calendars.drawCalendar(canvas,data)
        updateTime(canvas,data)
    elif data.screen == 'weather':
        backButton(canvas,data)
        calendars.updateWeather(canvas,data)
        updateTime(canvas,data)
    elif data.screen == 'displayEvents':
        backButton(canvas,data)
        calendars.createEvents(canvas,data)
        updateTime(canvas,data)
    elif data.screen == 'syllabus':
        backButton(canvas,data)
        syllabus.drawSyllabus(canvas,data)
        updateTime(canvas,data)
    elif data.screen == 'currentSyllabi':
        backButton(canvas,data)
        updateTime(canvas,data)
        syllabus.currentSyllabi(canvas,data)
    elif data.screen == 'schedule':
        backButton(canvas,data)
        schedule.displaySchedule(canvas,data)
        updateTime(canvas,data)
    elif data.screen == 'planSchedule':
        backButton(canvas,data)
        schedule.planning(canvas,data)
        schedule.updates(canvas,data)
        updateTime(canvas,data)
    elif data.screen == 'generatedSchedule':
        backButton(canvas,data)
        schedule.createdSchedule(canvas,data)
        if data.addedEvents:
            canvas.create_text(data.width//2,575,text='schedule added!',
                                                font='Calibri 25',fill='white')
        updateTime(canvas,data)
    elif data.screen == 'to do':
        backButton(canvas,data)
        toDoList(canvas,data)
        updateTime(canvas,data)
####################################
# use the run function as-is
####################################

def run(width=600, height=600):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    #create global root s0 buttons can be used 
    global root
    root = Tk()
    init(data)
    # create the root and the canvas
    global canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    canvas.data = { }
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run()
