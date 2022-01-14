from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import os
from __pycache__ import extra_byte



class Zoom_link:
    def __init__(self,subject):
        #4 digits code for the subjects
        subject_code_dict = link_dict = {'homeroom':'5160',
            'scout':'5153',
            'history':'5139',
            'science':'5118',
            'social':'5132',
            'art and craft':'5192',
            'guide':'5146',
            'Physical Education':'5178',
            'music':'5226',
            'Health Education':'5167',
            'design and technology':'5125',
            'math':'5102',
            'thai':'5110',
            'art':'5224',
            'english':'5204',
            'english skills selective':'5274',
            'club':'click your own class'}
        self.course_code = subject_code_dict[subject]
        
        if "GOOGLE_CHROME_BIN" in os.environ:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--no-sandbox")
            self.driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        else:
            options = webdriver.ChromeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            #create webdriver
            self.driver = webdriver.Chrome(ChromeDriverManager().install())
        #create action chain (to run chain of actions like move to element and click)
        self.actions = ActionChains(self.driver)

    def find_date(self):
        day_dict = {0:'จ',1:'อ',2:'พ',3:'พฤ',4:'ศ',5:'ส',6:'อา'}
        #return todays shorten weekday in thai (จ-อา) . date of to day (1-31) ex. จ.7
        return day_dict[datetime.datetime.today().weekday()] + '.' + str(datetime.datetime.today().day)

    def find_month(self):
        
        return datetime.datetime.today().month

    def wait_for_element_to_be_clickable(self,xpath):
        return WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath)))

    def get_to_meetings(self):
        self.driver.get("https://www.mycourseville.com/api/login")
        Username = self.driver.find_element_by_id("username")
        #make selenium to type username field
        Username.send_keys(extra_byte.username)
        password = self.driver.find_element_by_id("password")
        #make selenium to type password field
        password.send_keys(extra_byte.password)
        #click on submit
        submit = self.driver.find_element_by_id("cv-login-cvecologinbutton")
        submit.click()
        #click on cud+
        cudplus = self.driver.find_elements_by_class_name("cv-userhome-apptitle")
        cudplus[1].click()
        #click on courses
        courses = self.driver.find_elements_by_xpath('//a[contains(@href,"/curriculum/getJoinedCourses?type=other")]')
        courses[1].click()
        #click on subject
        subject = self.wait_for_element_to_be_clickable(f'//a[contains(@href,"/lms/courseHome?course={self.course_code}")]')
        self.actions.move_to_element(subject).click().perform()
        #click on all meetings
        all_meetings = self.wait_for_element_to_be_clickable(f'//a[contains(@href,"/lms/courseonlinemeetings/{self.course_code}/index")]')
        self.driver.execute_script("arguments[0].scrollIntoView();", all_meetings)
        self.driver.execute_script("arguments[0].click();", all_meetings) 
        sleep(2)
    

#find all the meeting links

    
    def click_meeting(self):
        month_dict = {'ม.ค.':1,
                    'ก.พ.':2,
                    'มี.ค.':3,
                    'เม.ย.':4,
                    'พ.ค.':5,
                    'มิ.ย.':6,
                    'ก.ค.':7,
                    'ส.ค.':8,
                    'ก.ย.':9,
                    'ต.ค.':10,
                    'พ.ย.':11,
                    'ธ.ค.':12}
        meeting = self.driver.find_elements_by_tag_name('a')
        this_month = self.find_month()
        months = self.driver.find_elements_by_class_name("ss-month.ss-color-1")
        meetings = self.driver.find_elements_by_class_name("ss-dow-date")
        today_date = self.find_date()
        # add is for 
        add = 0
        #loop on all of the dates of the meetings
        for i, element in enumerate(meetings):
            #if the date is today
            if month_dict[months[i].text] > this_month:
                add += 1
                continue
            try:
                date_in_text = int(element.text[-2:])
            except ValueError:
                date_in_text = int(element.text[-1:])
            if date_in_text > int(datetime.datetime.today().day):
                add += 1
                continue
            if element.text == today_date and month_dict[months[i].text] == this_month:
                #click that meeting link
                #Add more index for upcoming meetings
                meeting[25+i+add].click()
                break
            if len(meetings) - i == 1:
                self.driver.quit()
                return 'quit'

    def get_link(self):
        meeting_link = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'ml-2'))) 
        ml = meeting_link.get_attribute('href')
        self.driver.quit()
        return ml

