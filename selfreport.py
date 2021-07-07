#!/usr/bin/python3
# coding=UTF-8
from selenium import webdriver
import time
import random
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import json
import sys
import schedule

from sendEmail import email

from selenium.webdriver.support.wait import WebDriverWait

# https://selfreport.shu.edu.cn/ViewDayReport.aspx?day=2021-05-01
class SelfReport(object):

    def __init__(self):
        self.base_url =  "https://selfreport.shu.edu.cn/"
        self.warn_msg = {}  #错误信息字典 {msg:[username, ...], ...}

    def dayDream(self, start=1, end=5):
        t = random.choice(range(start, end))
        # print("daydream", t)
        time.sleep(t)

    def auto_report(self, username, password):
        errorFlag = True   #返回填报情况失败(False)或成功(True)
        if "win" in sys.platform:
            self.driver = webdriver.Chrome(executable_path=r'./chromedriver.exe')
            # self.driver = webdriver.Chrome(executable_path=r'E:/Google/Chrome/Application/chromedriver.exe')
        elif "linux" in sys.platform:
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--headless')
            self.driver = webdriver.Chrome(executable_path=r'./chromedriver', chrome_options=chrome_options)

        # 脚本主体
        driver = self.driver
        try:
            # 请求网页
            driver.get(self.base_url + 'DayReport.aspx')
            url = driver.current_url
            # 如果进入了身份认证界面 进行认证
            if "newsso.shu.edu.cn/login" in url:
                # 填写用户名和密码
                driver.find_element_by_id("username").send_keys(username)
                self.dayDream()
                driver.find_element_by_id("password").send_keys(password)
                self.dayDream()

                # 登陆
                driver.find_element_by_id("submit").click()
                self.dayDream()
            
            # 进入每日填报
            # 勾选承诺
            promise = driver.find_element_by_id("p1_ChengNuo-inputEl-icon")
            promise.click()

            # 勾选在上海：
            driver.find_element_by_id("fineui_7-inputEl-icon").click()
            self.dayDream()

            # 勾选住校：
            driver.find_element_by_id("fineui_9-inputEl-icon").click()
            self.dayDream()

            # 勾选是家庭地址
            driver.find_element_by_id("fineui_12-inputEl-icon").click()
            self.dayDream()
            
            # 提交
            driver.find_element_by_id("p1_ctl01_btnSubmit").click()
            self.dayDream()

            # 按照css_selector找到可能的按钮
            windows = driver.find_elements_by_css_selector(".f-btn.f-noselect.f-state-default.f-corner-all"
                                                                ".f-btn-normal.f-btn-icon-no.f-cmp.f-widget"
                                                                ".f-toolbar-item")
            # 点击确定按钮
            for w in windows:
                if w.text == "确定":
                    w.click()
                    break # 点击后页面会变动，应马上跳出循环
            self.dayDream()
            # 检查是否出现 '正确提交' 提示框
            if "成功" not in driver.find_element_by_class_name("f-messagebox-message").text:
                raise Exception("提交失败")

        # 网络连接超时或者网址错误
        except TimeoutException:
            msg = "base_url error OR timeout\n"
            userArr = self.warn_msg.get(msg, [])
            userArr.append(username)
            self.warn_msg[msg] = userArr
            errorFlag = False
            print(self.warn_msg)

        # 找不到对应元素  在self.warn_msg中写入异常信息
        except Exception as msg:
            msg = str(msg)
            userArr = self.warn_msg.get(msg,[])
            userArr.append(username)
            self.warn_msg[msg] = userArr
            errorFlag = False
            print(self.warn_msg)

        # 未发生异常
        else:
            errorFlag = True

        # 关闭网页
        finally:
            driver.quit()
            return errorFlag

    def readUserGroupInfo(self, file="userInfo.json"):
        """
        read UserGroupInfo from file;
        return a dict object
        """
        with open(file, mode="r", encoding="utf-8") as userFile:
            user = json.load(userFile)
        return user

    def schedule(self, user):
        schedule.every().day.at("09:00").do(self.auto_report, user['username'], user['password'])
        # schedule.every(20).seconds.do(print, user['username'], user['password'])
        # self.auto_report(user['username'], user['password'])
            
    def run(self):
        user = self.readUserGroupInfo()
        self.schedule(user)
        while True:
            schedule.run_pending()
            self.dayDream()
        # # 记录开始时间
        # recordtime = time.time()
        # print(time.localtime(time.time()))
        # # 初始化
        # self.__init__()
        # userList = self.readUserGroupInfo()
        # # 计算每个用户开始时间
        # for user in zip(userList,intervalList):
        #     # user[1] 对应用户的时间偏移量
        #     starttime = recordtime + user[1]
        #     while starttime > time.time():
        #         time.sleep(1)
        #         # print("sleep……")
        #     print("获取用户", user[0]["username"])
        #     print("填报...")
        #     errorFlag = self.auto_report(user[0]["username"], user[0]["password"], type)
        #     print("写日志...\n")
        #     self.writeLog(user[0]["username"], type, errorFlag)

        # if self.warn_msg != {}:
        #     self.writeError(type)
        #     #发送邮件
        #     mail = email()
        #     #编辑邮件标题和内容
        #     subject = ("晨报出错" if type == 1 else "晚报出错")
        #     content = ""
        #     for error in self.warn_msg:
        #         content += error
        #         for user in self.warn_msg[error]:
        #             content = content + user + "\n"
        #     #发送
        #     mail.send(subject, content)

    def writeLog(self, username, type, errorFlag):
        file_handle = open('log.txt', mode='r+',encoding='utf-8')
        old = file_handle.read()
        file_handle.seek(0)
        file_handle.write('\n')
        file_handle.write('='*100)
        file_handle.write('\n')
        file_handle.write(time.ctime())
        file_handle.write('\n')
        file_handle.write('用户: '+username)
        file_handle.write('\n')
        msg = "成功" if errorFlag else "失败"
        file_handle.write("晨报填报"+msg if type == 1 else "晚报填报"+msg)
        file_handle.write('\n')
        file_handle.write('='*100)
        file_handle.write('\n')
        file_handle.write(old)
        file_handle.close()

    def writeError(self, type):
        file_handle = open('log.txt', mode='r+',encoding='utf-8')
        old = file_handle.read()
        file_handle.seek(0)
        file_handle.write('\n')
        file_handle.write('='*100)
        file_handle.write('\n')
        file_handle.write(time.ctime())
        file_handle.write('\n')
        file_handle.write("晨报出错" if type == 1 else "晚报出错")
        file_handle.write('\n')
        file_handle.write("错误详情:\n")
        for error in self.warn_msg:
            file_handle.write(error)
            for user in self.warn_msg[error]:
                file_handle.write(user+"\n")
        file_handle.write('\n')
        file_handle.write('='*100)
        file_handle.write('\n')
        file_handle.write(old)
        file_handle.close()


if __name__ == '__main__':
    sp = SelfReport()
    sp.run()
