from tkinter import *

#code taken from https://stackoverflow.com/questions/31394170/python-storing-user-input
#modified to fit project
#gather basic information from the user (name and email) 

def getStarterInfo():
    master = Tk()    
    l = Label(master, text="name")    
    l.pack()
    # create Entry for user
    e = Entry(master)
    e.pack()
    l2 = Label(master, text="email")
    l2.pack()
    # create Entry for pass and show * when user types their password
    e2 = Entry(master)
    e2.pack()
    e.focus_set()
        
    # callback function to save the username and password
    def callback():
        with open("nameAndEmail.txt","a")as f:
            f.write("{},{}\n".format(e.get(),e2.get()))
        # command set to callback when button is pressed
    b = Button(master, text="Save", width=10, command=callback)
    b.pack()
    
    mainloop()
    
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

#get information from the file that has the name and email stored
def readInfo(filename):
    info = readFile(filename)
    summary = ""
    for line in info.splitlines():
        first = line.find(",")
        name = line[0:first]
        email = line[first+1:]
    return name,email

getStarterInfo()
