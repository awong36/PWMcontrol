import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO
from CommonFunction import timeCal
import time


class pinConfig(object):
    restTime = 8  #seconds
    timeout = 25 #seconds
    swTime = 6

    upDIR = "P9_15"
    downDIR = "P9_12"
    upperSW = "P9_25"
    lowerSW = "P9_28"

    pwmPIN = "P9_14"
    freq = 10000
    duty = 100

    def setPin(self):
        GPIO.setup(self.upDIR, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.downDIR, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.upperSW, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.lowerSW, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def moveUP(self):
        try:
            GPIO.add_event_detect(motor.upperSW, GPIO.RISING, bouncetime=1000)
        except RuntimeError:
            pass

        PWM.start(self.pwmPIN, self.duty, self.freq, 0)
        GPIO.output(self.upDIR, GPIO.HIGH)
        print "Moving motor UP"
        return 0, time.time()


    def moveDOWN(self):
        try:
            GPIO.add_event_detect(motor.lowerSW, GPIO.RISING, bouncetime=1000)
        except RuntimeError:
            pass

        PWM.start(self.pwmPIN, self.duty, self.freq, 0)
        GPIO.output(self.downDIR, GPIO.HIGH)
        status = 0
        print "Moving motor DOWN"
        return 1, time.time()


    def moveStop(self,channel):
        try:
            GPIO.remove_event_detect(channel)
        except RuntimeError:
            pass

        #PWM.start(self.pwmPIN, 0, self.freq, 0)
        GPIO.output(self.upDIR, GPIO.LOW)
        GPIO.output(self.downDIR, GPIO.LOW)
        print "Motor STOP...!!"
        return time.time()


    def timeoutStop(self):
        GPIO.output(self.upDIR, GPIO.LOW)
        GPIO.output(self.downDIR, GPIO.LOW)
        print "Motor STOP...!!"

    def eStop(self):
        PWM.start(self.pwmPIN, 0, self.freq, 0)
        GPIO.output(self.upDIR, GPIO.LOW)
        GPIO.output(self.downDIR, GPIO.LOW)

def myCallback(channel):
    motor.eStop()

def main():
    global status
    global motor
    status = -1  # up = 1, down = 0
    nextMove = -1
    startTime = 0
    sleepTimer = 1000
    motor = pinConfig()
    motor.setPin()

    if GPIO.input(motor.upperSW):  # if on upperSW move down
        print "@Upper switch..."
        nextMove, startTime = motor.moveDOWN()

    elif GPIO.input(motor.lowerSW):  # if on lowerSW move up
        print "@Lower switch..."
        nextMove, startTime = motor.moveUP()

    else:
        print "@Middle...no switch detected"
        nextMove, startTime = motor.moveUP()


    try:
        while True:
            #stop motor when upper switch trigger
            if GPIO.event_detected(motor.upperSW) and GPIO.input(motor.upperSW):
                sleepTimer = motor.moveStop(motor.upperSW)
                status = 1
                print "stop1"

            #timeout condition @ upperSW
            elif GPIO.input(motor.upperSW) and timeCal(startTime) > pinConfig.timeout:
                print "Motor @Upper Switch timeout..."
                sleepTimer = motor.moveStop(motor.upperSW)
                nextMove, startTime = motor.moveDOWN()
                status = 0

            #stop motor when lower switch trigger
            if GPIO.event_detected(motor.lowerSW) and GPIO.input(motor.lowerSW):
                sleepTimer = motor.moveStop(motor.lowerSW)
                status = 1
                print "stop2"

            #timeout condition @ lowerSW
            elif GPIO.input(motor.lowerSW) and timeCal(startTime) > pinConfig.timeout:
                print "Motor @Lower Switch timeout..."
                sleepTimer = motor.moveStop(motor.lowerSW)
                nextMove, startTime = motor.moveUP()
                status = 0

            # motor timeout without upperSW/lowerSW
            if nextMove == 0 and GPIO.input(motor.lowerSW):
                if timeCal(startTime) > pinConfig.swTime:
                    print "Motor timeout...no movement detected"
                    try:
                        sleepTimer = motor.moveStop(motor.upperSW)
                    except RuntimeError:
                        pass

                    print "stop3"
                    nextMove, startTime = motor.moveUP()
                    status = 0


            elif nextMove == 1 and GPIO.input(motor.upperSW):
                if timeCal(startTime) > pinConfig.swTime:
                    print "Motor timeout...no movement detected"
                    try:
                        sleepTimer = motor.moveStop(motor.lowerSW)
                    except RuntimeError:
                        pass

                    print "stop4"
                    nextMove, startTime = motor.moveDOWN()
                    status = 0

            # motor timeout without upperSW/lowerSW
            if timeCal(startTime) > pinConfig.timeout:
                print "Motor timeout...no switch detected"
                if nextMove == 0:
                    print "stop3"
                    sleepTimer = motor.moveStop(motor.upperSW)
                    print "rest3"
                    time.sleep(pinConfig.restTime)
                    nextMove, startTime = motor.moveDOWN()
                    status = 0

                elif nextMove == 1:
                    print "stop4"
                    sleepTimer = motor.moveStop(motor.lowerSW)
                    print "rest4"
                    time.sleep(pinConfig.restTime)
                    nextMove, startTime = motor.moveUP()
                    status = 0


            #switch direction after rest time lapse
            if nextMove == 0 and status == 1:
                if timeCal(sleepTimer) > pinConfig.restTime:
                    nextMove, startTime = motor.moveDOWN()
                    status = 0

            elif nextMove == 1 and status == 1:
                if timeCal(sleepTimer) > pinConfig.restTime:
                    nextMove, startTime = motor.moveUP()
                    status = 0


    except KeyboardInterrupt:
        motor.eStop()
        GPIO.cleanup()

    # optionally, you can set the frequency as well as the polarity from their defaults:
    # PWM.start("P9_14", 50, 1000, 1)
    # PWM.set_duty_cycle("P9_14", 25.5)
    # PWM.set_frequency("P9_14", 10)

if __name__ == "__main__":
    main()
