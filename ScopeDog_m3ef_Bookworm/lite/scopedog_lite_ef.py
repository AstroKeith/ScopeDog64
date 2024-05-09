#!/usr/bin/env python3

# Program to implement a combined ScopeDog & eFinder (electronic finder) on motorised Alt Az telescopes
# Copyright (C) 2024 Keith Venables.
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# This variant is customised for ZWOASI or QHY ccds as camera, No DSC
# It requires astrometry.net installed

from Phidget22.Phidget import *
from Phidget22.Devices.Stepper import *
from Phidget22.Devices.DigitalInput import *
from Phidget22.Devices.DigitalOutput import *
from Phidget22.Devices.VoltageRatioInput import *
import time
import math
import os
import sys
from datetime import datetime
from gpiozero import LED, Button
import serial
from threading import Thread
import subprocess
from PIL import Image
import psutil
import shutil
from shutil import copyfile
import glob
import re
from skyfield.api import load, Star
import skyfield.positionlib
import skyfield.toposlib
import numpy as np
import select
from pathlib import Path
import fitsio
import Location_64
import Coordinates_lite
import Display_64
from collections import OrderedDict
import socket


ser = serial.Serial("/dev/ttyAMA2",baudrate=19200)

azSteps = altSteps=0
trackFracAZ = trackFracALT = 0.0
stepAngle = 1.8/16.0
jStickSpeed = 1
azCurrentPosition = altCurrentPosition = 100000
azAPSAval = altAPSAval=0
go_to = False
moving = False
calibrate = False
az_Joy = alt_Joy = False
home_path = str(Path.home())
print('homepath',home_path)
version = "lite_7" 
x = y = 0  # x, y  define what page the display is showing
deltaAz = deltaAlt = 0
increment = [0, 1, 5, 1, 1]
offset_flag = False
align_count = 0
offset = 640, 480
star_name = "no star"
solve = False
sync_count = 0
pix_scale = 15.4
count = 1
loop = ""
rateInd = 0
rateTable = ["Sidereal","Lunar","No Drive"]
rate_str = rateTable[rateInd]
ts = load.timescale()
alt_rate = az_rate = 0
newAzRatio = newAltRatio = azBacklash = altBacklash = lookRatio = 0
cAz = cAlt = 0
doMove = False
speed = 10

try:
    import board
    import busio
    import adafruit_ina260
    i2c = busio.I2C(board.SCL, board.SDA)
    
    adafruit_ina260.AveragingCount.COUNT_1024
    adafruit_ina260.Mode.CONTINUOUS
    ina260 = adafruit_ina260.INA260(i2c)
    ina = True
except:
    print("no Power Sensor fitted")
    ina = False

def scopedog_loop(): # run at 1Hz
    global ina, lst, lowBattery, az_Joy, alt_rate, az_rate, jStickSpeed, scopeAz, scopeAlt, scopeDec, scopeAz, alt_Joy, go_to, moving, loop, arr,ampHour,scopeRa,scopeDec
    blink = True
    lowBattery = False
    ampHour = 0
    time.sleep(1) 
    while True:
        Led1.toggle()
        if go_to == True:
            print('go_to True')
            loop = ""
            performSSgoto()
            if param["Auto GoTo++"] == '1' and rateInd != 1:
                loop = "++"
                time.sleep(0.1)
                handpad.display("Attempting", "Auto GoTo++", "")
                go_to = True
                time.sleep(1)
                do_align()
                time.sleep(1)
                performSSgoto()
                loop = ""
                go_solve()
            go_to = False
        elif doMove == True:
            print('moving scope')
            moveScope(dirMove)
        now = datetime.now()
        nowStr = now.strftime("%d/%m/%Y %H:%M:%S")
        t = ts.now()
        lst = t.gmst + lon/15
        
        if align_count != 0:
            azCountPos = azStepAngle * int(-azDir) * azStepper.getPosition()+ cAz
            altCountPos = altStepAngle * int(-altSide) * AltStepper.getPosition()+ cAlt
            scopeRa,scopeDec = geoloc.altaz2Radec(azCountPos,altCountPos)
             
        
        scopeAlt, scopeAz, alt_s_rate, az_s_rate = (geoloc.get_rate(scopeRa,scopeDec))

        if rateInd == 0:
            alt_rate = alt_s_rate
            az_rate = az_s_rate
        elif rateInd == 1:
            g_ra, g_dec, alt, alt_rate, az_rate = geoloc.get_lunar_rates()
        elif rateInd == 2:
            alt_rate = az_rate = 0

        if (az_Joy == False) and (alt_Joy == False) and (go_to == False) and (moving == False):
            
            trackInALT(alt_rate)
            trackInAZ(az_rate)
          
            print("************************")
            print("RPI  ",nowStr, "  LST",coordinates.dd2dms(lst).strip('+') )
            print("RA:  ",coordinates.dd2dms(scopeRa).strip('+'), "   Dec:  ",coordinates.dd2dms(scopeDec))
            print("           Az         Alt")
            print('%s    %3s      %s   %s' % ('Angle',coordinates.dd2dms(scopeAz.degrees).strip('+'),coordinates.dd2dms(scopeAlt.degrees),'degrees'))
            #print('%s   %3s      %s   %s' % ('AngleC',coordinates.dd2dms(azCountPos).strip('+'),coordinates.dd2dms(altCountPos),'degrees'))
            print('%s   %2.3f       %2.3f   %s' % ('Motion',az_rate,alt_rate,'"/sec'))
            print('%s     %6.4f      %6.4f' % ('APSA',azAPSAval,altAPSAval))
            print('%s    %3.0f         %3.0f' % ('steps',azSteps,altSteps))
            print("%s %s   %s %s" % (' GoTo:',go_to,'Move:',moving))
            print('%s %s   %s %s' % (' Az-joy:',az_Joy,' Alt-joy:',alt_Joy)) 

        try:
            if ina260.voltage < float(param["volt_alarm"]):
                lowBattery = True
            else:
                lowBattery = False
            ampHour = ampHour + ina260.current/(1000*3600)
        except:
            pass
        
        if x == 0 and y == 0:
            line_1 = '%s %s' % ('RA:',coordinates.dd2dms(scopeRa).strip('+'))
            line_2 = '%s %s' % ('Dec:',coordinates.dd2dms(scopeDec))
            if lowBattery == True:
                if blink == True:
                    line_3 = "Low Battery !!"
                else:
                    line_3 = ""
                blink = not blink
            else:
                line_3 = '%s%3d %s%2d' % ('Az:',scopeAz.degrees,'Alt:',scopeAlt.degrees)
            handpad.display(line_1.ljust(15)+rate_str[0],line_2,line_3)
        elif (x == 0 and y == 4 and ina == True):
            arr[0,4][0] = "V:%.1f Vlim:%s" % (ina260.voltage,param["volt_alarm"])
            arr[0,4][1] = "%.0f mA" % (ina260.current)
            arr[0,4][2] = "%.1f AHr" % (ampHour)
            refresh()
        else:
            if lowBattery == True:
                if blink == True:
                    handpad.display(arr[x,y][0],arr[x,y][1],"Low Battery !!")
                else:
                    handpad.display(arr[x,y][0],arr[x,y][1],"")
                blink = not blink
        remain = 1-(time.time() % 1)
        time.sleep(remain)
        
