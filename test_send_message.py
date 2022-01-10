from linebot import *
from linebot.models import *
from datetime import datetime, date, timedelta
from get_zoom_link import Zoom_link
import os
from time import sleep
from __pycache__ import extra_byte

class Send_Message:
    link_dict = {'homeroom':'https://cudplus.onsmart.school/lms/courseHome?course=5160 \n zoom link: {zoom_link}',
            'scout':'https://cudplus.onsmart.school/lms/courseHome?course=5153 \n zoom link: {zoom_link}',
            'history':'https://cudplus.onsmart.school/lms/courseHome?course=5139 \n zoom link: {zoom_link}',
            'science':'https://cudplus.onsmart.school/lms/courseHome?course=5118 \n zoom link: {zoom_link}',
            'social':'https://cudplus.onsmart.school/lms/courseHome?course=5132 \n zoom link: {zoom_link}',
            'art and craft':'https://cudplus.onsmart.school/lms/courseHome?course=5192 \n zoom link: {zoom_link}',
            'guide':'https://cudplus.onsmart.school/lms/courseHome?course=5146 \n zoom link: {zoom_link}',
            'Physical Education':'https://cudplus.onsmart.school/lms/courseHome?course=5178 \n zoom link: {zoom_link}',
            'music':'music -> https://cudplus.onsmart.school/lms/courseHome?course=5226 \n zoom link: {zoom_link} \n dance class -> https://cudplus.onsmart.school/lms/courseHome?course=5227',
            'Health Education':'https://cudplus.onsmart.school/lms/courseHome?course=5167 \n zoom link: {zoom_link}',
            'design and technology':'https://cudplus.onsmart.school/lms/courseHome?course=5125 \n zoom link: {zoom_link}',
            'math':'https://cudplus.onsmart.school/lms/courseHome?course=5102 \n zoom link: {zoom_link}',
            'thai':'https://cudplus.onsmart.school/lms/courseHome?course=5110 \n zoom link: {zoom_link}',
            'art':'https://cudplus.onsmart.school/lms/courseHome?course=5224 \n zoom link: {zoom_link}',
            'english':'for high ab: https://cudplus.onsmart.school/lms/courseHome?course=5204 \n zoom link: {zoom_link}',
            'english_no_high_ab':'Please submit information for link. Usually no high ab class here. {zoom_link}',
            'selective class':'for english skills selective: https://cudplus.onsmart.school/lms/courseHome?course=5274 \n zoom link: {zoom_link} \n else: please get from your own cudplus page \n',
            'club':'click your own class'}
    def __init__(self) -> None:
        self.line_bot_api = LineBotApi(extra_byte.lineapi)
        handler = WebhookHandler(extra_byte.webhookhandler)
    
    def push_message(self,text):
        self.line_bot_api.push_message(extra_byte.my_user_id, messages=TextSendMessage(text=text))

    def message_logic(self, i, e, get_lesson,get_time):
        lesson = get_lesson.get_lesson(i)
        if lesson != '':
            res = get_time.get_time(int(e[:2]),int(e[-2:])-5)
            print(e)
            if res == 'pass':
                return
            elif lesson == 'english_no_high_ab':
                zl = ''
            elif lesson == 'math':
                zl='https://chula.zoom.us/j/95897429693?pwd=V0pyWmhKZlF6Q2VsTE9pbTBTWGE2QT09#success'
            elif lesson == 'feedback':
                self.push_message(text='It\'s the end of the week! Please give feedback and suggestion at https://forms.gle/XEqSriTfEPSc2kTA9')
                return
            else:
                zl = get_lesson.get_zoom_link(lesson)
            link = self.link_dict[lesson]
            print(f'please join {lesson} class at -> {link.format(zoom_link = zl)} \n If there is a bug, please report it via https://forms.gle/1tGx7qNBDMCDWDeAA \n If you like to give some information especially on your english and selective class, please do so at https://forms.gle/HHWt9SsRWvqkvnqA8')
            self.push_message(text=f'please join {lesson} class at -> {link.format(zoom_link = zl)} \n If there is a bug, please report it via https://forms.gle/1tGx7qNBDMCDWDeAA \n If you like to give some information especially on your english and selective class, please do so at https://forms.gle/HHWt9SsRWvqkvnqA8')


class Get_lesson:
    lesson_list = [[['','english_no_high_ab','thai','','selective class','selective class','science','',''],
                ['','math','','Physical Education','selective class','selective class','','science',''],
                ['homeroom','thai','science','','english','','history','math',''],
                ['','social','english','art and craft','art','math','selective class','selective class',''],
                ['','social','selective class','selective class','design and technology','','','thai','feedback'],[],[]],
                [['homeroom','english_no_high_ab','thai','','selective class','selective class','science','Health Education',''],
                ['','math','guide','','selective class','selective class','','science',''],
                ['','','science','','english','scout','history','math',''],
                ['','social','english','','','math','selective class','selective class',''],
                ['','social','selective class','selective class','design and technology','','music','thai','feedback'],[],[]]]
    def __init__(self) -> None:
        self.day = int(datetime.now().weekday())
        self.week = self.get_week()

    def get_weekday_of_the_first_day_of_the_month(self):
        month = datetime.now().month
        year = datetime.now().year
        return date(year,month,1).weekday()

    def get_week(self):
        offset = self.get_weekday_of_the_first_day_of_the_month()
        day = datetime.now().day
        week1 = (day+offset)//7+1
        print(f'offset = {offset}, day = {day}, week1 = {week1}')
        if week1%2 == 0:
            #even week (a)
            return 0
        else:
            #odd week (b)
            return 1

    def get_lesson(self,i):
        return self.lesson_list[self.week][self.day][i]

    def get_zoom_link(self,lesson):
        z = Zoom_link(lesson)
        z.get_to_meetings()
        a = z.click_meeting()
        if a != 'quit':
            return z.get_link()

class Get_time:
    def __init__(self) -> None:
        pass


    def get_time_now(self):
        now = datetime.now()
        if "GOOGLE_CHROME_BIN" in os.environ:
            return timedelta(hours=now.hour, minutes=now.minute) + timedelta(hours=7)
        return timedelta(hours=now.hour, minutes=now.minute)

    def get_time(self,h, m):
        return True
        # pass

send_message = Send_Message()
get_lesson = Get_lesson()
get_time = Get_time()
for i,e in enumerate(['08:00','08:30','09:20','10:20','12:00','12:50','13:50','14:40','15:30']):
    send_message.message_logic(i, e, get_lesson, get_time)

