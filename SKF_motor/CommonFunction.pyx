#!/usr/bin/env python
#CommonFunction version 1.0
#updates: class implementation, common function
#compile command: python setup.py build_ext --inplace
#Program designed by Adrian Wong
import time, math, csv

def timeCal(arg):  #time calculation
    cdef long end_time = time.time()
    cdef long timeElapse = end_time - <long> arg
    return timeElapse

def signedInt(arg):
    #MOD(NUM+2^15,2^16)-2^15
    cdef int num = ((<int> arg + 2 ** 15) % (2 ** 16)) - 2 ** 15
    #signedInt = str(signedInt)
    return num

def shiftTemp(arg):
    cdef double num = <double> arg
    cdef double temp = num * math.pow(10, -1)
    temp = round(temp,1)
    #temp = str(temp)
    return temp

def shiftCurrent(arg):
    #MOD(NUM+2^15,2^16)-2^15
    cdef double n = ((((<int> arg + 2 ** 15) % (2 ** 16)) - 2 ** 15) * math.pow(10,-1))
    n = round(n,1)
    #signedInt = str(signedInt)
    return n

def statusCheck(arg,mask):
    cdef int status = <int> arg
    cdef int check = <int> mask
    cdef int n = <int> (status & check)
    return n

#load settings from file
def loadSettings(name):
    with open(name, 'rb') as getInfo:
        reader = csv.reader(getInfo)
        for csvInfo in reader:
            x = 1
    getInfo.close()
    return csvInfo