def serveWifi(): # replace with serve WiFi port
    global gotoRa,gotoDec, go_to,doMove, dirMove, scopeRa, scopeDec, speed

    host = ''
    port = 4060
    backlog = 50
    size = 1024
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host,port))
    s.listen(backlog)
    try:
        while True:
            client, address = s.accept()
            while True:
                data = client.recv(size)
                if not data:
                    break
                if data:
                    pkt = data.decode("utf-8","ignore")
                    Led2.toggle()
                    time.sleep(0.02)
                    if align_count != 0:
                        azCountPos = azStepAngle * int(-azDir) * azStepper.getPosition()+ cAz
                        altCountPos = altStepAngle * int(-altSide) * AltStepper.getPosition()+ cAlt
                        scopeRa,scopeDec = geoloc.altaz2Radec(azCountPos,altCountPos)
                    #print(pkt)
                    #time.sleep(0.1)
                    a = pkt.split('#')
                    #print(a)
                    raPacket = coordinates.dd2dms(scopeRa)+'#'
                    decPacket = coordinates.dd2aligndms(scopeDec)+'#'
                    for x in a:
                        if x != '':
                            #print (x)
                            if x == ':GR':
                                #print("sending RA  ",raPacket)
                                #time.sleep(0.05)
                                client.send(bytes(raPacket.encode('ascii')))
                            elif x == ':GD':
                                #print("sending Dec",decPacket)
                                #time.sleep(.05)
                                client.send(bytes(decPacket.encode('ascii')))
                            elif x == ':RC':
                                #print("send Dec")
                                #time.sleep(.1)
                                speed = 10
                                #client.send(bytes(decPacket.encode('ascii')))
                            elif x[1:3] == 'Sr': # goto instructions incoming
                                packet = '1'
                                raStr = x[3:]
                                client.send(b'1')
                            elif x[1:3] == 'Sd': # goto instructions incoming
                                packet = '1'
                                decStr = x[3:]
                                client.send(b'1')  
                            elif x[1:3] == 'MS':
                                client.send(b'0')
                                ra = raStr.split(':')
                                gotoRa = int(ra[0])+int(ra[1])/60+int(ra[2])/3600
                                dec = decStr.split('*')
                                decdec = dec[1].split(':')
                                gotoDec = int(dec[0]) + math.copysign((int(decdec[0])/60+int(decdec[1])/3600),float(dec[0]))
                                print('GoTo target received:',gotoRa, gotoDec)
                                go_to = True
                            elif x[1:3] == 'RG':
                                print('RG')
                                speed = 40
                                #client.send(bytes(decPacket.encode('ascii')))
                            elif x[1:3] == 'RM':
                                print('RM')
                                speed = 3
                                #client.send(bytes(decPacket.encode('ascii')))
                            elif x[1:3] == 'RS':
                                print('RS')
                                speed = 1
                                #client.send(bytes(decPacket.encode('ascii')))
                            elif x[1] == 'M':
                                doMove = True
                                dirMove = x[2]
                            elif x[1] == 'Q':
                                print('STOP!')
                                go_to = False
                                doMove = False
                                stop_goto()
                    
    except:
        pass
    

def stop_goto():
    global go_to, doMove, moving
    go_to = False
    doMove = False
    moving =False
    azStepper.setAcceleration(10000)
    azStepper.setVelocityLimit(0)
    AltStepper.setAcceleration(10000)
    AltStepper.setVelocityLimit(0)
    while azStepper.getIsMoving()==1 or AltStepper.getIsMoving()==1:
        time.sleep(0.1)
    print('goto stopped, go_to is:',go_to)


def butChange(state=True):
    global AZjStickSlewSpeed,ALTjStickSlewSpeed,jStickSpeed
    if state != True:
        return
    if jStickSpeed == 3:
        jStickSpeed = 1
        AZjStickSlewSpeed = azVelocityLim/azSlewSpeedSlow
        ALTjStickSlewSpeed = altVelocityLim/altSlewSpeedSlow
    elif jStickSpeed == 1:
        jStickSpeed = 2
        AZjStickSlewSpeed = azVelocityLim/azSlewSpeedMed
        ALTjStickSlewSpeed = altVelocityLim/altSlewSpeedMed
    elif jStickSpeed == 2:
        jStickSpeed = 3
        AZjStickSlewSpeed = azVelocityLim
        ALTjStickSlewSpeed = altVelocityLim
    handpad.set_speed(int(jStickSpeed))
        
def moveScope(moveString):
    global moving
    print ('move speed',speed)
    Alt = False
    Az = False
    if (moveString == "n"):
        diRection = (int)(-1 * altSide)
        Alt = True
    elif (moveString == "s"):
        diRection = (int)(1 * altSide)
        Alt = True
    elif (moveString == "e"):
        diRection = -1
        Az = True
    elif (moveString == "w"):
        diRection = 1
        Az = True
    if (Az):
        if (speed == 0):  # this means stop!
            azStepper.setAcceleration(50000)
            azStepper.setVelocityLimit(0)
            while azStepper.getIsMoving()==1:
                time.sleep(0.1)
            moving = False
        else: # this means start!
            azStepper.setAcceleration(10000)
            azStepper.setVelocityLimit(azVelocityLim/speed)
            azStepper.setTargetPosition(diRection*max)
            azStepper.setEngaged(True)
            moving = True
    elif (Alt):
        if (speed == 0):  # this means stop!
            AltStepper.setAcceleration(50000)
            AltStepper.setVelocityLimit(0)
            while AltStepper.getIsMoving()==1:
                time.sleep(0.1)
            moving = False
        else: # this means start!
            AltStepper.setAcceleration(10000)
            AltStepper.setVelocityLimit(altVelocityLim/speed)
            AltStepper.setTargetPosition((diRection * max))
            AltStepper.setEngaged(True)
            moving = True
    if moving == False:
        return
        
def jStickMoveAz(azStick):
    global az_Joy,jStickSpeed
    if(azStick == '+'):
        azStepper.setEngaged(False)
        az_Joy=True
        azStepper.setAcceleration(10000)
        azStepper.setVelocityLimit(AZjStickSlewSpeed)
        if (jStickSpeed==1):
            azStepper.setTargetPosition(max*flip_AzS)	
        else:
            azStepper.setTargetPosition(-max*flip_AzF)
        azStepper.setEngaged(True)
    elif(azStick == '-'):
        azStepper.setEngaged(False)
        az_Joy=True
        azStepper.setAcceleration(10000)
        azStepper.setVelocityLimit(AZjStickSlewSpeed)
        if (jStickSpeed==1):
            azStepper.setTargetPosition(-max*flip_AzS)
        else:
            azStepper.setTargetPosition(max*flip_AzF)
        azStepper.setEngaged(True)
    else:
        azStepper.setAcceleration(50000)
        azStepper.setVelocityLimit(0)
        while azStepper.getIsMoving()==1:
            time.sleep(0.1)
        az_Joy=False
        
