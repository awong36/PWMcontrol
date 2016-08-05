import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO
import time

class pinConfig(object):
	restTIme = 5 #seconds

	upDIR = "P8_17"
	downDIR = "P8_15"
	upperSW = "P9_29"
	lowerSW = "P9_31"
	
	pwmPIN = "P8_13"
	freq = 10000
	duty = 100
	
	def setPin(self):
		GPIO.setup(self.upDIR, GPIO.OUT)
		GPIO.setup(self.downDIR, GPIO.OUT)
		GPIO.setup(self.upperSW, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		GPIO.setup(self.lowerSW, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	
	def moveUP(self):
		PWM.start(self.pwmPIN, self.duty, self.freq, 0)
		GPIO.output(self.upDIR, GPIO.HIGH)
		status = 1
		print "Moving motor UP"
		time.sleep(1.5)
		return status
		
	def moveDOWN(self):
		PWM.start(self.pwmPIN, self.duty, self.freq, 0)
		GPIO.output(self.downDIR, GPIO.HIGH)
		status = 0
		print "Moving motor DOWN"
		time.sleep(1.5)
		return status
		
	def moveStop(self):
		#PWM.stop(self.pwmPIN)
		GPIO.output(self.upDIR, GPIO.LOW)
		GPIO.output(self.downDIR, GPIO.LOW)
		print "Motor STOP...!!"
	
def main():
	global status 
	status = -1 #up = 1, down = 0
	motor = pinConfig()
	motor.setPin()
	
	if GPIO.input(motor.upperSW): #if on upperSW move down
		print "@Upper switch..."
		status = motor.moveDOWN()
	elif GPIO.input(motor.lowerSW): #if on lowerSW move up
		print "@Lower switch..."
		status = motor.moveUP()
	else:
		print "@Middle..."
		status = motor.moveUP()
	
	print "GPIO event enabled"
	GPIO.add_event_detect(motor.upperSW, GPIO.RISING, bouncetime=1000)
	GPIO.add_event_detect(motor.lowerSW, GPIO.RISING, bouncetime=1000)
	
	try:
		while True:
			#print status
			if status == 1: 
				if GPIO.input(motor.upperSW) and GPIO.event_detected(motor.upperSW):
					print "@Upper switch..."
					motor.moveStop()
					print "... ... Sleep ZZZzz"
					time.sleep(pinConfig.restTIme)
					status = motor.moveDOWN()
				
			elif status == 0:
				if GPIO.input(motor.lowerSW) and GPIO.event_detected(motor.lowerSW):
					print "@Lower switch..."
					motor.moveStop()
					print "... ... Sleeping ZZZzz"
					time.sleep(pinConfig.restTIme)
					status = motor.moveUP()

	except KeyboardInterrupt: 
		motor.moveStop()
		#GPIO.cleanup() 	
		
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
	

#optionally, you can set the frequency as well as the polarity from their defaults:
#PWM.start("P9_14", 50, 1000, 1)
#PWM.set_duty_cycle("P9_14", 25.5)
#PWM.set_frequency("P9_14", 10)

if __name__ == "__main__":
	main()