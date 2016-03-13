import websockets
import asyncio
import time
import json
from hk_usb_io import *

usb = init()

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

RA5 = sfr_get_regbit(usb, ior['PORTA'], 5)
RA1 = sfr_get_regbit(usb, ior['PORTA'], 1)
RA4 = sfr_get_regbit(usb, ior['PORTA'], 4)
RB4 = sfr_get_regbit(usb, ior['PORTB'], 4)


class Handler(object):

    def __init__(self):
        self.serv = websockets.serve(self.handler, 'localhost', 8765)
        self.ramp = '0'
        self.velocity1 = '0'
        self.velocity2 = '0'
        self.dwell = '0'
        self.limit_upper = '0'
        self.limit_lower = '0'

    async def xy(self):
        try:
            if RA5 == 0:
                ser_puts(usb, "ZA"+self.ramp)
            time.sleep(0.01)
            if RA5 == 0:
                ser_puts(usb, "ZD"+self.velocity1)
            time.sleep(0.01)
            if RA5 == 0:
                ser_puts(usb, "ZF"+self.velocity2)
            time.sleep(0.01)
            if RA5 == 0:
                ser_puts(usb, "ZB"+self.limit_upper)
            time.sleep(0.01)
            if RA5 == 0:
                ser_puts(usb, "ZE"+self.limit_lower)
            time.sleep(0.01)
            if RA5 == 0 and self.dwell != '0':
                ser_puts(usb, "ZJ"+self.dwell)
            time.sleep(0.01)
            if RA5 == 0:
                ser_puts(usb, "H")
            sfr_set_regbit(usb, ior['TRISA'],  5, 0)
        except Exception as e:
            print(e)

    async def handler(self, websocket, path):
        x = 0
        while True:
            check_first_click = await websocket.recv()
            if check_first_click == "start":
                while True:
                    b = adc_ra0(usb)
                    tasks = [asyncio.ensure_future(websocket.recv()), asyncio.ensure_future(Handler.xy(self))]
                    done, panding = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                    if tasks[0] in done:
                        if tasks[0].result() == "stop":
                            break
                    else:
                        tasks[0].cancel()

                    if tasks[1] in done:
                        mess = tasks[1].result()
                        await websocket.send(str(mess))
                        await asyncio.sleep(0.1)
                    else:
                        tasks[1].cancel()
                    x += 1


loop = asyncio.get_event_loop()
loop.run_until_complete(Handler())
loop.run_forever()