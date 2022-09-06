#Kyle R Fogerty


import threading
from time import sleep
from Analyze2 import Analyze
from Notification import Notification
from Stream import Stream


class Scanner:
    def __init__(self, url: str, short_name: str, long_name: str):
        self.stream = Stream(url, short_name)
        self.analyze = Analyze(short_name)
        self.notifcation = Notification(short_name, long_name)
    
    def __run(self):
        t1 = threading.Thread(target=self.stream.run)
        t2 = threading.Thread(target=self.analyze.run)
        t3 = threading.Thread(target=self.notifcation.run)
        t1.start()
        sleep(1)
        t2.start()
        sleep(1)
        t3.start()
        while self.stream.done == False and self.analyze.done == False and self.notifcation.done == False:
            pass
        self.stream.done = True
        self.analyze.done = True
        self.notifcation.done = True
        t1.join()
        t2.join()
        t3.join()
        return
    
    def run(self):
        while True:
            self.__run()
            sleep(2)
