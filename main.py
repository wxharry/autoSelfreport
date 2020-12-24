from Timing import timing
import selfreport

if __name__ == '__main__':
    print("START")
    start = ["7:05", "20:05"]
    end = ["8:55", "21:55"]
    sp = selfreport.SelfReport()
    userList = sp.readUserGroupInfo()
    t = timing(userList)
    t.setEffectTime(start,end)
    t.setInterval()
    while True:
        t.checkTime(sp.run,5)