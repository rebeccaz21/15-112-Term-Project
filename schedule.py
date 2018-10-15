import datetime
import quickstart
import copy
import googleCalendar

#this file handles the functions that are involved in creating and displaying the 
#user's schedule

#initializes the schedule
def startSchedule():
    d = [['00:00',""],['00:30',""],['01:00',""],['01:30',""],['02:00',""],
    ['02:30',""],['03:00',""],['03:30',""],['04:00',""], ['04:30',""],
    ['05:00',""],['05:30',""],['06:00',""],['06:30',""],['07:00',""],
    ['07:30',""],['08:00',""],['08:30',""],['09:00',""],['09:30',""],
    ['10:00',""],['10:30',""],['11:00',""],['11:30',""],['12:00',""],
    ['12:30',""],['13:00',""],['13:30',""],['14:00',""],['14:30',""],
    ['15:00',""],['15:30',""],['16:00',""],['16:30',""],['17:00',""],
    ['17:30',""],['18:00',""],['18:30',""],['19:00',""],['19:30',""],
    ['20:00',""],['20:30', ""],['21:00',""],['21:30',""],['22:00',""],
    ['22:30',""],['23:00',""],['23:30',""],['24:00',""]]
    return d

#changes from number month to word month
def calculateMonth(month):
    months = ['','january','february','march','april','may','june','july',
    'august','september','october','november','december']
    strMonth = months[month]
    return strMonth

#convert time to military
def timeToMilitary(time):
    intTime = ""
    if len(time) == 7:
        intTime = time[0:1]+time[2:4]
    elif len(time) == 8:
        intTime = time[0:2] + time[3:5]
    intTime = int(intTime)
    if time[-2] == 'p':
        intTime += 1200
    elif time[-2] == 'a':
        pass
    if time == '12:00 am':
        intTime = 0
    elif time == '12:30 am':
        intTime = '30'
    elif time == '12:00 pm':
        intTime = 1200
    elif time == '12:30 pm':
        intTime = 1230
    return intTime

#checks that sleep time is not later than 12:00 am
#to encourage the user to sleep early
def checkTime(sleepTime):
    if len(sleepTime) == 5:
        sleepTime = sleepTime[0:2]+sleepTime[3:]
    else:
        sleepTime = sleepTime[1:3]+sleepTime[4:]
    #change the sleeptime to be an int so that we can compare times
    sleepTime = int(sleepTime)
    if sleepTime == 0 or sleepTime == 2400:
        return False
    if sleepTime<1000:
        return True
    return False

#checks that there isn't an event in a time slot
def check(start,end,data):
    #change start and end times to be in military so they can be compared
    startTime = timeToMilitary(start)
    endTime = timeToMilitary(end)
    for i in range(len(data.schedule)):
        key = data.schedule[i][0]
        checkKey = key[0:2]+key[3:]
        if checkKey == "0000":
            checkKey = 0
        elif checkKey == "0030":
            checkKey = 30
        elif checkKey[0] == '0':
            checkKey = checkKey[1:]
        checkKey = int(checkKey)
        #if the time in data.schedule is within the range of the start
        #and end time, check whether there is an empty or nonempty slot
        if startTime - checkKey <= 0 and endTime - checkKey > 0:
            if data.schedule[i][1] != '':
                return False
    return True

#rearranges tasks in order of priority
#we arrange based on priority and not deadline because it is assumed that
#deadlines would have higher priority already
def rearrange(lstOfTasks):
    lst = []
    taskLst = copy.deepcopy(lstOfTasks)
    p = 5
    while len(lst) != len(lstOfTasks):
        for item in taskLst:
            priority = item[2]
            if priority == p:
                lst.append(item)
                # taskLst.remove(item)
        p -= 1
    return lst

#gets the first time with an open time slot
def getEmpty(schedule):
    for i in range(len(schedule)):
        if schedule[i][1] == "":
            return i

#finds how many consecutive empty time slots there are from firstEmpty
def howManyEmpty(schedule, firstEmpty):
    consecutive = True
    count = 0
    for i in range(firstEmpty,len(schedule)):
        key = schedule[i][0]
        if schedule[i][1] == "":
            count += 1
        else:
            consecutive = False
            return count,schedule[i-1][0]
    return count,schedule[len(schedule)-1][0]

#creates a list of all the empty spots (start,end,how many spaces)
# we will us this when creating the schedule
def freeSpaces(schedule):
    empty = []
    index = 0
    while index < len(schedule):
        if schedule[index][1] == "":
            start = schedule[index][0]
            result = howManyEmpty(schedule,index)
            counts = result[0]
            end = result[1]
            empty.append((start,end,counts))
            if counts == 0:
                index += 1
            else:
                index = schedule.index([start,''])+counts
        else:
            index +=1
    return empty

