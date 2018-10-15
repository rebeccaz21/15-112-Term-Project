from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog

#code taken from fall 2015 notes: http://www.kosbie.net/cmu/fall-16/15-112/notes/notes-tkinter-demos.html
#modified to fit project
#this file consists of all the buttons that are used in the project

#ask about where the user lives to check for the weather
def addCity(root):
    msg = "what city do you live in?"
    response = simpledialog.askstring('city', msg,parent=root)
    return response

#let user add a task to the to-do list
def askForTask(root):
    msg = "what do you need to get done?"
    response = simpledialog.askstring('add task', msg,parent=root)
    return response

#let user link classes+syllabi for the semester
def addSyllabus(root):
    msg1 = 'what class is this for?'
    c = simpledialog.askstring('class', msg1,parent=root)
    msg2 = 'what is the link to '+c+' syllabus?'
    link = simpledialog.askstring('link', msg2,parent=root)
    return (c,link)

#let user input what time they would like to sleep
def addSleepTime(root):
    msg = "what time do you want to sleep?"
    response = simpledialog.askstring('sleep time', msg,parent=root)
    return response

# add a class and times while planning schedule
def addClass(root):
    msg1 = 'what class do you have?'
    c = simpledialog.askstring('class', msg1,parent=root)
    msg2 = 'what time does '+c+' start?'
    start = simpledialog.askstring('start', msg2,parent=root)
    msg3 = 'what time does '+c+' end?'
    end = simpledialog.askstring('end', msg3,parent=root)
    return c,start,end

#add a meal while planning schedule
def addMeal(root):
    msg = "what meal is this?"
    response = simpledialog.askstring('meal', msg,parent=root)
    return response

#add times for meals
def addMealTimes(root,meal):
    msg1 = 'what time does '+meal+' start?'
    start = simpledialog.askstring('start',msg1,parent=root)
    msg2 = 'what time does '+meal+' end?'
    end = simpledialog.askstring('end',msg2,parent=root)
    return (start,end)

#prioritize tasks and whether they will have deadlines / how long they will take
def addPriority(root,item,data):
    msg1 = 'how long will '+item+' take?'
    time = simpledialog.askstring('time',msg1,parent=root)
    msg2 = 'how important is '+item+' on a scale of 1-5?'
    priority = int(simpledialog.askstring('priority',msg2,parent=root))
    msg3 = 'does '+item+' have a deadline?'
    deadline = simpledialog.askstring('deadline', msg3,parent=root)
    #if the task has no deadline, then the deadline is just by the time
    #the user wants to sleep
    if deadline == 'yes':
        msg4 = 'what time is '+item+' due?'
        deadlineTime = simpledialog.askstring('time',msg4,parent=root)
    else:
        deadlineTime = data.sleepTime
    return (time,priority,deadlineTime)
    