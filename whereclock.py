#!/usr/bin/env python

# This code is written by Stephen C Phillips.
# It is in the public domain, so you can do what you like with it
# but a link to http://scphillips.com would be nice.

import socket
import re
from datetime import datetime
import pygame
import RPi.GPIO as GPIO
from Stepper import Motor

# Set up stepper-motor:
GPIO.setmode(GPIO.BOARD)
motor = Motor([18,22,24,26])
motor.rpm = 5

# Set up the clock locations:
location = {
    'home': 0,
    'woodcraft': 45,
    'work': 90,
    'pub': 135,  # this is more of an aspration than a location
    'salsa': 180,
    'pilates': 225,
    'travelling': 270,
    'mortalperil': 315,  # traditionally must be included
    }

# Standard socket stuff:
host = ''  # do we need socket.gethostname() ?
port = 4387
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(1)  # don't queue up any requests

# pygame things for sound
pygame.init()
sound = pygame.mixer.Sound('/home/pi/whereClock/ZINGBONK.WAV')

print "Server running on port " + `port`

# Loop forever, listening for requests:
while True:
    print "Waiting..."
    csock, caddr = sock.accept()
    print datetime.today()
    print "Connection from: " + `caddr`
    req = csock.recv(1024)  # get the request, 1kB max
    req = req.split("\n")[0]
    print "Request: " + req
    # Look in the first line of the request for a move command
    # A move command should be e.g. 'http://server/move?a=90'
    match_angle = re.match('GET /move\?a=(\d+)\sHTTP/1', req)
    match_location = re.match('GET /move\?l=(\w+)\sHTTP/1', req)
    if match_angle:
        angle = int(match_angle.group(1))
        print "Angle: " + `angle`
        csock.sendall("HTTP/1.0 200 OK\r\n\r\n")
        print "Moving motor..."
        motor.move_to(angle)
    elif match_location:
        loc = match_location.group(1)
        try:
            print "Location: " + loc
            angle = location[loc]
            print "Angle: " + `angle`
            csock.sendall("HTTP/1.0 200 OK\r\n\r\n")
            print "Moving motor..."
            sound.play()
            motor.move_to(angle)        
        except KeyError:
            print "Location " + loc + " is unknown, returning 501"
            csock.sendall("HTTP/1.0 501 Not Implemented\r\n\r\n")
    else:
        # If there was no recognised command then return a 404 (page not found)
        print "Returning 404"
        csock.sendall("HTTP/1.0 404 Not Found\r\n\r\n")
    csock.close()
    print "--------"