def jStickMoveAlt(altStick):
    global alt_Joy, jStickSpeed
    if(altStick == '+'):
        AltStepper.setEngaged(False)
        alt_Joy=True
        AltStepper.setAcceleration(10000)
        AltStepper.setVelocityLimit(ALTjStickSlewSpeed)
        if (jStickSpeed==1):
            AltStepper.setTargetPosition(-ALTmax*flip_AltS)
        else:
            AltStepper.setTargetPosition(ALTmax*flip_AltF)
        AltStepper.setEngaged(True)
    elif(altStick == '-'):
        AltStepper.setEngaged(False)
        alt_Joy=True
        AltStepper.setAcceleration(10000)
        AltStepper.setVelocityLimit(ALTjStickSlewSpeed)
        AltStepper.setTargetPosition(-ALTmax*flip_AltF)
        if (jStickSpeed==1):
            AltStepper.setTargetPosition(ALTmax*flip_AltS)
        else:
            AltStepper.setTargetPosition(-ALTmax*flip_AltF)
        AltStepper.setEngaged(True)
    else:
        AltStepper.setAcceleration(50000)
        AltStepper.setVelocityLimit(0)
        while AltStepper.getIsMoving()==1:
            time.sleep(0.1)
        alt_Joy=False


def trackInAZ(azMotion):
    global azSteps,azAPSAval,trackFracAZ, azCurrentPosition, stepsPerArcsecAZ
    if (abs(azMotion) > 250): # 'dobhole'
        azMotion = math.copysign(250,azMotion)
    azAPSAval = stepsPerArcsecAZ * azMotion  
    trackFracHVal = 0
    if (azAPSAval<0):
        trackVal = math.ceil(azAPSAval)
        trackFrac = azAPSAval-trackVal
    else:
        trackVal = math.floor(azAPSAval)
        trackFrac = azAPSAval-trackVal
    trackFracAZ = trackFracAZ + trackFrac
    if (trackFracAZ <= -1):
        trackFracHVal = math.ceil(trackFracAZ)
        trackFracAZ = trackFracAZ-trackFracHVal
    elif(trackFracAZ >= 1):
        trackFracHVal = math.floor(trackFracAZ)
        trackFracAZ = trackFracAZ-trackFracHVal
    trackVal=trackVal+trackFracHVal
    azSteps=trackVal
    acclVal = math.pow(trackVal*2.0, 2)
    if (acclVal == 0):
        acclVal=10
    azStepper.setTargetPosition(azStepper.getPosition()+((int)(trackVal) * -(int)(azDir)))
    azStepper.setAcceleration(acclVal)
    azStepper.setVelocityLimit((int)(abs(trackVal*1.15)))
    azStepper.setEngaged(True)

def trackInALT(altMotion):
    global altSteps, altAPSAval, trackFracALT,altCurrentPosition, stepsPerArcsecALT
    altAPSAval = stepsPerArcsecALT * altMotion
    trackFracHVal = 0
    if (altAPSAval<0):
        trackVal = math.ceil(altAPSAval)
        trackFrac = altAPSAval-trackVal
    else:
        trackVal = math.floor(altAPSAval)
        trackFrac = altAPSAval-trackVal
    trackFracALT = trackFracALT + trackFrac
    if (trackFracALT <= -1):
        trackFracHVal = math.ceil(trackFracALT)
        trackFracALT = trackFracALT-trackFracHVal
    elif (trackFracALT >= 1):
        trackFracHVal = math.floor(trackFracALT)
        trackFracALT = trackFracALT-trackFracHVal
    trackVal=trackVal+trackFracHVal
    altSteps=trackVal
    acclVal = math.pow(trackVal*2.0, 2)
    if (acclVal == 0):
        acclVal=10
    AltStepper.setTargetPosition(AltStepper.getPosition()+((int)(trackVal) * -(int)(altSide)))
    AltStepper.setAcceleration(acclVal)
    AltStepper.setVelocityLimit((int)(abs(trackVal*1.15)))
    AltStepper.setEngaged(True)

def calculateGoToSteps():
    # update Goto AltAz coordinates
    #gotoRa = goto_radec[0]
    #gotoDec = goto_radec[1]
    position = skyfield.positionlib.position_of_radec(gotoRa, gotoDec, epoch=ts.now())
    ra, dec, d = position.radec(ts.J2000)
    gotoAlt, gotoAz, alt_rate, az_rate = (geoloc.get_rate(ra.hours,dec.degrees))
    # calculate deltas
    newDeltaAZ = gotoAz.degrees - scopeAz.degrees
    newDeltaALT = gotoAlt.degrees - scopeAlt.degrees
    if (abs(newDeltaAZ) > 180):
        if (newDeltaAZ < 0):
            newDeltaAZ = newDeltaAZ + 360
        else:
            newDeltaAZ = newDeltaAZ - 360
    return(newDeltaAZ,newDeltaALT)

def performSSgoto():
    global stoppedAZ, stoppedALT, tracking, count, go_to, altCurrentPosition, azCurrentPosition
    while go_to:
        stepsPreDegALT = altRatio/stepAngle
        stepsPreDegAZ =  azRatio/stepAngle
        totalStepsAZ = 0
        totalStepsALT = 0
        newDeltaAZ,newDeltaALT = calculateGoToSteps()
        print('++++++++++++++')
        print("%s %7.3f   %7.3f  %s" % ('goto deltas',newDeltaAZ,newDeltaALT,'degrees'))
        print('Performing GoTo iteration ',count)
        handpad.display('GoTo Deltas','Az: '+str(newDeltaAZ)[0:6],'Alt: '+str(newDeltaALT)[0:6])
        totalStepsAZ = stepsPreDegAZ * -newDeltaAZ
        totalStepsALT = stepsPreDegALT * -newDeltaALT
        azStepper.setEngaged(False)
        AltStepper.setEngaged(False)
        AltStepper.setTargetPosition(AltStepper.getPosition()+totalStepsALT * altSide)
        AltStepper.setAcceleration(3800)
        AltStepper.setVelocityLimit(23000) 
        azStepper.setTargetPosition(azStepper.getPosition()+totalStepsAZ * azDir)
        azStepper.setAcceleration(3800)
        azStepper.setVelocityLimit(23000)
        azStepper.setEngaged(True)
        AltStepper.setEngaged(True)
        while azStepper.getIsMoving()==1 or AltStepper.getIsMoving()==1:
            time.sleep(0.1)
        time.sleep(0.4)

        # insert solve/align so as to fix scopeRA & scopeDec
        '''
        scope = Star(ra_hours=scopeRa, dec_degrees=scopeDec)  # will set as J2000 as no epoch input
        scopeLoc = (geoloc.get_location().at(coordinates.get_ts().now()).observe(scope))  # now at Jnow and current location
        goto = Star(ra_hours=gotoRa, dec_degrees=gotoDec)  # will set as J2000 as no epoch input
        gotoLoc = (geoloc.get_location().at(coordinates.get_ts().now()).observe(goto))  # now at Jnow and current location
        sep = scopeLoc.separation_from(gotoLoc)
        delta = sep.arcminutes()
        print('%s %3.1f %s' % ('delta',delta,'arc minutes'))
        delta_str = ('%3.1f' % delta)
        if delta > backlash:
            count +=1
            performSSgoto()
        '''
        # handpad.display('Finished GoTo'+loop,'Final delta',str(delta_str)[0:4]+' arcmin')
        count = 1
        go_to = False

