import atexit
import os
import random
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import libs.GetLatestChromedriver as chromedriver

data = {'id' : 'your id',
        'pwd' : 'your pwd'}

card_num = "1234-0000-1234-0000"
# card_num = "0000-0000-0000-0000"
card_month = "0"
card_year = "2000"
# the fist two digits of the pwd of your card
card_pwd = "00"
# the first 6 digits from your birthday date
my_birth = "881214"

driver_path = chromedriver.get_path()
driver = webdriver.Chrome(executable_path = driver_path)
driver.get('http://www.letskorail.com/korail/com/login.do')
driver.implicitly_wait(10)

# logging in
driver.find_element_by_css_selector('#txtMember').send_keys(data['id'])
driver.find_element_by_css_selector('#txtPwd').send_keys(data['pwd'])
driver.find_element_by_css_selector('.btn_login').click()

driver.get('http://www.letskorail.com/ebizprd/EbizPrdTicketpr21100W_pr21110.do')
driver.implicitly_wait(10)

# select departure
depart = input("출발지 \n"
               "1. 서울\n"
               "2. 부산\n")
while True:
    if depart == "1" or depart == "서울":
        depart = 1
        print("서울 → 부산")
        break
    elif depart == "2" or depart == "부산":
        depart = 2
        print("부산 → 서울")
        break
    else:
        print("숫자 또는 지명을 넣어주십시오")

# input departure
driver.find_element_by_css_selector('#start').clear()
driver.find_element_by_css_selector('#get').clear()
driver.find_element_by_css_selector('#start').send_keys("서울")
driver.find_element_by_css_selector('#get').send_keys("부산")

# select date
print("출발 날짜 입력 (출발 날짜는 오늘로부터 30일 이내로만 가능)")
month = input("月 : ")
date = input("日 : ")

# input month
month_op = driver.find_elements_by_css_selector('#s_month option')
for i in month_op :
    if i.text == month :
        i.click()

# input date
day_op =  driver.find_elements_by_css_selector('#s_day option')
for i in day_op :
    if i.text == date :
        i.click()

# select time
what_time = input("출발 시간 입력(00 ~ 23) : ")
hour_op = driver.find_elements_by_css_selector('#s_hour option')
for i in hour_op :
    if i.get_attribute('value') == what_time :
        i.click()

# select people
people = input("인원 수 : ")
people_op = driver.find_elements_by_css_selector('#peop01 option')
for i in people_op :
    if i.get_attribute('value') == people:
        i.click()

# submit
driver.find_element_by_css_selector('.btn_inq').click()
driver.implicitly_wait(10)

got_ticket = False
idx = 0
how_many_next = 0

while not got_ticket :
    try :
        # make a reservation
        got_ticket = False
        tickets = driver.find_elements_by_css_selector('#tableResult tbody tr')
        for i in tickets :
            print(idx, ", " , end = "")
            idx += 1
            normal_seat = i.find_elements_by_css_selector('td')[5]
            isAvailable = normal_seat.find_element_by_css_selector('img').get_attribute('alt')
            if isAvailable == '예약하기' :
                normal_seat.find_element_by_css_selector('img').click()
                got_ticket = True
                print("GOT IT")
                break
        if got_ticket == True :
            break
        print('?')
        next_btn = driver.find_element_by_css_selector('table.btn img')
        if next_btn.get_attribute('alt') == "다음" :
            next_btn.click()
            how_many_next += 1
            print("next")
            time.sleep(random.randint(1, 3))
        else :
            while how_many_next != 0 :
                if next_btn.get_attribute('alt') == "이전" :
                    next_btn.click()
                    print("previous")
                    time.sleep(random.randint(1, 3))
                    how_many_next -= 1
    except Exception as e :
        pass

while True :
    try :
        driver.find_element_by_css_selector('body').send_keys(Keys.ENTER)
        driver.find_element_by_css_selector('body').send_keys(Keys.ENTER)
        break
    except Exception as e :
        pass

driver.find_element_by_css_selector('#btn_next').click()

temp = driver.find_elements_by_css_selector('#Div_Card tbody.lef tr')[1].find_elements_by_css_selector('input')

card_num = card_num.split('-')

for n, i in enumerate(temp) :
    i.send_keys(card_num[n])

temp = driver.find_elements_by_css_selector('#month option')
for i in temp :
    if i.text == card_month :
        i.click()

temp = driver.find_elements_by_css_selector('#year option')
for i in temp :
    if i.text == card_year:
        i.click()

temp = driver.find_elements_by_css_selector('#Div_Card tbody.lef tr')[4].find_element_by_css_selector('input')
temp.send_keys(card_pwd)

temp = driver.find_elements_by_css_selector('#Div_Card tbody.lef tr')[5].find_element_by_css_selector('input')
temp.send_keys(my_birth)

driver.find_element_by_css_selector('#fnIssuing').click()

@atexit.register
def my_exit():
    os.system('taskkill /f /im chromedriver.exe')