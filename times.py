#changes from number month to word month
def calculateMonth(month):
    months = ['','january','february','march','april','may','june','july',
    'august','september','october','november','december']
    strMonth = months[month]
    return strMonth
    
#change 24-hour time to 12-hour time
def calculateTime(hour,minute):
    if hour > 12:
        time = 'PM'
    else:
        time = 'AM'
    hour = hour%12
    if hour == 0:
        hour = 12
    if minute < 10:
        minute = "0"+str(minute)
    return hour, minute, time


