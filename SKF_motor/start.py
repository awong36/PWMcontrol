#!/usr/bin/env python
#PWMcontrol version 1.1
#updates: controls two motors, timeout and sleep timer enabled
#Program designed by Adrian Wong

import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO
from CommonFunction import timeCal
import time


class pinConfig(object):
    restTime = 8  # seconds
    timeout = 30  #seconds

    upDIR = "P9_15"
    downDIR = "P9_12"
    upperSW = "P9_25"
    lowerSW = "P9_28"

    pwmPIN = "P9_14"
    freq = 10000
    duty = 100

    def setGPIO(self, up, down, upSW, loSW, pwm):
        self.upDIR = up
        self.downDIR = down
        self.upperSW = upSW
        self.lowerSW = loSW
        self.pwmPIN = pwm

    def setPin(self):
        GPIO.setup(self.upDIR, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.downDIR, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.upperSW, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.lowerSW, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def moveUP(self, device):
        PWM.start(self.pwmPIN, self.duty, self.freq, 0)
        GPIO.output(self.upDIR, GPIO.HIGH)
        timer = time.time()
        print "Moving motor %r UP" %device
        #time.sleep(1.5)
        return 1, timer  # status

    def moveDOWN(self, device):
        PWM.start(self.pwmPIN, self.duty, self.freq, 0)
        GPIO.output(self.downDIR, GPIO.HIGH)
        timer = time.time()
        print "Moving motor %r DOWN" %device
        #time.sleep(1.5)
        return 0, timer  # status

    def moveStop(self, device):
        # PWM.stop(self.pwmPIN)
        PWM.start(self.pwmPIN, 0, self.freq, 0)
        GPIO.output(self.upDIR, GPIO.LOW)
        GPIO.output(self.downDIR, GPIO.LOW)
        print "Motor %r STOP...!!" %device
        print "Motor %r... ... Sleeping ZZZzz" %device
        sleepTimer = time.time()
        return 0, sleepTimer #reset startTime, set sleep timer


def main():
    status = [0, -1, -1]  # [ignore,device1,device2] up = 1, down = 0
    startTime = [0, 0, 0]
    ready = [0, 0, 0]
    sleepTimer = [0, 0, 0]
    motor1 = pinConfig()
    motor1.setGPIO("P9_15", "P9_12", "P9_25", "P9_28", "P9_14")
    motor1.setPin()

    motor2 = pinConfig()
    motor2.setGPIO("P8_17", "P8_15", "P9_29", "P9_31", "P8_13")
    motor2.setPin()

    if GPIO.input(motor1.upperSW):  # if on upperSW move down
        print "Motor1 @Upper switch..."
        status[1], startTime[1] = motor1.moveDOWN(1)
    elif GPIO.input(motor1.lowerSW):  # if on lowerSW move up
        print "Motor1 @Lower switch..."
        status[1], startTime[1] = motor1.moveUP(1)
    else:
        print "Motor1 @Middle..."
        status[1], startTime[1] = motor1.moveUP(1)

    if GPIO.input(motor2.upperSW):
        print "Motor2 @Upper switch..."
        status[2], startTime[2] = motor2.moveDOWN(2)
    elif GPIO.input(motor2.lowerSW):
        print "Motor2 @Lower switch..."
        status[2], startTime[2] = motor2.moveUP(2)
    else:
        print "Motor2 @Middle..."
        status[2], startTime[2] = motor2.moveUP(2)

    print "GPIO event enabled"
    GPIO.add_event_detect(motor1.upperSW, GPIO.RISING, bouncetime=1000)
    GPIO.add_event_detect(motor1.lowerSW, GPIO.RISING, bouncetime=1000)
    GPIO.add_event_detect(motor2.upperSW, GPIO.RISING, bouncetime=1000)
    GPIO.add_event_detect(motor2.lowerSW, GPIO.RISING, bouncetime=1000)

    try:
        while True:
            # print status
            if status[1] == 1:
                if GPIO.input(motor1.upperSW) and GPIO.event_detected(motor1.upperSW):
                    print "Motor1 @Upper switch..."
                    startTime[1], sleepTimer[1] = motor1.moveStop(1)

                if ready[1] == 1:
                    status[1], startTime[1] = motor1.moveDOWN(1)
                    ready[1] = 0

                if timeCal(startTime[1]) > pinConfig.timeout:
                    startTime[1], sleepTimer[1] = motor1.moveStop(1)
                    status[1] = 0

            elif status[1] == 0:
                if GPIO.input(motor1.lowerSW) and GPIO.event_detected(motor1.lowerSW):
                    print "Motor1 @Lower switch..."
                    startTime[1], sleepTimer[1] = motor1.moveStop(1)

                if ready[1] == 1:
                    status[1], startTime[1] = motor1.moveUP(1)
                    ready[1] = 0

                if timeCal(startTime[1]) > pinConfig.timeout:
                    startTime[1], sleepTimer[1] = motor1.moveStop(1)
                    status[1] = 1

            if status[2] == 1:
                if GPIO.input(motor2.upperSW) and GPIO.event_detected(motor2.upperSW):
                    print "Motor2 @Upper switch..."
                    startTime[2], sleepTimer[2] = motor2.moveStop(2)

                if ready[2] == 1:
                    status[2], startTime[2] = motor2.moveDOWN(2)
                    ready[2] = 0

                if timeCal(startTime[2]) > pinConfig.timeout:
                    startTime[2], sleepTimer[2] = motor2.moveStop(2)
                    status[2] = 0

            elif status[2] == 0:
                if GPIO.input(motor2.lowerSW) and GPIO.event_detected(motor2.lowerSW):
                    print "Motor2 @Lower switch..."
                    startTime[2], sleepTimer[2] = motor2.moveStop(2)

                if ready[2] == 1:
                    status[2], startTime[2] = motor2.moveUP(2)
                    ready[2] = 0

                if timeCal(startTime[2]) > pinConfig.timeout:
                    startTime[2], sleepTimer[2] = motor2.moveStop(2)
                    status[2] = 1

            if timeCal(sleepTimer[1]) > pinConfig.restTime:
                ready[1] = 1
            if timeCal(sleepTimer[2]) > pinConfig.restTime:
                ready[2] = 1


    except KeyboardInterrupt:
        motor1.moveStop()
        motor2.moveStop()
        GPIO.cleanup()

        # if GPIO.event_detected(motor.upperSW):
        # print "@Upper switch..."
        # motor.moveStop()
        # print "... ... Sleep ZZZzz"
        # time.sleep(pinConfig.restTIme)
        # motor.moveDOWN()
        # elif GPIO.event_detected(motor.lowerSW):
        # print "@Lower switch..."
        # motor.moveStop()
        # print "... ... Sleeping ZZZzz"
        # time.sleep(pinConfig.restTIme)
        # motor.moveUP()


# optionally, you can set the frequency as well as the polarity from their defaults:
# PWM.start("P9_14", 50, 1000, 1)
# PWM.set_duty_cycle("P9_14", 25.5)
# PWM.set_frequency("P9_14", 10)

if __name__ == "__main__":
    main()
