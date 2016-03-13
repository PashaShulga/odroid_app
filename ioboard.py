#!/usr/bin/python
# Markham Thomas  2/24/2013
#
# Demo some of the HK_USB_IO ROM functions
#
#   Refer to the other python programs for more
# in depth examples
from hk_usb_io import *		# import interface module
import sys
import time

usb = init()			# init the USB IO board


ior = {'ANSELA': 0x5b, 'ANSELB' : 0x5c ,'ANSELC' : 0x5d, 'ANSELD' : 0x5e, 'ANSELE' : 0x5f,
	   'PORTA' : 0x80, 'PORTB' :  0x81, 'PORTC'  : 0x82, 'PORTD'  : 0x83, 'PORTE'  : 0x84,
	  'TRISA' : 0x92, 'TRISB' :  0x93, 'TRISC'  : 0x94, 'TRISD'  : 0x95, 'TRISE'  : 0x96,
	  'LATA'  : 0x89, 'LATB'  :  0x8a, 'LATC'   : 0x8b, 'LATD'   : 0x8c, 'LATE'   : 0x8d }


sfr_set_regbit(usb, ior['ANSELA'], 5, 0)	# RA5 is digital
sfr_set_regbit(usb, ior['ANSELA'], 4, 0)	# RA4 is digital
sfr_set_regbit(usb, ior['ANSELA'], 1, 0)	# RA1 is digital
sfr_set_regbit(usb, ior['ANSELB'], 4, 0)	# RB4 is digital

sfr_set_regbit(usb, ior['TRISA'],  5, 0)	# RA5 pin 0 - output, 1 - input
sfr_set_regbit(usb, ior['TRISA'],  4, 1)	# RA4 pin 0 - output, 1 - input
sfr_set_regbit(usb, ior['TRISA'],  1, 1)	# RA1 pin 0 - output, 1 - input
sfr_set_regbit(usb, ior['TRISB'],  4, 0)	# RA4 pin 0 - output, 1 - input

a = sfr_get_regbit(usb, ior['PORTA'],  1)	# get the value
print("Pin value:", a)

ser_putc(usb, "Zgityug9uogoyuhoihoouD")