import atexit
import os
import random
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class korail:
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path = path)
        self.driver.get('http://www.letskorail.com/korail/com/login.do')
        self.driver.implicitly_wait(10)
        self.login()

    def login(self):
    # logging in
        self.driver.find_element_by_css_selector('#txtMember').send_keys(data['id'])
        self.driver.find_element_by_css_selector('#txtPwd').send_keys(data['pwd'])
        self.driver.find_element_by_css_selector('.btn_login').click()
        time.sleep(1)
        self.rsv(day,card_num,card)


    def rsv(self,day,card_num,card):
        self.driver.get('http://www.letskorail.com/ebizprd/EbizPrdTicketpr21100W_pr21110.do')
        self.driver.implicitly_wait(10)





        # input departure
        self.driver.find_element_by_css_selector('#start').clear()
        self.driver.find_element_by_css_selector('#get').clear()
        self.driver.find_element_by_css_selector('#start').send_keys("대전")
        self.driver.find_element_by_css_selector('#get').send_keys("울산(통도사)")


        # input month
        month_op = self.driver.find_elements_by_css_selector('#s_month option')
        for i in month_op :
            if i.text == day[0] :
                i.click()
        # day를 리스트
        # input date
        day_op =  self.driver.find_elements_by_css_selector('#s_day option')
        for i in day_op :
            if i.text == day[1]:
                i.click()

        # select time
        hour_op = self.driver.find_elements_by_css_selector('#s_hour option')
        for i in hour_op :
            if i.get_attribute('value') == day[2]:
                i.click()

        # select people
        # people = day[3]
        people_op = self.driver.find_elements_by_css_selector('#peop01 option')
        for i in people_op :
            if i.get_attribute('value') == day[3]:
                i.click()

        # submit
        self.driver.find_element_by_css_selector('.btn_inq').click()
        self.driver.implicitly_wait(10)

        got_ticket = False
        idx = 0
        how_many_next = 0

        while not got_ticket :
            try :
                # make a reservation
                got_ticket = False
                tickets = self.driver.find_elements_by_css_selector('#tableResult tbody tr')
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
                next_btn = self.driver.find_element_by_css_selector('table.btn img')
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
                self.driver.find_element_by_css_selector('body').send_keys(Keys.ENTER)
                self.driver.find_element_by_css_selector('body').send_keys(Keys.ENTER)
                break
            except Exception as e :
                pass

        self.driver.find_element_by_css_selector('#btn_next').click()

        temp = self.driver.find_elements_by_css_selector('#Div_Card tbody.lef tr')[1].find_elements_by_css_selector('input')

        card_num = card_num.split('-')

        for n, i in enumerate(temp) :
            i.send_keys(card_num[n])

        temp = self.driver.find_elements_by_css_selector('#month option')
        for i in temp :
            if i.text == card[0]:
                i.click()

        temp = self.driver.find_elements_by_css_selector('#year option')
        for i in temp :
            if i.text == card[1]:
                i.click()

        temp = self.driver.find_elements_by_css_selector('#Div_Card tbody.lef tr')[4].find_element_by_css_selector('input')
        temp.send_keys(card[2])

        temp = self.driver.find_elements_by_css_selector('#Div_Card tbody.lef tr')[5].find_element_by_css_selector('input')
        temp.send_keys(card[3])

        self.driver.find_element_by_css_selector('#fnIssuing').click()
        self.driver.find_element_by_css_selector('#tabSale3').click()
        #self.driver.find_element_by_css_selector('#btn_next').click()
        #self.driver.switch_to_frame(self.driver.find_element_by_xpath('//*[@id="mainframeSaleInfo"]'))
        #elem = self.driver.find_element_by_xpath('/html/body')

        # 현재 웹페이지에서 iframe이 몇개가 있는지 변수에 넣고 확인해 봅니다.
        iframes = self.driver.find_elements_by_tag_name('iframe')
        print('현재 페이지에 iframe은 %d개가 있습니다.' % len(iframes))
        self.driver.switch_to_frame(iframes[2])
        self.driver.find_elements_by_css_selector("input[type='radio'][title='예']")[0].click()
        self.driver.find_element_by_xpath('//*[@id="btn_next"]').click()
        self.driver.switch_to_default_content()



        @atexit.register
        def my_exit():
            os.system('taskkill /f /im chromedriver.exe')




# select departure
data = {'id' : 'id',
        'pwd' : 'password'}
day = ['9','6','15','1'] # month,day,time,people
card_num = "1234-0000-1234-0000"
card = ['1','2022','00','950411'] # valid_month, valid_year, the fist two digits of the pwd of your card, your birth
path = 'path here' # chromedriver path

K = korail()
