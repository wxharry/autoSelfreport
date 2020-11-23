#!/usr/bin/python3
# coding=UTF-8
from selenium import webdriver
import time
import random
from selenium.webdriver.chrome.options import Options
import json

class SelfReport(object):

    def __init__(self):
        with open('userInfo.json', mode="r", encoding="utf-8") as userFile:
            self.userList = json.load(userFile)["userList"]

    def auto_report(self, username, password, type):
        # chrome_options = Options()
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--disable-dev-shm-usage')
        # chrome_options.add_argument('--headless')
        # self.driver = webdriver.Chrome(executable_path=r'./chromedriver', chrome_options=chrome_options)
        self.driver = webdriver.Chrome(executable_path=r'./chromedriver.exe')

        # print("="*100)
        # print("已进入填报网站")


        # 脚本主体
        # 请求网页
        driver = self.driver
        driver.get('https://selfreport.shu.edu.cn/Default.aspx')

        # 填写用户名和密码
        driver.find_element_by_id("username").send_keys(username)
        driver.find_element_by_id("password").send_keys(password)
        # print("自动填入账号密码完成")

        # 登陆
        driver.find_element_by_id("submit").click()
        # print("进入每日一报网站")
        # 进入每日填报
        driver.find_element_by_id("lnkReport").click()
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
        store = ["36.8","36.9","37","37.1","37.2"]
        i = random.randint(0,4)
        choose = store[i]
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
        driver.find_element_by_id("p1_XiangXDZ-inputEl").clear()
        driver.find_element_by_id("p1_XiangXDZ-inputEl").send_keys("新世纪大学村")
        time.sleep(0.5)

        # 当天是否隔离：
        driver.find_element_by_id("fineui_15-inputEl-icon").click()
        time.sleep(0.5)

        # 11月09日至11月23日是否与来自中高风险地区发热人员密切接触
        driver.find_element_by_id("fineui_21-inputEl-icon").click()
        time.sleep(0.5)

        # 11月09日至11月23日是否乘坐公共交通途径中高风险地区
        driver.find_element_by_id("fineui_23-inputEl-icon").click()
        time.sleep(0.5)

        # 当天随身码
        driver.find_element_by_id("fineui_7-inputEl-icon").click()
        time.sleep(0.5)

        # 提交        
        submit_res = driver.find_element_by_id("p1_ctl00_btnSubmit")
        submit_res.click()
        time.sleep(2)

#         driver.find_elements_by_css_selector(".f-btn.f-noselect.f-state-default.f-corner-all"
#                                                     ".f-btn-normal.f-btn-icon-no.f-cmp.f-widget"
#                                                     ".f-toolbar-item")[3].click()
        driver.find_element_by_id("fineui_32").click()
        print(time.ctime())
        time.sleep(5)
        # print("成功提交")

        driver.close()
        # print("每日一报已完成")

        # 填写日志
        # print("="*100)


    def run(self,type):
        for user in self.userList:
            self.auto_report(user["username"], user["password"], type)
            self.writeLog(user["username"], type)


    def writeLog(self, username, type):
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
        if type == 1:
            file_handle.write('已完成晨报填写\n')
        elif type == 2:
            file_handle.write('已完成晚报填写\n')
        file_handle.write('='*100)
        file_handle.write('\n')
        file_handle.write(old)
        file_handle.close()

if __name__ == '__main__':
    sp = SelfReport()
    sp.run(2)