def driveScope(moveAz,moveAlt):
    azStepper.setEngaged(False)
    azStepper.setTargetPosition(azStepper.getPosition() + int(moveAz * azDir))
    azStepper.setAcceleration(3800)
    azStepper.setVelocityLimit(23000)
    azStepper.setEngaged(True)
    AltStepper.setEngaged(False)
    AltStepper.setTargetPosition(AltStepper.getPosition() + int(moveAlt * altSide))
    AltStepper.setAcceleration(3800)
    AltStepper.setVelocityLimit(23000) 
    AltStepper.setEngaged(True)
    while azStepper.getIsMoving()==1 or AltStepper.getIsMoving()==1:
        time.sleep(0.1)
    time.sleep(1)
        
def calibrateDrive():
    global nexVsolAz, nexVsolAlt, newAzRatio,newAltRatio,azBacklash,altBacklash,solved_altaz, rateInd, altCurrentPosition, azCurrentPosition, moving, calibrate
    calibrate = True
    print('calibrating drives')
    handpad.display('About to perform','Drive','Calibration')
    moving = True
    rate = rateInd # remember current drive rate
    rateInd = 2 # turn drive off
    time.sleep(0.5)
    stepsPerDegALT = altRatio/stepAngle
    stepsPerDegAZ =  azRatio/stepAngle
    dAz = 30 # this is the angle we will intend to move the scope
    dAlt = 15
    moveAz = stepsPerDegALT * -dAz 
    moveAlt = stepsPerDegAZ * -dAlt
    print('++++++++++++++')
    print('Current ratios (Az,Alt):',azRatio,altRatio)
    print('Performing initialisation')
    handpad.display('Performing','Initialisation','Please wait')
    time.sleep(0.5)
    # first move the scope a little bit to take out any backlash
    driveScope(moveAz/200,moveAlt/100)
    # now move the scope by the intended amount 
    print('Performing First Solve & transit')
    handpad.display('Performing first','solve','keep clear')
    go_solve() # measure actual Az & Alt
    time.sleep(0.1)
    handpad.display('Performing first','transit','keep clear')
    azalt0 = solved_altaz
    print ('%s %3.3f %2.3f' % ('Initial Az,Alt:',azalt0[1],azalt0[0]))
    driveScope(moveAz,moveAlt)
    go_solve() # re-measure actual Az & Alt
    azalt1 = solved_altaz
    print ('%s %3.3f %2.3f' % ('Destination Az,Alt:',azalt1[1],azalt1[0]))
    actDeltaAz = azalt0[1] - azalt1[1]
    newAzRatio = azRatio * actDeltaAz/dAz
    actDeltaAlt = azalt0[0] - azalt1[0]
    newAltRatio = altRatio * actDeltaAlt/dAlt
    print('%s %2.3f %2.3f %s' % ('Actual delta Az, Alt:',actDeltaAz,actDeltaAlt,'degrees'))
    print ('%s %4.1f %4.1f' % ('New ratios (Az,Alt):',newAzRatio,newAltRatio))
    nexDeltaAz = nexAltAz1[1] - nexAltAz0[1]
    nexDeltaAlt = nexAltAz1[0] - nexAltAz0[0]
    time.sleep(1)
    print('Performing Final Transit & Solve')
    handpad.display('Performing final','transit & solve',' ')
    # now reverse the scope by the same amount
    driveScope(-moveAz,-moveAlt)
    go_solve() # re-measure actual Az & Alt, should be same as start, except for backlash
    azalt2 = solved_altaz
    print ('%s %3.3f %2.3f' % ('Returned to start Az,Alt:',azalt2[1],azalt2[0]))
    actDeltaAz = azalt2[1] - azalt1[1]
    azBacklash = 60 * (dAz - actDeltaAz)
    actDeltaAlt = azalt2[0] - azalt1[0]
    altBacklash = 60 * (dAlt - actDeltaAlt)
    print('%s %2.3f %2.3f %s' % ('Actual Return delta Az, Alt:',actDeltaAz,actDeltaAlt,'degrees'))
    print('%s %3.3f %3.3f %s' % ('Measured backlash   Az, Alt:', azBacklash, altBacklash,'arcmin'))
    handpad.display('B.L arcmin','Az:'+str(azBacklash)[0:6],'Alt:'+str(altBacklash)[0:6])
    rateInd = rate
    moving = False
    calibrate = False

def compareRatios(s):
    global lookRatio
    lookRatio = lookRatio + s
    if lookRatio > 2:
        lookRatio = 0
    elif lookRatio < 0:
        lookRatio = 2
    if lookRatio == 0:
        handpad.display('old/new ratios','Az: '+str(int(azRatio))+'/'+str(int(newAzRatio)),'Alt: '+str(int(altRatio))+'/'+str(int(newAltRatio)))
    elif lookRatio == 1:
        handpad.display('Backlash','Az: '+str(int(azBacklash)),'Alt: '+str(int(altBacklash)))
    else:
        handpad.display('Dummy','Az: ','Alt: ')

def saveRatios():
    global azRatio, altRatio, stepsPerArcsecAZ, stepsPerArcsecALT
    if lookRatio != 0:
        return
    keyNew = d + "_Az_Gear_Ratio"
    configCopy.update({keyNew:str(newAzRatio)})
    keyNew = d + "_Alt_Gear_Ratio"
    configCopy.update({keyNew:str(newAltRatio)})
    azRatio = newAzRatio
    altRatio = newAltRatio
    with open(home_path+"/ScopeDog.config","w") as h:
        for key, value in configCopy.items():
            h.write("%s:%s\n" % (key,value))
    stepsPerArcsecAZ = azRatio/(stepAngle * 3600) ## of steps per arcsec
    stepsPerArcsecALT = altRatio/(stepAngle * 3600) ## of steps per srcsec
    handpad.display('New Drive Ratios','saved, and','now in use')
        
