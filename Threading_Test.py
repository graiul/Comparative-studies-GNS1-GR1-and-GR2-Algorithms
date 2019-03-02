import time
import threading
def loop1_10():
    for i in range(1, 11):
        time.sleep(1)
        print(i)

threading.Thread(target=loop1_10).start()