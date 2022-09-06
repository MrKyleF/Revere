#Kyle R Fogerty

#Global
MAX_FILE_INDEX = 50             #Index where files return back to zero count

#Stream
STREAM_BUFFER_SIZE = 2048       #Size of the buffer from stream
FAIL_THRESHOLD_STREAM = 5       #Number of times it will re-attempt after error

#Analyze
REQUIRED_RMS = 100              #Root mean square of audio signal loudness required to unmute
MAX_STEPS_FORWARD = 200         #Number of steps forward it will take for future audio
MINIMUM_DURATION = 1000         #Minimum duration required to have meaning
FAIL_THRESHOLD_ANALYZE = 50     

#Notifcation
FAIL_THRESHOLD_NOTIFICATION = 5 #Number of times it will re-attempt after error

#Mailing List
MAILING_LIST = {
    "KRF":{"Email":"kylefogerty@gmail.com",\
        "Phone":"9143305724",\
        "Carrier":"Verzion"}
}