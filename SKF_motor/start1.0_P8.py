import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO
from CommonFunction import timeCal
import time


class pinConfig(object):
    restTime = 8  # seconds
    timeout = 25  # seconds

    upDIR = "P8_17"
    downDIR = "P8_15"
    upperSW = "P9_29"
    lowerSW = "P9_31"

    pwmPIN = "P8_13"

    freq = 10000
    duty = 100


    def setPin(self):
        GPIO.setup(self.upDIR, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.downDIR, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.upperSW, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.lowerSW, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def moveUP(self):
        PWM.start(self.pwmPIN, self.duty, self.freq, 0)
        GPIO.output(self.upDIR, GPIO.HIGH)
        status = 1
        print "Moving motor UP"
        return 0, time.time()

    def moveDOWN(self):
        PWM.start(self.pwmPIN, self.duty, self.freq, 0)
        GPIO.output(self.downDIR, GPIO.HIGH)
        status = 0
        print "Moving motor DOWN"
        return 1, time.time()

    def moveStop(self):
        #PWM.start(self.pwmPIN, 0, self.freq, 0)
        GPIO.output(self.upDIR, GPIO.LOW)
        GPIO.output(self.downDIR, GPIO.LOW)
        print "Motor STOP...!!"
        return time.time()

    def eStop(self):
        PWM.start(self.pwmPIN, 0, self.freq, 0)
        GPIO.output(self.upDIR, GPIO.LOW)
        GPIO.output(self.downDIR, GPIO.LOW)


def myCallback(channel):
    motor.moveStop()


def main():
    global status
    global motor
    status = -1  # up = 1, down = 0
    nextMove = -1
    startTime = 0
    sleepTimer = 1000
    motor = pinConfig()
    motor.setPin()

    time.sleep(5)

    if GPIO.input(motor.upperSW):  # if on upperSW move down
        print "@Upper switch..."
        nextMove, startTime = motor.moveDOWN()
    elif GPIO.input(motor.lowerSW):  # if on lowerSW move up
        print "@Lower switch..."
        nextMove, startTime = motor.moveUP()
    else:
        print "@Middle..."
        nextMove, startTime = motor.moveUP()

    print "GPIO event enabled"
    GPIO.add_event_detect(motor.upperSW, GPIO.RISING, bouncetime=2000)
    GPIO.add_event_detect(motor.lowerSW, GPIO.RISING, bouncetime=2000)

    try:
        while True:
            #stop motor when switch trigger
            if GPIO.event_detected(motor.upperSW) and GPIO.input(motor.upperSW):
                sleepTimer = motor.moveStop()
                status = 1

            #timeout condition @ upperSW
            elif GPIO.input(motor.upperSW) and timeCal(startTime) > pinConfig.timeout:
                print "Motor timeout..."
                sleepTimer = motor.moveStop()
                time.sleep(pinConfig.restTime)
                status = 1
                if nextMove == 0:
                    nextMove, startTime = motor.moveDOWN()
                    status = 0
                elif nextMove == 1:
                    nextMove, startTime = motor.moveUP()
                    status = 0

            if GPIO.event_detected(motor.lowerSW) and GPIO.input(motor.lowerSW):
                sleepTimer = motor.moveStop()
                status = 1

            #timeout condition @ lowerSW
            elif GPIO.input(motor.lowerSW) and timeCal(startTime) > pinConfig.timeout:
                print "Motor timeout..."
                sleepTimer = motor.moveStop()
                time.sleep(pinConfig.restTime)
                status = 1
                if nextMove == 0:
                    nextMove, startTime = motor.moveDOWN()
                    status = 0
                elif nextMove == 1:
                    nextMove, startTime = motor.moveUP()
                    status = 0

            # motor timeout without upperSW/lowerSW
            if timeCal(startTime) > pinConfig.timeout:
                print "Motor timeout...no switch detected"
                sleepTimer = motor.moveStop()
                time.sleep(pinConfig.restTime)
                status = 1
                if nextMove == 0:
                    nextMove, startTime = motor.moveDOWN()
                    status = 0
                elif nextMove == 1:
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

    # motor.moveUP()  # optionally, you can set the frequency as well as the polarity from their defaults:
    # PWM.start("P9_14", 50, 1000, 1)
    # PWM.set_duty_cycle("P9_14", 25.5)
    # PWM.set_frequency("P9_14", 10)


if __name__ == "__main__":
    main()