def xy2rd(x, y):  # returns the RA & Dec equivalent to a camera pixel x,y
    result = subprocess.run(
        [
            "wcs-xy2rd",
            "-w",
            destPath + "capture.wcs",
            "-x",
            str(x),
            "-y",
            str(y),
        ],
        capture_output=True,
        text=True,
    )
    result = str(result.stdout)
    line = result.split("RA,Dec")[1]
    ra, dec = re.findall("[-,+]?\d+\.\d+", line)
    return (float(ra), float(dec))


def pixel2dxdy(
    pix_x, pix_y
):  # converts a pixel position, into a delta angular offset from the image centre
    deg_x = (float(pix_x) - 640) * pix_scale / 3600  # in degrees
    deg_y = (480 - float(pix_y)) * pix_scale / 3600
    dxstr = "{: .1f}".format(float(deg_x * 60))  # +ve if finder is left of Polaris
    dystr = "{: .1f}".format(
        float(deg_y * 60)
    )  # +ve if finder is looking below Polaris
    return (deg_x, deg_y, dxstr, dystr)


def dxdy2pixel(dx, dy):
    pix_x = dx * 3600 / pix_scale + 640
    pix_y = 480 - dy * 3600 / pix_scale
    dxstr = "{: .1f}".format(float(60 * dx))  # +ve if finder is left of Polaris
    dystr = "{: .1f}".format(float(60 * dy))  # +ve if finder is looking below Polaris
    return (pix_x, pix_y, dxstr, dystr)


def imgDisplay():  # displays the captured image on the Pi desktop.
    for proc in psutil.process_iter():
        if proc.name() == "display":
            proc.kill()  # delete any previous image display
    im = Image.open(destPath + "capture.jpg")
    im = im.resize((640, 480), Image.LANCZOS)
    im = im.rotate(180)
    im.show()


def solveImage():
    global offset_flag, solve, solvedPos, elapsed_time, star_name, star_name_offset, solved_radec, solved_altaz,azAngleOffset,altAngleOffset
    scale_low = str(pix_scale * 0.9)
    scale_high = str(pix_scale * 1.1)
    print('offset_flag',offset_flag)
    name_that_star = ([]) if (offset_flag == True) else (["--no-plots"])
    handpad.display("Started solving", "", "")
    limitOptions = [
        "--overwrite",  # overwrite any existing files
        "--skip-solved",  # skip any files we've already solved
        "--cpulimit",
        "10",  # limit to 10 seconds(!). We use a fast timeout here because this code is supposed to be fast
    ]
    optimizedOptions = [
        "--downsample",
        "2",  # downsample 4x. 2 = faster by about 1.0 second; 4 = faster by 1.3 seconds
        "--no-remove-lines",  # Saves ~1.25 sec. Don't bother trying to remove surious lines from the image
        "--uniformize",
        "0",  # Saves ~1.25 sec. Just process the image as-is
    ]
    scaleOptions = [
        "--scale-units",
        "arcsecperpix",  # next two params are in arcsecs. Supplying this saves ~0.5 sec
        "--scale-low",
        scale_low,  # See config above
        "--scale-high",
        scale_high,  # See config above
    ]
    fileOptions = [
        "--new-fits",
        "none",  # Don't create a new fits
        "--solved",
        "none",  # Don't generate the solved output
        "--match",
        "none",  # Don't generate matched output
        "--corr",
        "none",  # Don't generate .corr files
        "--rdls",
        "none",  # Don't generate the point list
    ]
    #    "--temp-axy",  # We can't specify not to create the axy list, but we can write it to /tmp
    
    cmd = ["solve-field"]
    captureFile = destPath + "capture.jpg"
    #imgDisplay()
    options = (
        limitOptions + optimizedOptions + scaleOptions + fileOptions + [captureFile]
    )
    start_time = time.time()
    # next line runs the plate-solve on the captured image file
    result = subprocess.run(
        cmd + name_that_star + options, capture_output=True, text=True
    )
    elapsed_time = time.time() - start_time
    print("solve elapsed time " + str(elapsed_time)[0:4] + " sec\n")
    #print(result.stdout)  # this line added to help debug.
    result = str(result.stdout)
    if "solved" not in result:
        print("Bad Luck - Solve Failed")
        handpad.display("Not Solved", "", "")
        solve = False
        return
    if (offset_flag == True) and ("The star" in result):
        table, h = fitsio.read(destPath + "capture.axy", header=True)
        star_name_offset = table[0][0], table[0][1]
        lines = result.split("\n")
        for line in lines:
            if line.startswith("  The star "):
                print('line',line)
                star_name = line.split(" ")[4]
                print("Solve-field Plot found: ", star_name)
                break
    solvedPos,solved_altaz = applyOffset()
    #print('altaz',solved_altaz)
    #print('scope:',scopeAz.degrees,scopeAlt.degrees)
    ra, dec, d = solvedPos.apparent().radec(coordinates.get_ts().now())
    solved_radec = ra.hours, dec.degrees
    arr[0, 2][0] = "Sol: RA " + coordinates.hh2dms(solved_radec[0])
    arr[0, 2][1] = "   Dec " + coordinates.dd2dms(solved_radec[1])
    arr[0, 2][2] = "time: " + str(elapsed_time)[0:4] + " s"
    solve = True
    deltaCalc()


def applyOffset():
    x_offset, y_offset, dxstr, dystr = dxdy2pixel(
        float(param["d_x"]), float(param["d_y"])
    )
    ra, dec = xy2rd(x_offset, y_offset)
    solved = Star(ra_hours=ra / 15, dec_degrees=dec)  # will set as J2000 as no epoch input
    solvedPos_scope = (geoloc.get_location().at(coordinates.get_ts().now()).observe(solved))  # now at Jnow and current location
    solvedAlt,solvedAz,rate1,rate2 = geoloc.get_rate(ra/15,dec)
    solved_altaz = solvedAlt.degrees,solvedAz.degrees
    return solvedPos_scope,solved_altaz

def deltaCalc():
    global deltaAz, deltaAlt, elapsed_time, scopeAlt, scopeAz
    
    azCountPos = azStepAngle * azStepper.getPosition()+ cAz
    altCountPos = altStepAngle * -1 * AltStepper.getPosition()+ cAlt
        
    scopeRa,scopeDec = geoloc.altaz2Radec(azCountPos,altCountPos)
    scopeAlt, scopeAz, alt_s_rate, az_s_rate = (geoloc.get_rate(scopeRa,scopeDec))

    deltaAz = solved_altaz[1] - scopeAz.degrees
    print('dektaA:',deltaAz)
    if abs(deltaAz) > 180:
        if deltaAz < 0:
            deltaAz = deltaAz + 360
        else:
            deltaAz = deltaAz - 360
    deltaAz = 60 * (
        deltaAz * math.cos(scopeAlt.degrees * math.pi/180)
    )  # actually this is delta'x' in arcminutes
    deltaAlt = solved_altaz[0] - scopeAlt.degrees
    deltaAlt = 60 * (deltaAlt)  # in arcminutes
    deltaXstr = "{: .2f}".format(float(deltaAz))
    deltaYstr = "{: .2f}".format(float(deltaAlt))
    arr[0, 1][0] = "Delta: x= " + deltaXstr
    arr[0, 1][1] = "       y= " + deltaYstr
    arr[0, 1][2] = "time: " + str(elapsed_time)[0:4] + " s"


