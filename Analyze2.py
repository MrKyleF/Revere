#Kyle R Fogerty
from time import sleep
from pydub import AudioSegment
from os.path import exists
import os
from Config import FAIL_THRESHOLD_ANALYZE, MAX_FILE_INDEX, MAX_STEPS_FORWARD, MINIMUM_DURATION, REQUIRED_RMS

class Analyze:
    def __init__(self, short_name: str):
        self.short_name: str = short_name
        self.current_file_index_stream: int = 0
        self.current_file_index_notification: int = 0
        self.start_index: int = 0
        self.current_step_forward: int = 0
        self.unmuted: bool = False
        self.current_audio: AudioSegment = None
        self.done: bool = False
    
    def __checkNotificationFileFolder(self):
        #Feed Folder
        feed_directory = "Feed_" + self.short_name
        if not exists(feed_directory):
            os.mkdir(feed_directory)
        #Processing Folder
        notifcation_directory = feed_directory + "/Notification"
        if not exists(notifcation_directory):
            os.mkdir(notifcation_directory)
        else:
            if len(os.listdir(notifcation_directory)) > 0:
                for item in os.listdir(notifcation_directory):
                    os.remove(notifcation_directory + "/" + item) 
                    
    def cleanAudioSegment(self, segment: AudioSegment):
        try:
            index = 0
            while (index + 1) < len(segment):
                if segment[index].rms < -10000000:
                    segment = segment[:index] + segment[index + 1:]
                else:
                    index += 1
            return segment
        except:
            print("Error cleaning sound")
            return None
    
    def __getSoundClip(self, retry_count = 0):
        try:
            path = "Feed_" + self.short_name + "/Processing/Clip_" + str(self.current_file_index_stream) + ".mp3"
            sound_clip: AudioSegment = AudioSegment.from_file(path)
            if len(sound_clip) > 0:
                return sound_clip
            else:
                return None
        except:
            if retry_count > 3:
                print("Error getting sound clip, giving up...")
                return None
            else:
                return self.__getSoundClip(retry_count+1)
    
    def __waitForClipToExist(self):
        path = "Feed_" + self.short_name + "/Processing/Clip_" + str(self.current_file_index_stream) + ".mp3"
        while not exists(path):
            sleep(0.25)
        return

    def __run(self, retry=False):
        while not self.done:
            self.__waitForClipToExist()
            #Get Sound
            sound_clip = self.__getSoundClip()
            #Clean Sound
            sound_clip = self.cleanAudioSegment(sound_clip) if sound_clip else sound_clip
            if sound_clip:
                index = 0
                self.start_index = 0
                for i in sound_clip:
                    if self.unmuted:
                        if i.rms < REQUIRED_RMS and self.current_step_forward > MAX_STEPS_FORWARD:
                            self.current_audio = (self.current_audio[:] + sound_clip[self.start_index:index-MAX_STEPS_FORWARD]) if self.current_audio != None else sound_clip[self.start_index:index-MAX_STEPS_FORWARD]
                            if len(self.current_audio) > MINIMUM_DURATION:
                                print("Trying to export")
                                save_path = "Feed_" + self.short_name + "/Notification/Clip_" + str(self.current_file_index_notification) + ".mp3"
                                self.current_audio.export(save_path, format="mp3")
                                print("Exported")
                                self.current_file_index_notification = (self.current_file_index_notification + 1) % MAX_FILE_INDEX
                            self.current_audio = None
                            self.current_step_forward = 0
                            self.unmuted = False
                        elif i.rms < REQUIRED_RMS:
                            self.current_step_forward += 1
                        else:
                            self.current_step_forward = 0
                    else:
                        if i.rms > REQUIRED_RMS:
                            self.start_index = index
                            self.unmuted = True
                    index += 1
                if self.unmuted:
                    self.current_audio = (self.current_audio + sound_clip[self.start_index:]) if self.current_audio != None else sound_clip[self.start_index:]
            os.remove("Feed_" + self.short_name + "/Processing/Clip_" + str(self.current_file_index_stream) + ".mp3")
            self.current_file_index_stream = (self.current_file_index_stream + 1) % MAX_FILE_INDEX
    
    def run(self):
        self.__checkNotificationFileFolder()
        for _ in range(FAIL_THRESHOLD_ANALYZE):
            if self.__run() == True:
                break
            sleep(1)
        self.done = True