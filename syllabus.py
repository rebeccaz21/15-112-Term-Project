import add 
#this file handles the functions necessary for the syllabus screen

#stores information about the class + link for syllabus
def uploadSyllabus(data,root):
    info = add.addSyllabus(root)
    data.syllabi.append(info)
    print(data.syllabi)
    
    for i in range(len(data.syllabi)):
        x0 = data.width//2 - 75
        x1 = data.width//2 + 75
        y0 = data.height//10 * i + 75
        y1 = data.height//10 * i + 125
        if (x0,y0,x1,y1) not in data.syllabiCoords:
            data.syllabiCoords.append((x0,y0,x1,y1))
            
#draw rectangles and classes and what season / year it is
def currentSyllabi(canvas,data):
    spring = ['march','april', 'may']
    fall = ['september','october','november']
    summer = ['june','july','august',]
    winter = ['december','january','february']
    
    if data.month in spring:
        season = 'spring'
    elif data.month in fall:
        season = 'fall'
    elif data.month in summer:
        season = 'summer'
    elif data.month in winter:
        season = 'winter'
    year = data.year
    
    canvas.create_text(data.width//2,37,text=season+' '+str(year),font='Calibri 30',fill='gray')
    canvas.create_text(data.width//2,35,text=season+' '+str(year),font='Calibri 30',fill='white')
    

    for j in range(len(data.syllabiCoords)):
        canvas.create_rectangle(data.syllabiCoords[j],fill='SkyBlue2',outline='SkyBlue2')
        x = data.width//2 
        y = data.height//10 *j +100
        canvas.create_text(x,y+3,text=data.syllabi[j][0],font='Calibri 20',fill='SteelBlue2') 
        canvas.create_text(x,y,text=data.syllabi[j][0],font='Calibri 20',fill='white')

#create the syllabus screen with buttons
def drawSyllabus(canvas,data):
    text = 'link syllabus!'
    canvas.create_rectangle(100,150,500,250,fill='SlateGray1',outline='SlateGray1')
    canvas.create_text(data.width//2+2,204,text=text,font='Calibri 50',fill='gray')
    canvas.create_text(data.width//2,200,text=text,font='Calibri 50',fill='white')

    text2 = 'current syllabi'
    canvas.create_rectangle(100,350,500,450,fill='SlateGray1',outline='SlateGray1')
    canvas.create_text(data.width//2+2,404,text=text2,font='Calibri 50',fill='gray')
    canvas.create_text(data.width//2,400,text=text2,font='Calibri 50',fill='white')

#display the scehdule
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