def do_align():
    global align_count, solve, sync_count, param, offset_flag, arr, cAz, cAlt
    #new_arr = geoloc.read_altAz(arr)
    #arr = new_arr
    handpad.display('Attempting','Solve & Align','')
    capture()
    solveImage()
    if solve == False:
        handpad.display(arr[x, y][0], "Solved Failed", arr[x, y][2])
        return
    print('solved_altaz',solved_altaz)
    cAz = solved_altaz[1] - azStepAngle * azStepper.getPosition() * int(-azDir)
    cAlt = solved_altaz[0] - altStepAngle * AltStepper.getPosition() * int(-altSide)
    
def align():
    global align_count, sync_count, solve,x,y
    if camera.camType == "not found":
        handpad.display("no camera","","")
        time.sleep(2)
        return
    do_align()
    if solve == False:
        return
    
    align_count += 1
    arr[0, 3][0] = "'OK' aligns"
    arr[0, 3][1] = ""
    arr[0, 3][2] = ' count: '+str(align_count)  
    deltaCalc()
    handpad.display(arr[x,y][0],arr[x,y][1],arr[x,y][2])
    return


def measure_offset():
    global offset_str, offset_flag, param, scope_x, scope_y, star_name
    if camera.camType == "not found":
        handpad.display("no camera","","")
        time.sleep(2)
        return
    offset_flag = True
    handpad.display("started capture", "", "")
    capture()
    #imgDisplay()
    solveImage()
    if solve == False:
        handpad.display("solve failed", "", "")
        return
    scope_x = star_name_offset[0]
    scope_y = star_name_offset[1]
    print('star_name offset:',star_name_offset)
    d_x, d_y, dxstr, dystr = pixel2dxdy(scope_x, scope_y)
    param["d_x"] = d_x
    param["d_y"] = d_y
    save_param()
    offset_str = dxstr + "," + dystr
    arr[2,1][1] = "new " + offset_str
    arr[2,2][1] = "new " + offset_str
    handpad.display(arr[2,1][0], arr[2,1][1], star_name + " found")
    offset_flag = False


def up_down(v):
    global x
    x = x + v
    handpad.display(arr[x, y][0], arr[x, y][1], arr[x, y][2])


def left_right(v):
    global y
    y = y + v
    handpad.display(arr[x, y][0], arr[x, y][1], arr[x, y][2])


def up_down_inc(i, sign):
    global increment, param
    arr[x, y][1] = int(float(arr[x, y][1])) + increment[i] * sign
    param[arr[x, y][0]] = float(arr[x, y][1])
    handpad.display(arr[x, y][0], arr[x, y][1], arr[x, y][2])
    update_summary()
    time.sleep(0.1)


def flip():
    global param
    arr[x, y][1] = 1 - int(float(arr[x, y][1]))
    param[arr[x, y][0]] = str((arr[x, y][1]))
    handpad.display(arr[x, y][0], arr[x, y][1], arr[x, y][2])
    update_summary()
    time.sleep(0.1)

def toggleDrive():
    global track
    track = not track

    
def change_rate(c):
    global rateInd, rate_str
    rateInd = rateInd + c
    if rateInd > 2:
        rateInd = 0
    if rateInd < 0:
        rateInd = 2
    rate_str = rateTable[rateInd]
    arr[x,y][1] = rate_str
    handpad.display(arr[x, y][0], arr[x, y][1], arr[x, y][2])
    
def update_summary():
    global param
    arr[1, 0][0] = "Ex:" + str(param["Exposure"]) + " Gn:" + str(param["Gain"])
    arr[1, 0][1] = "Test: " + str(bool(float(param["Test mode"])))
    arr[1, 0][2] = "GoTo++: " +  str(bool(float(param["Auto GoTo++"])))
    save_param()

def refresh():
    handpad.display(arr[x, y][0], arr[x, y][1], arr[x, y][2])

def capture():
    global param
    if param["Test mode"] == "1":
        if offset_flag == False:
            m13 = True
            polaris_cap = False
        else:
            m13 = False
            polaris_cap = True
    else:
        m13 = False
        polaris_cap = False

    camera.capture(
        int(float(param["Exposure"]) * 1000000),
        int(float(param["Gain"])),
        "n/a",
        m13,
        polaris_cap,
        destPath,
    )


def go_solve():
    global x, y, solve, arr, calibrate
    if camera.camType == "not found":
        handpad.display("no camera"," "," ")
        time.sleep(2)
        return
    #new_arr = geoloc.read_altAz(arr)
    #arr = new_arr
    handpad.display("Image capture"," "," ")
    capture()
    #imgDisplay()
    handpad.display("Plate solving"," "," ")
    solveImage()
    if solve == True:
        handpad.display("Solved"," "," ")
    else:
        handpad.display("Not Solved"," "," ")
        time.sleep(2)
        return
    if calibrate == False:
        print('here')
        x = 0
        y = 1
        handpad.display(arr[0, 1][0], arr[0, 1][1], arr[0, 1][2])


def goto():
    global go_to
    handpad.display("Attempting", "GoTo++", "")
    
    align()
    if solve == False:
        handpad.display("problem", "solving", "")
        return
    go_to = True
    handpad.display("Performing", " GoTo++", "")
    print('Performing GoTo++')
    time.sleep(2) 
    go_solve()

def goto_moon():
    global gotoRa, gotoDec, go_to
    if rateInd == 0:
        goto()
        return
    elif rateInd == 2:
        return
    gotoRa, gotoDec, alt, r1, r2 = geoloc.get_lunar_rates()
    if alt < 10:
        handpad.display("Moon too low","altitude",str(alt)[0:6] + "deg")
        time.sleep(2)
        return
    go_to = True

def setGoto():
    global align_count, solve, sync_count, param, offset_flag, arr, goto_radec
    #new_arr = geoloc.read_altAz(arr)
    #arr = new_arr
    handpad.display('Attempting','Set GoTo','')
    capture()
    solveImage()
    if solve == False:
        handpad.display(arr[x, y][0], "Solved Failed", arr[x, y][2])
        time.sleep(2)
        return
    goto_radec = solved_radec
    handpad.display(arr[x, y][0], "Target Set", arr[x, y][2])


