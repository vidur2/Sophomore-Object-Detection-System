import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
timeout = 1
def getDistance():
        GPIO.setup(11, GPIO.OUT)
        #cleanup output
        GPIO.output(11, 0)

        time.sleep(timeout)

        #send signal
        GPIO.output(11, 1)

        time.sleep(timeout)

        GPIO.output(11, 0)

        GPIO.setup(11, GPIO.IN)
            
        goodread=True
        watchtime=time.time()
        while GPIO.input(11)==0 and goodread:
                starttime=time.time()
                if (starttime-watchtime > timeout):
                        goodread=False

        if goodread:
                watchtime=time.time()
                while GPIO.input(11)==1 and goodread:
                        endtime=time.time()
                        if (endtime-watchtime > timeout):
                                goodread=False
            
        if goodread:
                duration=endtime-starttime
                distance=duration*34000/2
                return distance
def buzzer():
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(7, GPIO.OUT)
        GPIO.output(7, GPIO.HIGH)
        time.sleep(0.0005)
        GPIO.output(7, GPIO.LOW)  
