#!/usr/bin/env python

# Imports
import webiopi
import time
import pygame.mixer
from random import choice
#from halloweenHead import HalloweenHead

# init head
webiopi.setDebug()
GPIO = webiopi.GPIO

SLEEP_TIME = 1
BLINK_TIME = 0.25
LEFT_EYE = 17
RIGHT_EYE = 22

ambianceSfx = "../sounds/DemonZombieAmbiance-SoundBible.com-1821142973.wav"
laughs = ["../sounds/evillaugh5.wav", "../sounds/evillaugh2.wav"]
screams = ["../sounds/WilhelmScream.wav", "../sounds/Scream.wav", "../sounds/scream7.wav"]
scarySounds = ["../sounds/CastleThunder.wav", "Godzilla_Roar-Marc-1912765428.wav", "Velociraptor Call-SoundBible.com-1782075819.wav"]


DEBUG = True
AMBIANCE = False

def setup():
   webiopi.debug("setting up in script")
   GPIO.setFunction(17, GPIO.OUT)
   GPIO.setFunction(22, GPIO.OUT)
   pygame.mixer.init(44100, -16, 1, 1024)
   if AMBIANCE:
      startAmbiance()


# -------------------------------------------------- #
# Main server part                                   #
# -------------------------------------------------- #


# -------------------------------------------------- #
# Loop execution part                                #
# -------------------------------------------------- #

# If no specific loop is needed and defined above, just use 
def loop():
   pass

# -------------------------------------------------- #
# Termination part                                   #
# -------------------------------------------------- #

# Cleanly stop the server
def destroy():
   pass

def set_leds(l, r):
   if DEBUG: webiopi.debug("set_leds %r %r" % (l, r))
   GPIO.digitalWrite(LEFT_EYE, l)
   GPIO.output(RIGHT_EYE, r)

@webiopi.macro
def stare(secs=None):
   if DEBUG: webiopi.debug("staring")
   set_leds(True, True)
   if (secs != None):
      if DEBUG: webiopi.debug("stare... %r" % int(secs))
      time.sleep(secs)
      rest()

@webiopi.macro
def rest():
   #If DEBUG: webiopi.debug("resting")
   set_leds(False, False)

@webiopi.macro
def blink(secs):
   if DEBUG:
      webiopi.debug("blink... %r" % int(secs))
   for x in range(0, int(secs)):
      set_leds(not GPIO.digitalRead(LEFT_EYE), not GPIO.digitalRead(RIGHT_EYE))
      time.sleep(BLINK_TIME)
      set_leds(not GPIO.digitalRead(LEFT_EYE), not GPIO.digitalRead(RIGHT_EYE))
      time.sleep(BLINK_TIME)
   rest()

@webiopi.macro
def crazyblink(secs):
   if DEBUG:
      print("crazyblink... %r" % int(secs))
   for x in range(0, int(secs)):
      set_leds(GPIO.digitalRead(LEFT_EYE), not GPIO.digitalRead(RIGHT_EYE))
      time.sleep(BLINK_TIME)
      set_leds(not GPIO.digitalRead(LEFT_EYE), not GPIO.digitalRead(RIGHT_EYE))
      time.sleep(BLINK_TIME)
   rest()

@webiopi.macro
def startAmbiance():
   if DEBUG:
      print("ambiance... ")
   bgCh = pygame.mixer.Channel(1)
   bgSfx = pygame.mixer.Sound(ambianceSfx)
   bgCh.play(bgSfx, -1)

@webiopi.macro
def stopAmbiance():
   if DEBUG:
      print("stop ambiance... ")
   bgCh = pygame.mixer.Channel(1)
   bgCh = pygame.mixer.Channel(1)
   bgCh.stop()

@webiopi.macro
def scream():
   if DEBUG:
      print("screaming... ")
   sfxFg = pygame.mixer.Sound(choice(screams))
   fgCh = pygame.mixer.Channel(2)
   fgCh.play(sfxFg) 
   rest()
   len = int(sfxFg.get_length())
   stare(len/4)
   blink(len/2)
   stare(len/4)

@webiopi.macro
def laugh():
   if DEBUG:
      print("laughing... ")
   sfxFg = pygame.mixer.Sound(choice(laughs))
   fgCh = pygame.mixer.Channel(2)
   fgCh.play(sfxFg)
   rest()
   len = int(sfxFg.get_length())
   stare(len/4)
   blink(len/2)
   stare(len/4)

@webiopi.macro
def moreSounds():
   if DEBUG:
      print("moreSounds... ")
   sfxFg = pygame.mixer.Sound(choice(scarySounds))
   fgCh = pygame.mixer.Channel(2)
   fgCh.play(sfxFg)
   rest()
   len = int(sfxFg.get_length())
   stare(len/4)
   blink(len/2)
   stare(len/4)

