#!/usr/bin/env python
import time
import sys
import os
import pygame
from pygame import midi

class _Getch:
	def __init__(self):
		import tty, sys, termios

	def __call__(self):
		import sys, tty, termios
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			ch = sys.stdin.read(1)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ch

def getKey():
	inkey = _Getch()
	import sys
	k=inkey()
	print('key: ', k)

	return k

def print_device_info():
	pygame.midi.init()
	_print_device_info()
	pygame.midi.quit()

def _print_device_info():
	for i in range( pygame.midi.get_count() ):
		r = pygame.midi.get_device_info(i)
		(interf, name, input, output, opened) = r
		in_out = ""
		if input:
			in_out = "(input)"
		if output:
			in_out = "(output)"
		print ("%2i: interface :%s:, name :%s:, opened :%s:	 %s" %
		(i, interf, name, opened, in_out))

#Variables
velocity = 127
instrument = 0
currentPatch = 0
currentBank = 0
player = None

statusFlags = [0, 0, 0, 0, 0, 0, 0, 0, 0];

patchKeyMap = {
	# "left shift":58, 
	"1":1,	"2":2,	"3":3,	"4":4, "5":5, "6":6,  
	"7":7,	"8":8, "9":9	}

bankDeltaMap = {",":-1,	 ".":1
	}

messageMap = {
	# "left shift":58, 
	"caps lock":59, "world 7":57, "tab":58, "1":59, "<":60, "a":61, "z":62, "s":63, "x":64, "d":65, "c":66, "f":67,"v":68, "g":69, "b":70, "h":71,
	"n":72, "j":73, "m":74, "k":75, ",":76, "l":77, ".":78, "world 86":79, "-":80, "world 68":81, "right shift":82, "'":83, 
	"q":60, "2":61, "w":62, "3":63, "4":65, "r":66, "5":67, "t":68, "6":69, "y":70, "7":71, 
	"u":72, "8":73, "i":74, "9":75, "o":76, "0":77, "p":78, "+":79, "world 69":80, "backspace":81, "return":84,

	"[0]":84, "enter":85, "[1]":86, "[2]":87, "[3]":88, "[4]":89, "[5]":90, "[6]":91, "[+]":92, "[7]":93, "[8]":94, "[9]":95, "[/]":96, "[*]":97, "[-]":98
	} 



def keypress():
	global currentPatch
	global currentBank
	global player
    global statusFlags
	key = getKey()
	
	if key is not None:
		print(' key:' + key)
		if bankDeltaMap.get(key,0):
			currentBank += bankDeltaMap.get(key)
			if currentBank < 0:
				currentBank = 0
			currentPatch = 0
			print('Change bank ' + str(currentBank))
		elif patchKeyMap.get(key,0):
			tmp = patchKeyMap.get(key)
			currentPatch = currentBank*10 + tmp
			status = statusFlags[tmp - 1];
			if status == 1:
				statusFlags[tmp - 1] =	0
			else:
				statusFlags[tmp - 1] =	127

			player.write_short(0xb0, currentPatch, statusFlags[tmp - 1])
			print('Change patch ' + str(currentPatch))
		elif messageMap.get(key,0):
			player.note_on(messageMap.get(key) , velocity)
			print('Played note: ', messageMap.get(key))
		elif key == "e":
			print('Stop midi mapper')
			del player
			pygame.midi.quit()
			# pygame.display.quit()
			# client.disconnect('a2j:Midi Through [14] (capture): Midi Through Port-0', 'gx_head_amp:midi_in_1')

			sys.exit(0)
		
		return
	else:
		print('key is none')
		
# Collect events until released		

	
def main():
	global player
	device_id = None
	pygame.init()
	pygame.midi.init()
	_print_device_info()
	if device_id is None:
		port = pygame.midi.get_default_output_id()
	else:
		port = device_id
	
	print ("using output_id :%s:" % port)

	player = pygame.midi.Output(port, 0)
	i = 1
	while True:
		keypress()

main()

