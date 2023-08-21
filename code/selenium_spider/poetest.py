#作者：王屿轩 Eason Wang
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests
import time
import re
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import os
import shutil

#设置Chrome参数

options = Options()
#options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging']) # 防止打印一些无用的日志
options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
#option.add_argument('headless')  #不显示浏览器
browser = webdriver.Chrome(executable_path ='./chromedriver.exe',options=options)

print(browser.title)


browser.set_page_load_timeout(10)
url = "https://poe.com/chat/2i3kbw5mf6a75d0nnyj"
browser.get(url)
while True:
    try:
        browser.get(url)
    except TimeoutException:
        print('Timeout')
        browser.execute_script('window.stop()')
        continue
    time.sleep(2)
    break

while True:
    q=input("Human:")
    if(q=='!quit'):
        break
    question=browser.find_element_by_xpath("//*[@id='__next']/div[1]/main/div/div/div/footer/div/div/div[1]/textarea")
    question.send_keys(q)
    sendbutton=browser.find_element_by_xpath("//*[@id='__next']/div[1]/main/div/div/div/footer/div/div/button[2]")
    sendbutton.click()
    last=''
    samecount=1
    while True:
        botresponse=""
        responselist=browser.find_element_by_xpath("//*[@id='__next']//div[1]/main/div/div/div/div[2]")
        qablocks=responselist.find_elements(By.XPATH, "./div")
        qablock=qablocks[len(qablocks)-1]
        botresponses=qablock.find_elements(By.XPATH,"./div[2]/div[2]/div[2]/div/div[1]/div/div/p")
        #print(botresponses[0].get_attribute("innerHTML"))
        for resstruct in botresponses:
            botresponse=botresponse+str(resstruct.get_attribute("innerHTML"))
        #print(botresponse)
        if botresponse==last:
            samecount+=1
        else:
            samecount=0
        if samecount>=5:
            print('bot:'+botresponse)
            break
        last=botresponse
        time.sleep(0.5)




#//*[@id="__next"]/div[1]/main/div/div/div/div[2]/div[4]/div[2]/div[2]/div[2]/div/div[1]/div/div/p
#//*[@id="__next"]/div[1]/main/div/div/div/div[2]/div[3]/div[2]/div[2]/div[2]/div/div[1]/div/div/p
#//*[@id="__next"]/div[1]/main/div/div/div/div[2]/div[6]/div[2]/div[2]/div[2]/div/div[1]/div/div/p

#chrome --remote-debugging-port=9527 --user-data-dir="E:\downloads\poeapi\poe-api-main\examples\test"