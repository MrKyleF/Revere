#Kyle R Fogerty
from time import sleep
import requests
from os.path import exists
import os
from Config import FAIL_THRESHOLD_STREAM, MAX_FILE_INDEX, STREAM_BUFFER_SIZE

class Stream:
    def __init__(self, stream_url: str, short_name: str):
        self.stream_url: str = stream_url       #URL of stream CDN
        self.short_name: str = short_name       #Short name of stream
        self.current_file_index: int = 0        #Current index for saving files
        self.done = False                       #Completed 
    
    def __run(self):
        try:
            response = requests.get(self.stream_url, stream=True)
            for block in response.iter_content(STREAM_BUFFER_SIZE):
                path = "Feed_" + self.short_name + "/Processing/Clip_" + str(self.current_file_index) + ".mp3"
                with open(path, 'wb') as f:
                    f.write(block)
                self.current_file_index = (self.current_file_index + 1) % MAX_FILE_INDEX
            if self.done:
                return True
        except KeyboardInterrupt:
            feed_directory = "Feed_" + self.short_name
            processing_directory = feed_directory + "/Processing"
            if len(os.listdir(processing_directory)) > 0:
                for item in os.listdir(processing_directory):
                    os.remove(processing_directory + "/" + item)
            return True
        except:
            print("Error in stream.")
            return False      

    def __checkStreamFileFolder(self):
        #Feed Folder
        feed_directory = "Feed_" + self.short_name
        if not exists(feed_directory):
            os.mkdir(feed_directory)
        #Processing Folder
        processing_directory = feed_directory + "/Processing"
        if not exists(processing_directory):
            os.mkdir(processing_directory)
        else:
            if len(os.listdir(processing_directory)) > 0:
                for item in os.listdir(processing_directory):
                    os.remove(processing_directory + "/" + item)    
    
    def run(self):
        self.__checkStreamFileFolder()
        for _ in range(FAIL_THRESHOLD_STREAM):
            if self.__run() == True:
                break
            sleep(1)
        self.done = True