#place the task down in the slots
def placeTask(schedule,task,numSpaces,startIndex):
    for i in range(startIndex,startIndex+numSpaces):
        schedule[i][1] = task
    print(schedule)
    return schedule

#takes the longest task and splits it into two
#this is to prevent the user from doing a task for too long and thus 
#improve productivity
def splitTasks(tasks,empty,copyOfTasks):
    maxHour = 0
    maxItem = None
    #search for the task with the longest time
    for item in tasks:
        hour = item[1] 
        if hour > maxHour:
            maxItem = item
            maxHour = hour
    tasks.remove(maxItem)
    task = maxItem[0]
    hour = maxItem[1]
    priority = maxItem[2]
    deadline = maxItem[3]
    
    #split the task into two and replace the old task with these two new tasks
    newItem1 = (task,hour//2,priority,deadline)
    newItem2 = (task+' ', hour - (hour//2), priority,deadline)
    
    tasks.append(newItem1)
    tasks.append(newItem2)
    copyOfTasks.append(task+' ')
    return tasks,copyOfTasks

#checks to make sure we can schedule everything in the schedule
#by checking how many free spaces are available and how many free spaces are
#needed
def checkValid(taskTimes, schedTimes):
    count1 = 0
    count2 = 0
    for item in taskTimes:
        hours = item[1]
        count1 += hours
        
    for item in schedTimes:
        hours = item[2]
        count2 += hours
    if count1 <= count2:
        return True
    else:
        return False
        
#generate schedule
def generateSchedule(schedule,tasks,empty,copyOfTasks):
    ind = 0
    #while we still have tasks to place into the schedule and we have not reached
    #the end of the tasks list
    while len(tasks) != 0 and ind < len(tasks):
        placed = False
        canMoveOn = False
        #start by looking at a task
        task = tasks[ind]
        name = task[0]
        hours = task[1]
        deadline = task[3]
        
        #if there is a deadline: change the deadline to be an int to be compared
        if len(deadline) != 5:
            deadlineCheck = googleCalendar.timeToMilitary(deadline)
        else:
            deadlineCheck = deadline
        deadlineCheck = deadlineCheck[0:2]+deadlineCheck[3:]
        if deadlineCheck == "0000":
            deadlineCheck = 0
        elif deadlineCheck == "0030":
            deadlineCheck = 30
        elif deadlineCheck[0] == '0':
            deadlineCheck = deadlineCheck[1:]
        deadlineCheck = int(deadlineCheck)
        print('task we are trying to fit', task)
        #look through all the empty spaces and see if this task will fit
        for i in range(len(empty)):
            time = empty[i]
            print('time we are looking at ',time)
            start = time[0]
            end = time[1]
            numSpaces = time[2]
            
            checkStart = start[0:2]+start[3:]
            if checkStart == "0000":
                checkStart = 0
            elif checkStart == "0030":
                checkStart = 30
            elif checkStart[0] == '0':
                checkStart = checkStart[1:]
            checkStart = int(checkStart) + 30*(hours)
            #if there are enough spaces, then we place the task down into the
            #schedule
            if hours <= numSpaces:
                if deadlineCheck - checkStart >= 0:
                    startIndex = schedule.index([start,''])
                    schedule = placeTask(schedule,name,hours,startIndex)
                    print('placed!')
                    tasks.remove(task)
                    #we reupdate the order of the tasks and how many empty 
                    #spaces there are
                    tasks = rearrange(tasks)
                    empty = freeSpaces(schedule)
                    placed = True
                    break
        if not placed:
            print('we need to split!')
            info = splitTasks(tasks,empty,copyOfTasks)
            tasks= info[0]
            copyOfTasks = info[1]
            print('now tasks are: ',tasks)
            tasks = rearrange(tasks)
            
    print(schedule)
    if len(tasks) != 0:
        return None
    else:
        return schedule,copyOfTasks


#checks when to start schedule, the closest half hour
def start(hour,min):
    if hour == 22 and min > 45:
        startTime = 0
    else:
        if abs(min-30) < 15:
            startTime = hour*100 + 30
        elif min - 30 > 0:
            startTime = hour*100+100
        elif min - 30 <= 0:
            startTime = hour*100
        hour = startTime // 100
        min = startTime % 100
    if hour == 11 and min > 45:
        startTime = "1200"
        hour = '12'
        min = 0
    elif hour == 12 and min > 15:
        hour = '12'
        min = 30
    if min == 0:
        min = "00"
    startTime = str(hour)+str(min)
    if startTime[0] == '0':
        startTime = startTime[1:]
    startTime = int(startTime)
    return startTime

#changes sleeptime to int value to be compared
def getEnd(endTime):
    if len(endTime) == 5:
        endTime = endTime[0:2]+endTime[3:]
    else:
        endTime = endTime[1:3]+endTime[4:]
    if endTime[0] == ' ':
        endTime = endTime[1:]
    endTime = int(endTime)
    return endTime

#update schedule so the only valid times are present times to sleep times
def updateSchedule(data,startTime,endTime):
    for i in range(len(data.schedule)):
        key = data.schedule[i][0]
        checkKey = key[0:2]+key[3:]
        if checkKey == "0000":
            checkKey = 0
        elif checkKey == "0030":
            checkKey = 30
        elif checkKey[0] == '0':
            checkKey = checkKey[1:]
        checkKey = int(checkKey)
        if endTime == 0:
            if startTime - checkKey > 0:
                data.schedule[i][1] = None
        else:
            if startTime - checkKey > 0:
                data.schedule[i][1] = None
            if endTime - checkKey <= 0 :
                data.schedule[i][1] = "sleep"  
    print(data.schedule)

#convert event times to numbers
def checkEventTimes(time):
    check = time[:2]
    if check[0] == '0':
        check = check[1:]
    if len(check) == 4:
        check = check+time[2:]
    else:
        check = check+time[3:]
    return int(check)

#check if there are any events today and updates the schedule
def checkEvents(canvas,data):
    data.lstOfEvents = quickstart.calendar(data.email)
    if data.lstOfEvents[0] != 'No upcoming events found.':
        for item in data.lstOfEvents:
            date = item[0]
            day = date[8:10]
            day = int(day)
            year = date[:4]
            year = int(year)
            month = date[5:7]
            if month[0] == 0:
                month=month[1:]
            month = int(month)
            now = datetime.datetime.now()
            currYear = now.year
            currDay = now.day
            currMonth = now.month
            
            if currYear == year and currMonth == month and currDay == day:
                startTime = date[11:16]
                startTime = checkEventTimes(startTime)
                ending = item[1]
                endTime = ending[11:16]
                endTime = checkEventTimes(endTime)
                summary = item[2]
                for i in range(len(data.schedule)):
                    key = data.schedule[i][0]
                    checkKey = key[0:2]+key[3:]
                    if checkKey == "0000":
                        checkKey = 0
                    elif checkKey == "0030":
                        checkKey = 30
                    elif checkKey[0] == '0':
                        checkKey = checkKey[1:]
                    checkKey = int(checkKey)
                    if startTime - checkKey <= 0 and endTime - checkKey >= 0:
                        data.schedule[i][1] = summary
                        
#update schedule according to class times
def checkClasses(data):
    for c in data.classes:
        cl = c[0]
        startTime = c[1]
        startTime = timeToMilitary(startTime)
        endTime = c[2]
        endTime = timeToMilitary(endTime)
        for i in range(len(data.schedule)):
            key = data.schedule[i][0]
            checkKey = key[0:2]+key[3:]
            if checkKey == "0000":
                checkKey = 0
            elif checkKey == "0030":
                checkKey = 30
            elif checkKey[0] == '0':
                checkKey = checkKey[1:]
            checkKey = int(checkKey)
            if startTime - checkKey <= 0 and endTime - checkKey > 0:
                data.schedule[i][1] = cl
                
#update schedule according to meal times
def checkMeals(data):
    for meal in data.meals:
        m = meal[0]
        startTime = meal[1]
        startTime = timeToMilitary(startTime)
        endTime = meal[2]
        endTime = timeToMilitary(endTime)
        for i in range(len(data.schedule)):
            key = data.schedule[i][0]
            checkKey = key[0:2]+key[3:]
            if checkKey == "0000":
                checkKey = 0
            elif checkKey == "0030":
                checkKey = 30
            elif checkKey[0] == '0':
                checkKey = checkKey[1:]
            checkKey = int(checkKey)
            if startTime - checkKey <= 0 and endTime - checkKey > 0:
                data.schedule[i][1] = m
    data.foodAvail = False

#option to add a class
def addClasses(canvas,data):
    canvas.create_rectangle(40,200,180,240,fill='SkyBlue2',outline='SkyBlue2')
    canvas.create_text(110,220,text='add class',font='Calibri 20',fill='white')

#option to add a meal
def addEat(canvas,data):
    canvas.create_rectangle(40,260,180,300,fill='SkyBlue2',outline='SkyBlue2')
    canvas.create_text(110,280,text='add meal',font='Calibri 20',fill='white')

#rank tasks and estimate time for each
def todoTimes(canvas,data):
    canvas.create_rectangle(40,320,180,360,fill='SkyBlue2',outline='SkyBlue2')
    canvas.create_text(110,340,text='times for tasks',font='Calibri 20',fill='white')

#plans start and end times
def planning(canvas,data):
    now = datetime.datetime.now()
    hour = int(now.hour)
    min = int(now.minute)
    startTime = start(hour,min)
    starts = startTime
    
    if startTime == 0:
        startStatus = ' AM'
    if startTime == 1200:
        startStatus = ' PM'
    elif startTime == 1230:
        startStatus = ' PM'
    elif startTime > 1200:
        startStatus = ' PM'
        starts -= 1200
    else:
        startStatus = ' AM'
        starts = startTime
    textStart = str(starts)
    if int(textStart) < 1000:
        textStart = textStart[0:1]+":"+textStart[1:]
    else:
        textStart = textStart[0:2]+":"+textStart[2:]
    if startTime == 0:
        textStart = '12:00'
    elif startTime == 30:
        textStart = '12:30'
        
    #displays the start and end time
    canvas.create_rectangle(60,85,160,125,fill='SkyBlue2',outline='SkyBlue2')
    canvas.create_text(115,105,text='start time: ',font='Calibri 20',
    fill = 'white')
    canvas.create_text(215,105,text= textStart+startStatus,font='Calibri 20',fill='white')
    
    canvas.create_rectangle(60,140,160,180,fill='SkyBlue2',outline='SkyBlue2')
    canvas.create_text(115,155,text='end time: ',font="Calibri 20", fill='white')
    
    endTime = data.updateSleepTime
    canvas.create_text(215,155,text=endTime,font='Calibri 20',fill='white')
    #once we have a valid sleeptime, we want to update the schedule based
    #on times for sleeping, classes, events, and meals
    #create the button option to input times for tasks and the 'generate schedule'
    #button
    if endTime != None:
        if endTime == '12:00 am':
            endTime = 2400 
        else:
            endTime = timeToMilitary(endTime)
        updateSchedule(data,startTime,endTime)
        checkEvents(canvas,data)
        addClasses(canvas,data)
        addEat(canvas,data)
        d = todoTimes(canvas,data)
            
        generateButton(canvas,data)
        generateReset(canvas,data)

def generateReset(canvas,data):
    canvas.create_rectangle(200,525,400,575,fill='SkyBlue2',outline='SkyBlue2')
    canvas.create_text(300,550,text='reset',font='Calibri 25',fill='white')

#update schedule page to display meals, tasks, and classes
def updates(canvas,data):
    if len(data.classes) != 0:
        for i in range(len(data.classes)):
            y = 220
            x = data.height//5 * i + 250
            canvas.create_text(x,y,text=data.classes[i][0],font='Calibri 17',fill='white')
    if len(data.meals) != 0:
        for i in range(len(data.meals)):
            y = 270
            x = data.height//5 * i + 250
            canvas.create_text(x,y,text=data.meals[i][0],font='Calibri 20',fill='white')
    if len(data.todoTimes) != 0:
        for i in range(len(data.todoTimes)):
            y = 340
            x = data.height//8 * i + 250
            canvas.create_text(x,y,text=data.todoTimes[i][0],font='Calibri 17',fill='white')

#taken from https://stackoverflow.com/questions/31691007/0-23-hour-military-clock-to-standard-time-hhmm
#modified to fit project better
def timeConvert(miliTime):
    hours, minutes = miliTime.split(":")
    hours, minutes = int(hours), int(minutes)
    setting = "am"
    if hours == 12:
        setting = "pm"
    elif hours > 12 and hours != 24:
        setting = "pm"
        hours -= 12
    elif hours == 0 or hours == 24:
        setting = 'am'
        hours = 12
    return(("%02d:%02d" +' '+ setting) % (hours, minutes))

        
#display the generated schedule
def createdSchedule(canvas,data):
    seen = set()
    schedule = copy.deepcopy(data.schedule)

    index = 0
    #update the schedule so that only the first instance of a task and its 
    #start time is in the list
    while index < len(schedule):
        removed = False
        if schedule[index][1] == None or schedule[index][1] == '':
            schedule.remove(schedule[index])
            removed = True
        elif schedule[index][1] in seen:
            schedule.remove(schedule[index])
            removed = True
        else:
            seen.add(schedule[index][1])
        if not removed:
            index += 1
            
    # format the display based on how many items are in the schedule
    if len(schedule) > 6:
        for i in range(len(schedule)//2):
            x0 = data.width//4 - 60
            x1 = data.width//4 + 60
            y = data.height//10 * i + 100
            time = timeConvert(schedule[i][0])
            event = schedule[i][1]
            canvas.create_text(x0,y,text=time,font='Calibri 20',fill='white')
            canvas.create_text(x1,y,text=event,font='Calibri 22',fill='white')
            
        i = 0
        for j in range(len(schedule)//2,len(schedule)):
            x0 = data.width//4 * 2+ 35
            x1 = data.width//4 * 2 + 185
            y = data.height//10 * i + 100
            time = timeConvert(schedule[j][0])
            event = schedule[j][1]
            canvas.create_text(x0,y,text=time,font='Calibri 20',fill='white')
            canvas.create_text(x1,y,text=event,font='Calibri 22',fill='white')
            i += 1
    else:
        for i in range(len(schedule)):
            x0 = data.width//2 - 100
            x1 = data.width//2 + 100
            y = data.height//10 * i + 100
            time = timeConvert(schedule[i][0])
            event = schedule[i][1]
            canvas.create_text(x0,y,text=time,font='Calibri 20',fill='white')
            canvas.create_text(x1,y,text=event,font='Calibri 20',fill='white')
        
    canvas.create_text(data.width//2, 53,text='todays schedule',font = 'Calibri 30', fill='gray')
    canvas.create_text(data.width//2, 50,text='todays schedule',font = 'Calibri 30', fill='white')
    
    canvas.create_rectangle(100,500,500,550,fill='SteelBlue',outline='SteelBlue')
    canvas.create_text(data.width//2,528,text='add to google calendar!', font='Calibri 25',fill='SkyBlue2')
    canvas.create_text(data.width//2,525,text='add to google calendar!',font='Calibri 25',fill='white')
    

#display schedule planner
def displaySchedule(canvas,data):
    canvas.create_rectangle(50,100,550,200,fill='white',outline='white')
    canvas.create_text(data.width//2, 152, text= "let's plan today's schedule",
        font = "Calibri 40",fill='black')
    canvas.create_text(data.width//2, 150, text= "let's plan today's schedule",
        font = "Calibri 40",fill='gray')
    
    font = 'Calibri 30'
    if len(data.toDo) == 0:
        canvas.create_text(data.width//2, 300, text='nothing to do!', font=font,fill='white')
    for i in range(len(data.toDo)):
        x = data.width//2
        y = data.height//10 * i + 250
        canvas.create_text(x,y,text="- "+data.toDo[i],font=font,fill='white')

#display the button to generate the schedule
def generateButton(canvas,data):
    canvas.create_rectangle(100,400,500,500,fill='SkyBlue2',outline='SkyBlue2')
    canvas.create_text(data.width//2, 450,text='generate schedule',font='Calibri 40', fill='white')

#find the end time of a task and it's index
def endForTask(schedule,index,item):
    consecutive = True
    for i in range(index,len(schedule)):
        key = schedule[i][0]
        if schedule[i][1] == item:
            pass
        else:
            consecutive = False
            return i,schedule[i][0]
    return i, schedule[len(schedule)-1][0]

#make a list of tasks and their start and end times
def makeTaskList(data):
    tasks = []
    for item in data.toDoCopy:
        index = 0
        nextInd = None
        while index < len(data.schedule):
            if data.schedule[index][1] == item:
                startTime = data.schedule[index][0]
                nextInd, endTime = endForTask(data.schedule,index,item)
                startTime = timeConvert(startTime)
                endTime = timeConvert(endTime)
                tasks.append((item,startTime,endTime))
            if nextInd == None:
                index += 1
            else:
                index += nextInd
                nextInd = None
    return tasks

# add all meals, classes, and tasks to your google calendar for the day
def addToCalendar(data):
    for meal in data.meals:
        summary = meal[0]
        start = meal[1]
        end = meal[2]
        googleCalendar.makeEvent(data.email,None,False,summary,data.month,str(data.day),str(data.year),start,end)
    for c in data.classes:
        summary = c[0]
        start = c[1]
        end = c[2]
        googleCalendar.makeEvent(data.email,None,False,summary,data.month,str(data.day),str(data.year),start,end)

    for item in data.tasks:
        summary = item[0]
        start = item[1]
        end = item[2]
        googleCalendar.makeEvent(data.email,None,False,summary,data.month,str(data.day),str(data.year),start,end)

def clear(schedule):
    for i in range(len(schedule)):
        event = schedule[i][1]
        if event != None:
            schedule[i][1] = ''
    return schedule
    