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

from selenium.webdriver.support.wait import WebDriverWait


class SelfReport(object):

    def __init__(self):
        self.base_url =  "https://selfreport.shu.edu.cn/"
        self.warn_msg = {}  #错误信息字典 {msg:[username, ...], ...}

    def auto_report(self, username, password, type):
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
            driver.get(self.base_url + 'Default.aspx')
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))

            # 填写用户名和密码
            driver.find_element_by_id("username").send_keys(username)
            driver.find_element_by_id("password").send_keys(password)

            # 登陆
            driver.find_element_by_id("submit").click()

            # 进入每日填报
            # 可能出现需要读消息的情况，用读取href避开
            lnkReport = driver.find_element_by_id("lnkReport")
            lnkReport_href = lnkReport.get_attribute("href")
            driver.get(lnkReport_href)
            time.sleep(1)

            # 选择晨报/晚报 晨报p1_Button1 晚报p1_Button2
            driver.find_element_by_id("p1_Button"+str(type)).click()
            time.sleep(1)

            # 勾选承诺
            promise = driver.find_element_by_id("p1_ChengNuo-inputEl-icon")
            promise.click()
            time.sleep(0.5)

            # 填报体温
            temperature = driver.find_element_by_id("p1_TiWen-inputEl")
            store = ["36.7","36.8","36.9","37","37.1"]
            i = random.randint(0,4)
            choose = store[i]
            temperature.clear()
            temperature.send_keys(choose)
            time.sleep(0.5)

            # 当天是否在校：
            driver.find_element_by_id("fineui_6-inputEl-icon").click()
            time.sleep(0.5)

            # 过去14天是否在中高风险地区逗留
            driver.find_element_by_id("fineui_11-inputEl-icon").click()
            time.sleep(0.5)

            # 上海同住人员是否有近14天来自中高风险地区的人
            driver.find_element_by_id("fineui_13-inputEl-icon").click()
            time.sleep(0.5)

            # 具体地址
            address = driver.find_element_by_id("p1_XiangXDZ-inputEl")
            address.clear()
            address.send_keys("新世纪大学村")
            time.sleep(0.5)

            # 中高风险地区逗留：
            driver.find_element_by_id("fineui_11-inputEl-icon").click()
            time.sleep(0.5)

            # 上海同住人员是否有12月06日至12月20日来自中高风险地区
            driver.find_element_by_id("fineui_13-inputEl-icon").click()
            time.sleep(0.5)

            # 12月06日至12月20日是否与来自中高风险地区发热人员密切接触
            driver.find_element_by_id("fineui_17-inputEl-icon").click()
            time.sleep(0.5)

            # 12月06日至12月20日是否乘坐公共交通途径中高风险地区
            driver.find_element_by_id("fineui_19-inputEl-icon").click()
            time.sleep(0.5)

            # 当天是否隔离
            driver.find_element_by_id("fineui_21-inputEl-icon").click()
            time.sleep(0.5)

            # 当天随身码
            driver.find_element_by_id("fineui_26-inputEl-icon").click()
            time.sleep(0.5)

            # 提交
            submit_res = driver.find_element_by_id("p1_ctl00_btnSubmit")
            submit_res.click()
            time.sleep(2)

            driver.find_element_by_id("fineui_32").click()
            print(time.ctime())
            time.sleep(5)
            # print("成功提交")

        # 网络连接超时或者网址错误
        except TimeoutException:
            msg = "base_url error OR timeout"
            userArr = self.warn_msg.get(msg, [])
            userArr.append(username)
            self.warn_msg[msg] = userArr
            errorFlag = False
            print(self.warn_msg)

        #找不到对应元素
        except Exception as msg:
            msg = str(msg)
            userArr = self.warn_msg.get(msg,[])
            userArr.append(username)
            self.warn_msg[msg] = userArr
            errorFlag = False
            print(self.warn_msg)
        else:
            errorFlag = True
        finally:
            driver.quit()
            return errorFlag


    def readUserGroupInfo(self, file="userInfo.json"):
        """
        read UserGroupInfo from file;
        return a dict object
        """
        with open(file, mode="r", encoding="utf-8") as userFile:
            userList = json.load(userFile)["userList"]
        return userList

    def run(self,type):
        self.__init__()
        userList = self.readUserGroupInfo()
        for user in userList:
            print("获取用户", user["username"])
            print("填报...")
            errorFlag = self.auto_report(user["username"], user["password"], type)
            print("写日志...\n")
            self.writeLog(user["username"], type, errorFlag)
        if self.warn_msg != {}:
            self.writeError(type)

    def writeLog(self, username, type,errorFlag):
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
    sp.run(1)