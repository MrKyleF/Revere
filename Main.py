



import threading
from Scanner import Scanner


if __name__ == '__main__':
    scanner_1 = Scanner("https://broadcastify.cdnstream1.com/32994", "FI_ISLANDWIDE", "Fire Island Islandwide Repeater Alert")
    scanner_2 = Scanner("https://broadcastify.cdnstream1.com/33044", "FI_Ocean_Beach", "Ocean Beach Fire Department Primary")
    #scanner_3 = Scanner("https://broadcastify.cdnstream1.com/38399", "FI_Coast_Guard", "United States Coast Guard Fire Island")
    thread1 = threading.Thread(target=scanner_1.run)
    thread2 = threading.Thread(target=scanner_2.run)
    #thread3 = threading.Thread(target=scanner_3.run)
    thread1.start()
    thread2.start()
    #thread3.start()
    thread1.join()
    thread2.join()
    #thread3.join()