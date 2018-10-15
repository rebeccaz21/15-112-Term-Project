
#create screen that displays the to do list
def toDoList(canvas,data):
    title = "Today's Agenda"
    termproject1.displayDate(canvas,data,data.width//2,data.height//5,40)
    
    canvas.create_text(data.width//2,data.height//10+4,text=title,font='Calibri 50',fill='SlateGray3')
    canvas.create_text(data.width//2,data.height//10,text=title,font='Calibri 50',fill='white')
    
    canvas.create_rectangle(50,175,550,575,fill='SkyBlue',outline="SkyBlue")
    font = 'Calibri 30'
    for i in range(len(data.toDo)):
        x = data.width//2
        y = data.height//10 * i + 200
        canvas.create_rectangle(100,data.height//10 *i+175,500,data.height//10 * i+225,fill='SkyBlue2',outline='SkyBlue2')
        canvas.create_text(x,y,text="- "+data.toDo[i],font=font,fill='white')
    
    #the add button
    canvas.create_rectangle(510,10,590,80,fill='gray',outline='gray')
    canvas.create_text(552,42,text='add',font='Calibri 30',fill='black')
    canvas.create_text(550,40,text='add',font = 'Calibri 30',fill='white')