def reset_offset():
    global param, arr
    param["d_x"] = 0
    param["d_y"] = 0
    offset_str = "0,0"
    arr[2,1][1] = "new " + offset_str
    arr[2,2][1] = "new " + offset_str
    handpad.display(arr[x, y][0], arr[x, y][1], arr[x, y][2])
    save_param()


def get_param():
    global param, offset_str
    if os.path.exists(home_path + "/eFinder.config") == True:
        with open(home_path + "/eFinder.config") as h:
            for line in h:
                line = line.strip("\n").split(":")
                param[line[0]] = str(line[1])
        pix_x, pix_y, dxstr, dystr = dxdy2pixel(
            float(param["d_x"]), float(param["d_y"])
        )
        offset_str = dxstr + "," + dystr


def save_param():
    global param
    with open(home_path + "/eFinder.config", "w") as h:
        for key, value in param.items():
            #print("%s:%s\n" % (key, value))
            h.write("%s:%s\n" % (key, value))


def reader():
    global go_to
    while True:
        try:
            if handpad.get_box() in select.select([handpad.get_box()], [], [], 0)[0]:
                button = handpad.get_box().readline().decode("ascii")
                button = re.sub("\s","",button)
                #print(button,len(button))
                if button == "20":
                    exec(arr[x, y][7])
                elif button == "18":
                    exec(arr[x, y][4])
                elif button == "16":
                    exec(arr[x, y][3])
                elif button == "19":
                    exec(arr[x, y][5])
                elif button == "17":
                    exec(arr[x, y][6])
                elif button == '21':
                    exec(arr[x, y][8])
                elif button == "28":
                    if go_to == True:
                        stop_goto()
                    else:    
                        butChange()
                        handpad.display(arr[x,y][0],arr[x,y][1],'slew speed: ')
                elif button == "31":
                    jStickMoveAlt('-')
                elif button == "32":
                    jStickMoveAlt('0')
                elif button == "33":
                    jStickMoveAlt('+')
                elif button == "41":
                    jStickMoveAz('-')
                elif button == "42":
                    jStickMoveAz('0')
                elif button == "43":
                    jStickMoveAz('+')
                button = ""
        except Exception as error:
            print("read error",error)


def updateFirmware():
    filenames = glob.glob("/media/pi/*/*_new") # looks for new files on a USB stick
    if len(filenames) >0:
        print('Found on USB stick: ',filenames)
        try:
            for filename in filenames:
                print('---------------------------')
                print(filename)
                destName = filename[:-3] + "old"
                print('will create backup on USB as ',destName.split('/')[4])
                newName = home_path + '/' + filename.split('/')[4][:-4]
                shutil.copy(newName,destName) # make a safe copy of previous code on the stick.
                handpad.display('Old file copied','to USB stick','new file next')
                shutil.copy(filename,newName) # overwrite old file
                print('New ' + newName + ' successfully written to the ScopeDog')
                handpad.display('New file copied','to ScopeDog','Please wait')
            print('---------------------------')    
        except Exception as error:
            print('Problem copying files', error)
            handpad.display('Problem copying files', str(error),'Please wait')
        
        cmd = "sudo eject /dev/sda"
        os.system(cmd)
        time.sleep(3)
        print('OK to remove USB memory stick')
        handpad.display('OK to remove','USB stick','and reboot')
        
        exit()
    else:
        print('No usb or new files')

def save_image():
    print('saving last image')
    copyfile(destPath+"capture.jpg",home_path + "/Solver/Stills/" + "_" + camera.get_capture_time() + ".jpg")
    handpad.display('Saved to Stills','',camera.get_capture_time())

def vLimit_adj(i):
    global param, arr, ina
    if ina == False:
        return
    param["volt_alarm"] = str(float(param["volt_alarm"])+i/10)
    arr[x, y][0] = "V:12.3" + " Vlim:" + param["volt_alarm"]
    save_param()
    refresh()

# here starts the main code

handpad = Display_64.Handpad(version)
coordinates = Coordinates_lite.Coordinates()
geoloc = Location_64.Geoloc(handpad, coordinates)
geoloc.read()

updateFirmware()

argLen = len(sys.argv)
print ('Number of arguments:', argLen, 'arguments.')
args=sys.argv
run=False
if (argLen > 1):
    run=True
print ("Run: ",run)

Led1 = LED(17)
Led2 = LED(27)
scope_select = Button(11)
#read config file and set parameters for selected scope
d='1'
if scope_select.value:
    d='2'
print('switch is ',d)

parameters = dict()
configCopy = OrderedDict()

with open(home_path+"/ScopeDog.config") as f:
    for line in f:
        configLine = line.strip("\n").split(":")
        configCopy.update({configLine[0]:configLine[1]})
        if line[0] == d:
            if line.find("False") > 0:
                if(run==False):
                    print('Not set to autostart')
                    handpad.display('ScopeDog mk3','Autostart','not set')
                    exit()
            line = line[2:].strip("\n").split(":")
            parameters[line[0]] = line[1] 

azRatio = float(parameters['Az_Gear_Ratio'])
altRatio = float(parameters['Alt_Gear_Ratio'])
currentLimit = float(parameters['Current_Limit'])
azVelocityLim = float(parameters['azVelocity'])
altVelocityLim = float(parameters['altVelocity'])
altSlewSpeedSlow = float(parameters['SlewSpeedSlow'])
altSlewSpeedMed = float(parameters['SlewSpeedMed'])
azSlewSpeedSlow = float(parameters['SlewSpeedSlow'])
azSlewSpeedMed = float(parameters['SlewSpeedMed'])
backlash = float(parameters['Backlash'])
stepsPerArcsecAZ = azRatio/(stepAngle * 3600) ## of steps per arcsec
stepsPerArcsecALT = altRatio/(stepAngle * 3600) ## of steps per srcsec

azStepAngle = stepAngle/azRatio
altStepAngle = stepAngle/altRatio

if 'Left' in parameters['Alt_Gear']:
    altSide = 1.0
    ALTmax=20000000
else:
    altSide = -1.0
    ALTmax=-20000000
if 'A' in parameters['Az_Direction']:
    azDir = -1.0
    max=20000000
else:
    azDir = 1.0
    max=-20000000
print('azDir:',azDir,'  altSide:',altSide)
if 'checked' in parameters['flip_AltF']:
    flip_AltF=1
else:
    flip_AltF=-1
if 'checked' in parameters['flip_AltS']:
    flip_AltS=1
else:
    flip_AltS=-1
if 'checked' in parameters['flip_AzF']:
    flip_AzF=1
else:
    flip_AzF=-1
if 'checked' in parameters['flip_AzS']:
    flip_AzS=1
else:
    flip_AzS=-1

sp = { # converts LX200 slew speed into ScopeDog max slew speed division factor
    "0":0,
    "1":40,
    "2":10,
    "3":5,
    "4":1
}


lon = geoloc.get_long() # Long
lat = geoloc.get_lat() # Lat
print("%s %2.3f  %s %3.3f" % ("Lat: ",lat,"Long: ",lon))

