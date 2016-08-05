#!/bin/sh

#define function
pinConfig(){
	if [ ! -e /sys/class/gpio/gpio48/value ] 
	then
		echo 48 > /sys/class/gpio/export
		echo out > /sys/class/gpio/gpio48/direction
	fi

	if [ ! -e /sys/class/gpio/gpio60/value ] 
	then
		echo 60 > /sys/class/gpio/export
		echo out > /sys/class/gpio/gpio60/direction
	fi

	if [ ! -e /sys/class/gpio/gpio45/value ] 
	then
		echo 45 > /sys/class/gpio/export
		echo out > /sys/class/gpio/gpio45/direction
	fi

	if [ ! -e /sys/class/gpio/gpio44/value ] 
	then
		echo 44 > /sys/class/gpio/export
		echo out > /sys/class/gpio/gpio44/direction
	fi
	
}

pwmConfig() {
	echo 5000 > duty
	echo 10000 > period
	echo 1 > run
}
pwmFull(){
	echo 10000 > duty
	echo 10000 > period
	echo 1 > run
}
pwmHalf(){
	echo 5000 > duty
	echo 10000 > period
	echo 1 > run
}
pwmStop(){
	echo 0 > run
}


#main
PIN48UP=/sys/class/gpio/gpio48/value
PIN60LOW=/sys/class/gpio/gpio60/value
pinConfig

if [ $PIN48UP]

while [ True ]
do
	echo 1 > $PIN48UP
	echo 1 > $PIN60LOW
	sleep 5
	echo 0 > $PIN48UP
	echo 0 > $PIN60LOW
	sleep 5
done
