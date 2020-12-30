import random
import time
from selfreport import SelfReport

class timing:

    def __init__(self,userList=[]):
        self.userNum = userList.__len__()

    # start开始时间list  end结束时间list
    def setEffectTime(self,start,end):
        self.startList = start
        self.endList = end
        self.reported_flag = [False] * start.__len__()

    # 设置随机时间间隔
    def setInterval(self, minduration=60):
        self.minduration = minduration
        self.intervalList = []
        random.seed()
        for duration in zip(self.startList,self.endList):
            starttime = time.mktime(time.strptime("2000-"+duration[0],"%Y-%H:%M"))
            endtime = time.mktime(time.strptime("2000-"+duration[1], "%Y-%H:%M"))
            interval = endtime - starttime
            # print(interval)

            # 人数 * 最短时间 > 总时间间隔  无法完成运行
            if self.userNum * minduration > interval:
                raise Exception("错误:人数过多，时间间隔过短")

            # resttime = 总时间间隔 - 人数 * 最短时间 是可随机分配的时间
            resttime = interval - self.userNum * minduration

            # condition1 可分配时间秒数 < 人数
            if resttime < self.userNum:
                addlist = [0] * self.userNum # 时间点偏移量(以最小时间间隔为基准)
                for i in range(int(resttime)):
                    index = random.randint(0,self.userNum-1)
                    addlist[index]+=1
                intervallist = [] # 当前时间段开始时间点列表
                suminterval = 0
                for i in range(self.userNum):
                    suminterval += addlist[i]
                    intervallist.append(suminterval)
                    suminterval += minduration
                self.intervalList.append(intervallist)
                # print(self.intervalList)

            # condition2 可分配时间秒数 >= 人数
            else:
                addlist = [s for s in range(int(resttime))]
                intervallist = random.sample(addlist,self.userNum)
                intervallist.sort()
                for i in range(len(intervallist)):
                    intervallist[i] = intervallist[i] + i * minduration
                self.intervalList.append(intervallist)
            print(self.intervalList)

    # 监听时间，在确定区间自动填报
    def checkTime(self,func,sleeptime=10):
        hour = time.localtime().tm_hour
        minute = time.localtime().tm_min
        # 零点更新时间间隔，刷新系统reported_flag[]以及每个用户mor_report_flag, eve_report_flag
        if hour == 0 and minute == 0:
            self.setInterval(self.minduration)
            self.reported_flag = [False] * self.reported_flag.__len__()
        index = 0
        # 检查starttime执行填报程序
        for start in self.startList:
            starttime = time.strptime(start, "%H:%M")
            index += 1
            if starttime.tm_hour == hour and starttime.tm_min == minute and not self.reported_flag[index-1]:
                func(index,self.getIntervalList()[index-1])
                self.reported_flag[index-1] = True
        # 刷新间隔
        time.sleep(sleeptime)

    # 返回用户填报时间间隔列表
    def getIntervalList(self):
        return self.intervalList


if __name__ == '__main__':
    a = ["7:00", "00:19"]
    b = ["7:03", "00:22"]
    sp = SelfReport()
    userList = sp.readUserGroupInfo()
    timer = timing(userList)
    timer.setEffectTime(a,b)
    timer.setInterval()
    while True:
        timer.checkTime(sp.run,5)