now = datetime.now()
nowStr = now.strftime("%d/%m/%Y %H:%M:%S")
t = ts.now()
lst = t.gmst + lon/15
scopeRa = lst
scopeDec = 89.9

azStepper = Stepper()
azStepper.setHubPort(0)
azStepper.openWaitForAttachment(2000)
print("Stepper AZ attached")
azStepper.setCurrentLimit(currentLimit)
azStepper.setAcceleration(600)
azStepper.setVelocityLimit(5000)
azStepper.setEngaged(False)
azStepper.addPositionOffset(azStepper.getPosition()*-1)

azStepper.setEngaged(True)
azStepper.setTargetPosition(0)
AltStepper = Stepper()
AltStepper.setHubPort(1)
AltStepper.openWaitForAttachment(2000)
print("Stepper ALT attached")
AltStepper.setCurrentLimit(currentLimit)
AltStepper.setAcceleration(600)
AltStepper.setVelocityLimit(5000)
AltStepper.setEngaged(False)
AltStepper.addPositionOffset(AltStepper.getPosition()*-1)
AltStepper.setEngaged(True)
AltStepper.setTargetPosition(0)

azStepper.addPositionOffset(10000000)
AltStepper.addPositionOffset(10000000)

AZjStickSlewSpeed = azVelocityLim/azSlewSpeedSlow
ALTjStickSlewSpeed = altVelocityLim/altSlewSpeedSlow
print('about to start')

param = dict()
get_param()
handpad.set_speed(int(jStickSpeed))

# array determines what is displayed, computed and what each button does for each screen.
# [first line,second line,third line, up button action,down...,left...,right...,select button short press action, long press action]
# empty string does nothing.
# example: left_right(-1) allows left button to scroll to the next left screen
# button texts are infact def functions
p = ""
scope = [
    "RA:",
    "Dec:",
    "",
    "refresh()",
    "up_down(1)",
    "refresh()",
    "left_right(1)",
    "go_solve()",
    "goto()",
]
delta = [
    "Delta: No solve",
    "'OK' solves",
    "",
    "refresh()",
    "refresh()",
    "left_right(-1)",
    "left_right(1)",
    "go_solve()",
    "goto()",
]
sol = [
    "No solution yet",
    "'OK' solves",
    "",
    "refresh()",
    "refresh()",
    "left_right(-1)",
    "left_right(1)",
    "go_solve()",
    "goto()",
]
aligns = [
    "'OK' aligns",
    "Scope not align",
    "Drive " + rate_str,
    "toggleDrive()",
    "toggleDrive()",
    "left_right(-1)",
    "left_right(1)",
    "align()",
    "setGoto()",
]
summary = [
    "",
    "",
    "",
    "up_down(-1)",
    "up_down(1)",
    "refresh()",
    "left_right(1)",
    "go_solve()",
    "goto()",
]
exp = [
    "Exposure",
    param["Exposure"],
    "",
    "up_down_inc(1,1)",
    "up_down_inc(1,-1)",
    "left_right(-1)",
    "left_right(1)",
    "go_solve()",
    "goto()",
]
gn = [
    "Gain",
    param["Gain"],
    "",
    "up_down_inc(2,1)",
    "up_down_inc(2,-1)",
    "left_right(-1)",
    "left_right(1)",
    "go_solve()",
    "goto()",
]
mode = [
    "Test mode",
    int(param["Test mode"]),
    "",
    "flip()",
    "flip()",
    "left_right(-1)",
    "left_right(1)",
    "go_solve()",
    "save_image()",
]
goto_do = [
    "Auto GoTo++",
    int(param["Auto GoTo++"]),
    "",
    "flip()",
    "flip()",
    "left_right(-1)",
    "refresh()",
    "go_solve()",
    "goto()",
]
rate = [
    "Tracking rate",
    rate_str,
    "",
    "change_rate(-1)",
    "change_rate(1)",
    "left_right(-1)",
    "left_right(1)",
    "go_solve()",
    "goto_moon()",
]
status = [
    "Blank",
    "Blank",
    "Brightness",
    "up_down(-1)",
    "refresh()",
    "refresh()",
    "left_right(1)",
    "go_solve()",
    "goto()",
]
polar = [
    "'OK' Offset star",
    offset_str,
    "",
    "refresh()",
    "refresh()",
    "left_right(-1)",
    "left_right(1)",
    "measure_offset()",
    "measure_offset()",
]
reset = [
    "'OK' Resets",
    offset_str,
    "",
    "refresh()",
    "refresh()",
    "left_right(-1)",
    "left_right(1)",
    "reset_offset()",
    "reset_offset()",
]
bright = [
    "Handpad",
    "Display",
    "Bright Adj",
    "",
    "",
    "left_right(-1)",
    "refresh()",
    "go_solve()",
    "",
]
power = [
    "No Power Sensor",
    "fitted",
    "",
    "vLimit_adj(1)",
    "vLimit_adj(-1)",
    "left_right(-1)",
    "refresh()",
    "",
    "",
]
driveCalibrate = [
    "Drive",
    "Calibration",
    "Utility",
    "compareRatios(1)",
    "compareRatios(-1)",
    "left_right(-1)",
    "left_right(1)",
    "calibrateDrive()",
    "saveRatios()",
]
arr = np.array(
    [
        [scope, delta, sol, aligns, power, power],
        [summary, exp, gn, mode, goto_do, goto_do],
        [status, polar, reset, rate, driveCalibrate, bright]
    ]
)
update_summary()
deg_x, deg_y, dxstr, dystr = dxdy2pixel(float(param["d_x"]), float(param["d_y"]))
offset_str = dxstr + "," + dystr
#new_arr = geoloc.read_altAz(arr)
#arr = new_arr
if align_count != 0:
    arr[0, 3][0] = "'OK' Aligns"
    arr[0, 3][1] = "Scope is aligned"
    arr[0, 3][2] = '- count: '+str(align_count)

if 'ASI' in param["Camera Type ('QHY' or 'ASI')"]:
    import ASICamera_64
    camera = ASICamera_64.ASICamera(handpad)
elif 'QHY' in param["Camera Type ('QHY' or 'ASI')"]:
    import QHYCamera2
    camera = QHYCamera2.QHYCamera(handpad)

if param["Ramdisk"].lower()=='true':
    destPath = "/var/tmp/"
else:
    destPath = home_path + "/Solver/images/"

handpad.display("ScopeDog mk4","with eFinder","ver " + version) 
time.sleep(1)
handpad.display(arr[x,y][0],arr[x,y][1],arr[x,y][2]) 

scan = Thread(target=reader)
scan.daemon = True
scan.start()
time.sleep(0.5)

xloop = Thread(target=scopedog_loop)
xloop.daemon = True
xloop.start()

wifiloop = Thread(target=serveWifi)
wifiloop.start()
time.sleep(0.5)




