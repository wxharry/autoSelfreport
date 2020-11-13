#!/usr/bin/python3
# coding=UTF-8
from selenium import webdriver
import time
import random
import json
from selenium.webdriver.chrome.options import Options

class SelfReport(object):

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(executable_path=r'./chromedriver', chrome_options=chrome_options)
#         self.driver = webdriver.Chrome()
        with open('userInfo.json', mode="r", encoding="utf-8") as userFile:
            self.userInfo = json.load(userFile)
        self.user = self.userInfo["userList"]

    def auto_report(self,user,type):
        file_handle = open('log.txt', mode='a',encoding='utf-8')
        driver = self.driver
        driver.get('https://selfreport.shu.edu.cn/Default.aspx')
        print("="*100)
        file_handle.write('\n')
        file_handle.write('='*100)
        file_handle.write('\n')
        print("已进入填报网站")
        file_handle.write(time.ctime())
        file_handle.write('\n')
        username = driver.find_element_by_id("username")
        username.send_keys(user["username"])
        password = driver.find_element_by_id("password")
        password.send_keys(user["password"])
        print("自动填入账号密码完成")
        submit = driver.find_element_by_id("submit")
        submit.click()
        print("进入每日一报网站")
        
        driver.find_element_by_id("lnkReport").click()
        time.sleep(1)
        
        driver.find_element_by_id(("p1_Button"+str(type))).click()
        time.sleep(1)
        
        promise = driver.find_element_by_id("p1_ChengNuo-inputEl-icon")
        promise.click()
        print("勾选承诺完成")
        time.sleep(1)

        temperature = driver.find_element_by_id("p1_TiWen-inputEl")
        store = ["36.8","36.9","37","37.1","37.2"]
        i = random.randint(0,4)
        choose = store[i]
        temperature.send_keys(choose)
        print("填报体温完成")
        time.sleep(1)

        healthCode = driver.find_element_by_id("fineui_7-inputEl-icon")
        healthCode.click()
        print("勾选绿色随申码")
        time.sleep(1)

#         meal = driver.find_element_by_id("fineui_9-inputEl-icon")
#         meal.click()
#         print("勾选午餐")
#         time.sleep(1)
        
        submit_res = driver.find_element_by_id("p1_ctl00_btnSubmit")
        submit_res.click()
        time.sleep(1)
        print("成功提交")
        
#         driver.find_elements_by_css_selector(".f-btn.f-noselect.f-state-default.f-corner-all"
#                                                     ".f-btn-normal.f-btn-icon-no.f-cmp.f-widget"
#                                                     ".f-toolbar-item")[3].click()
        driver.find_element_by_id("fineui_14").click()
        print(time.ctime())
        time.sleep(1)
        driver.close()
        print("每日一报已完成")
        print("="*100)
        file_handle.write('体温为'+choose+'度\n')
        file_handle.write('已完成每日一报自动填写\n')
        file_handle.write('='*100)
        file_handle.write('\n')

        file_handle.close()

    def run(self,type):
        for tmp in self.user:
            self.auto_report(tmp,type)

if __name__ == '__main__':
    sp = SelfReport()
    sp.run()