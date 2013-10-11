#!/usr/bin/env python

# Code to drive the GPIO and to animate a skull for halloween
# Halloween head is a class with various functions to based on GPIO IO
#
# options to make the eyes blink, stare, and rest
# options to play various sound fx
# 'scary' ambiance in the background
# refactor to use pygame to play sounds simultaneously

import RPi.GPIO as GPIO, time, os, subprocess, threading
import pygame.mixer
from random import choice

GPIO.setmode(GPIO.BCM)

SLEEP_TIME = 1
BLINK_TIME = 0.25
GREEN_LED = 17
RED_LED = 22
LAUGH_LEN = 4.0
SCREAM_LEN = 14.0
SHORTSCREAM_LEN = 3.0
DANCE_LEN = 28.0

DEBUG = True
AMBIANCE = True

class HalloweenHead:

   castleSfx = "../sounds/CastleThunder.wav"
   ambianceSfx = "../sounds/DemonZombieAmbiance-SoundBible.com-1821142973.wav"
   laughSfx = "../sounds/evillaugh5.wav"
   screamSfx = "../sounds/scream7.wav"
   roarSfx = "../sounds/Godzilla_Roar-Marc-1912765428.wav"

   screams = ["../sounds/WilhelmScream.wav", "../sounds/Scream.wav", "../sounds/scream7.wav"] 
   laughs = ["../sounds/evillaugh5.wav", "../sounds/laugh.wav"] 

   def __init__(self):
      self.setup()

   def setup(self):
      if DEBUG: print("setting up")
      GPIO.setup(GREEN_LED, GPIO.OUT)
      GPIO.setup(RED_LED, GPIO.OUT)
      self.left_eye = False
      self.right_eye = False
      pygame.mixer.init(44100, -16, 1, 1024)
      self.bgCh = pygame.mixer.Channel(1)
      self.fgCh = pygame.mixer.Channel(2)

   def set_leds(self, l, r):
      if DEBUG: print("set_leds %r %r" % (l, r))
      GPIO.output(GREEN_LED, l)
      GPIO.output(RED_LED, r)

   def blink(self, secs):
      if DEBUG: print("blink...")
      for x in range(0, int(secs*2)):
         self.set_leds(not self.left_eye, not self.right_eye)
         time.sleep(BLINK_TIME)
         self.set_leds(self.left_eye, self.right_eye)
         time.sleep(BLINK_TIME)

   def crazy_blink(self, secs):
      if DEBUG: print("crazy_blink...")
      for x in range(0, int(secs*2)):
         self.set_leds(self.left_eye, not self.right_eye)
         time.sleep(BLINK_TIME)
         self.set_leds(not self.left_eye, self.right_eye)
         time.sleep(BLINK_TIME)
      self.set_leds(self.left_eye, self.right_eye)

   def stare(self, secs=None):
      #if DEBUG: print("stare... %r", % secs)
      if secs is not None:
         if DEBUG: print("setting stare timer %r ..." % int(secs))
         t = threading.Timer(int(secs), self.rest)
         t.start()
      self.left_eye = True
      self.right_eye = True
      self.set_leds(self.left_eye, self.right_eye)
      
   def rest(self):
      if DEBUG: print("rest...")
      self.left_eye = False
      self.right_eye = False
      self.set_leds(self.left_eye, self.right_eye)

   def ambiance(self):
      if not AMBIANCE: return
      sfxBg = pygame.mixer.Sound(self.ambianceSfx)
      self.bgCh.play(sfxBg, -1)

   def stop_ambiance(self):
      if not AMBIANCE: return
      self.bgCh.stop()

   def scream(self):
      if DEBUG: print("screaming...")
      sfxFg = pygame.mixer.Sound(choice(self.screams))
      self.fgCh.play(sfxFg)
      self.rest()
      len = int(sfxFg.get_length())
      self.stare(len/4)
      self.blink(len/2)
      self.stare(len/4)

   def shortscream(self):
      if DEBUG: print("shortscreaming...")
      sfxFg = pygame.mixer.Sound(self.roarSfx)
      if DEBUG: print("sound: %r" % sfxFg)
      self.fgCh.play(sfxFg)
      self.stare(SHORTSCREAM_LEN)

   def laugh(self):
      if DEBUG: print("laughing...")
      sfxFg = pygame.mixer.Sound(self.laughSfx)
      self.fgCh.play(sfxFg)
      self.blink(LAUGH_LEN+1)

   def dance(self):
      if DEBUG: print("dancing...")
      sfxFg = pygame.mixer.Sound(self.danceSfx)
      if DEBUG: print("sound: %r" % sfxFg)
      self.fgCh.play(sfxFg)
      self.rest()
      time.sleep(2)
      self.stare(2)
      self.stare(2)
      self.crazy_blink(int(DANCE_LEN/5))

   def testPygame(self):
      if DEBUG: print("mixer ok, trying channel")
      sfxBg = pygame.mixer.Sound(self.ambianceSfx)
      self.bgCh.play(sfxBg, -1)
      

   def cleanup(self):
      if DEBUG: print("head cleaning...")
      pygame.mixer.stop()
      GPIO.cleanup() 

