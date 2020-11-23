import time

def checktime(func1,func2):
    hour = time.localtime().tm_hour
    if str(hour)=="8":
        func1(1)
    elif str(hour) == "21":
        func2(2)
    time.sleep(3600)