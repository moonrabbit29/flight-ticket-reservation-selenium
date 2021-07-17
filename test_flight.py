from selenium import webdriver
import string
import time
from selenium.webdriver.common import keys
from selenium.webdriver.common.keys import Keys
import random
import calendar
from datetime import datetime 
from selenium.webdriver.common.action_chains import ActionChains
import pytest
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
class TestFlight:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-notifications")
    date_depature = ''
    month_depature =''
    dewasa=''
    cabin_class = ['Ekonomi','Premium','Bisnis','First']
    cabin=''
    totalPassenger=''
    totalOrdering = ''
    price = ''

    @classmethod
    def setup_class(self):
        self.driver = webdriver.Remote(
            command_executor="http://localhost:4444/wd/hub",
            desired_capabilities = {'browserName': 'chrome'},
            options=self.chrome_options)
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()

    def randomize_passenger(self):
        self.dewasa = random.randint(1,8)-1
        # self.anak = random.randint(1,8)-1

    def randomize_cabin_class(self):
        # self.cabin = random.randint(1,4) - 1
        self.cabin = 0

    def randomize_date_depature(self) :
        current_moth = datetime.today().month
        month_num = random.randint(current_moth,12)
        month_list = ['Januari','Febuari','Maret','April','Mei','Juni','Juli','Agustus','September',
            'Oktober','November','Desember']
        self.month_depature = month_list[month_num-1]
        day_range = calendar.monthrange(2021,month_num)[1]
        current_date = int(str(datetime.today()).split("-")[2].split(' ')[0])
        if(day_range>30):
            self.date_depature = random.randint(current_date,31)
        elif(day_range==30):
            self.date_depature = random.randint(current_date,30)
        elif(day_range<30):
            self.date_depature = random.randint(current_date,day_range)

    def randomize_depature_time_and_transit(self):
        pass
    
    def check_passenger(self,passenger,passengerBox):
        total_passenger = 0
        for i in passenger:
            total_passenger += int(i.find_element_by_tag_name("span").get_attribute("innerHTML"))
        self.babyPassenger = int(passenger[2].find_element_by_tag_name("span").get_attribute("innerHTML"))
        self.totalPassenger = total_passenger
        passengerBoxValue = passengerBox.get_attribute("value").split(" ")
        assert total_passenger == int(passengerBoxValue[0]), "total passengers seleceted not equal to the summary box"
        assert self.cabin_class[self.cabin] == passengerBoxValue[2],"cabin class seleceted not equal to the summary box"

    def check_exists_by_className(self,classname):
        try:
            DUP_popup = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 
                classname)))
        except TimeoutException:
            return False
        return True
    
    def set_user_checkout_data(self):
        driver = self.driver
        title_dropdown = driver.find_element_by_class_name("contact-person-dropdown")
        title_dropdown.click()
        title_dropdown_value = title_dropdown.find_elements_by_class_name("list-data")
        i = random.randint(0,2)
        title_dropdown_value[i].click()
        name_box = driver.find_element_by_class_name("contact-name")
        name_input = name_box.find_element_by_class_name("input-list-autocomplete")
        name_input.send_keys("Web testing")
        driver.find_element_by_name("cp-email").send_keys("webtesting@mail.com")
        driver.find_element_by_name("cp-phone").send_keys("0812345678910")
        same_as_pemesan = driver.find_element_by_name("cp-detail-switch")
        ActionChains(driver).move_to_element(same_as_pemesan).click(same_as_pemesan).perform()

        passenger_box = driver.find_elements_by_class_name("person-with-passport-panel")
        nationality_dropdown_exist= False
        if(self.check_exists_by_className("tix-core-country-dropdown")):
            nationality_dropdown_exist = True
            nationality_dropdown =passenger_box[0].find_element_by_class_name("tix-core-country-dropdown")
            select_nationality = nationality_dropdown.find_element_by_tag_name("input")
            nationality_dropdown.click()
            select_nationality.click()
            select_nationality.send_keys("indonesia")
            select_nationality.send_keys(Keys.ENTER)
            time.sleep(3)

        for i in range(self.totalPassenger-1) : 
            row = passenger_box[i+1].find_element_by_class_name("row")
            print(" row : {}".format(row))
            title_dropdown = passenger_box[i+1].find_element_by_class_name("input-flight-dropdown")
            ActionChains(driver).move_to_element(title_dropdown).click(title_dropdown).perform()
            title_dropdown.click()
            print("{}".format(title_dropdown))
               
            title_dropdown_value = row.find_elements_by_class_name("list-data")
            print(title_dropdown_value)
            try:
                x = random.randint(0,2)
                title_dropdown_value[x].click()
            except:
                title_dropdown_value[0].click()
            random_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(2))
            passenger_box[i+1].find_element_by_class_name("input-list-autocomplete").send_keys("testing {}".format(random_name))
            if(nationality_dropdown_exist):
                nationality_dropdown =passenger_box[i+1].find_element_by_class_name("tix-core-country-dropdown")
                select_nationality = nationality_dropdown.find_element_by_tag_name("input")
                nationality_dropdown.click()
                select_nationality.click()
                select_nationality.send_keys("indonesia")
                select_nationality.send_keys(Keys.ENTER)
        #LANJUTKAN KE PEMBAYARAN
        button_pay = driver.find_element_by_class_name("v3-btn__yellow")
        ActionChains(driver).move_to_element(button_pay).click(button_pay).perform()
        
    def test_one_way_1(self) : 
        driver = self.driver
        driver.get("https://www.tiket.com/")
        url = '/pesawat'
        searchPesawat = driver.find_element_by_xpath('//a[@href="'+url+'"]')
        ActionChains(driver).move_to_element(searchPesawat).click(searchPesawat).perform()
        sekalijalan = driver.find_element_by_id('oneway')
        driver.execute_script("arguments[0].click();", sekalijalan)
        depature_box = driver.find_element_by_xpath("//input[@placeholder='Kota atau bandara']")
        arrival_box = driver.find_element_by_xpath("//input[@placeholder='Mau ke mana?']")
        ActionChains(driver).move_to_element(depature_box).perform()
        depature_box.send_keys('Semarang')
        depature_box.send_keys(Keys.ENTER)
        arrival_box.send_keys('Surabaya')
        arrival_box.send_keys(Keys.ENTER)
        depature_date = driver.find_elements_by_class_name("input-datepicker")
        depature_date[0].click()
        self.randomize_date_depature()
        flag = 1 
        date_picker_box = driver.find_element_by_class_name("widget-datepicker-content")
        print(date_picker_box)
        while(flag):
            parent_visible_date = driver.find_elements_by_class_name("CalendarMonth_caption")[:2]
            for i in parent_visible_date : 
                try : 
                    date_value = i.find_element_by_tag_name("strong").get_attribute('innerHTML')
                    month = date_value.split(' ')[0]
                    print(self.month_depature)
                    if(month == self.month_depature) :
                        flag = 0
                        calendar_table = driver.find_element_by_class_name("CalendarMonth_table")
                        date_pickers = calendar_table.find_elements_by_class_name("widget-date-picker-day")
                        for date in date_pickers :
                            date_picker  = date.get_attribute('innerHTML')
                            if(date_picker== str(self.date_depature) ) :
                                select_date = date.find_element_by_xpath(".//ancestor::td")
                                ActionChains(driver).move_to_element(select_date).click(select_date).perform()
                except: continue

            if(flag==1):
                next_month = date_picker_box.find_element_by_class_name("tix-chevron-right")
                next_month.click()

        self.randomize_passenger()
        self.randomize_cabin_class()


        input_passanger = driver.find_element_by_class_name("input-passengerclass")
        input_passanger.click()
        passenger_box = driver.find_element_by_class_name("col-passenger")
        passenger_selection = passenger_box.find_elements_by_tag_name("li")
        for i in range(self.dewasa) : 
            passenger_selection[0].find_element_by_class_name("icon-plus").click()
        # for i in range(self.anak) :
        #     passenger_selection[1].find_element_by_class_name("icon-plus").click()

        cabin = driver.find_element_by_class_name("col-cabin")
        cabin_class = cabin.find_elements_by_tag_name("li")
        cabin_class[self.cabin].click()

        #check if selected seat and cabin class is correct
        self.check_passenger(passenger_selection,input_passanger)
        driver.find_element_by_class_name("btn-done").click()
        driver.find_element_by_class_name("v3-btn__yellow").click()

        if(self.check_exists_by_className("v3-btn__blue")):
            button = driver.find_element_by_class_name("v3-btn__blue")
            button.click()
        if(self.check_exists_by_className("ab-message-button")):
            button = driver.find_elements_by_class_name("ab-message-button")[1]
            button.click()

        if(self.check_exists_by_className("btn-book-now")):
            maskapai_penerbangan = driver.find_elements_by_class_name("btn-book-now") 
            pick_random_flight = random.randint(1,len(maskapai_penerbangan)-1)
            maskapai_penerbangan[pick_random_flight].click()

        self.set_user_checkout_data()
        driver.find_element_by_class_name("v3-btn__blue").click()
        driver.find_element_by_xpath("//*[text()[contains(., 'BNI Virtual Account')]]").click()
        time.sleep(20)

    # @classmethod
    # def teardown_class(self):
    #     self.driver.quit()
