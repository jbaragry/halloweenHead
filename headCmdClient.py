#!/usr/bin/env python

# a dumb cmdline client to drive the halloweenhead
# menu:
# options to make the eyes blink, stare, and rest
# options to play various sound fx
# 'scary' ambiance in the background
#     note: because I haven't got dmix working with the audio out
#      I need to stop and start the background fx for every foreground fx

import time
from halloweenHead import HalloweenHead


DEBUG = True
SLEEP_TIME = 1


# client
head = HalloweenHead()

def head_menu():
   print("what do you want to do?")
   print("\tStare [s]")
   print("\tRest [r]")
   print("\tBlink [b]")
   print("\tCrazyBlink [n]")
   print("\tScream [c]")
   print("\tShortScream [x]")
   print("\tLaugh [l]")
   print("\tTest Sound [t]")
   print("\tQuit [q]")
   menu_item = raw_input("\t> ")
   if DEBUG: print("menu_item %r" % menu_item)
   return menu_item

try:

   head.ambiance()
   while True:
      cmd = head_menu()
      if cmd == 'b':
         head.blink(2)
      if cmd == 'n':
         head.crazy_blink(2)
      elif cmd == 'r':
         head.rest()
      elif cmd == 's':
         head.stare()
      elif cmd == 'l':
         head.laugh()
      elif cmd == 'c':
         head.scream()
      elif cmd == 'x':
         head.shortscream()
      elif cmd == 'd':
         head.dance()
      elif cmd == 't':
         head.testPygame()
      elif cmd == 'q':
         head.stop_ambiance()
         raise KeyboardInterrupt
      else:
         print("CTRL-C to quit")
      time.sleep(SLEEP_TIME * 2)          


except KeyboardInterrupt:
    head.cleanup()
    head.stop_ambiance()
