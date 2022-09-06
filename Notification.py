#Kyle R Fogerty
from os.path import exists
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio

from datetime import datetime
from time import sleep
import pytz
import os
from Auth import LOGIN, PASSWORD
from Config import FAIL_THRESHOLD_NOTIFICATION, MAILING_LIST, MAX_FILE_INDEX

class Notification:
    def __init__(self, short_name: str, long_name: str):
        self.short_name: str = short_name
        self.long_name = long_name
        self.current_file_index_notification: int = 0
        self.port = 587
        self.smtp_server = "smtp.gmail.com"
        self.done = False
    
    def __sendEmail(self, path, receiver):
        message = MIMEMultipart()
        message["From"] = LOGIN
        message["To"] = receiver
        message["Subject"] = self.long_name #"F.I. Islandwide Repeater Alert"
        now = datetime.now(pytz.timezone('US/Eastern')) # current date and time
        body = "Alert recorded at " + now.strftime("%m/%d/%Y, %H:%M:%S") + " US/Eastern"
        message.attach(MIMEText(body, "plain"))
        # Open PDF file in binary mode
        with open(path, 'rb') as fp:
            img = MIMEAudio(fp.read(), _subtype="mp3")
            img.add_header('Content-Disposition', 'attachment', filename=self.short_name + "_" + str(self.current_file_index_notification) + ".mp3")
            message.attach(img)
        # send your email
        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.starttls()
            server.login(LOGIN, PASSWORD)
            server.sendmail(
                LOGIN, receiver, message.as_string()
            )

    
    def __run(self):
        try:
            while not self.done:
                path = "Feed_" + self.short_name + "/Notification/Clip_" + str(self.current_file_index_notification) + ".mp3"
                while not exists(path):
                    sleep(0.25)
                for receiver in MAILING_LIST:
                    self.__sendEmail(path, MAILING_LIST[receiver]['Email'])
                self.current_file_index_notification = (self.current_file_index_notification + 1) % MAX_FILE_INDEX
                os.remove(path)
            return True
        except KeyboardInterrupt:
            return True
        except:
            print("Error in Notfication.")
            return False  
    
    def run(self):
        for _ in range(FAIL_THRESHOLD_NOTIFICATION):
            if self.__run() == True:
                break
        self.done = True