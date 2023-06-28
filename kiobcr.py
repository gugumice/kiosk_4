#!/usr/bin/env python3
import serial
from time import sleep

def bc_callback(**kargv):
    print('Barcode: {} {}'.format(kargv['barcode']))

class Barcodereader(object):
    def __init__(self, port = '/dev/ttyACM0', timeout=1, callback_fn=None) -> None:
        self.port = port
        self.timeout = timeout
        self.running = False
        self._scanner = None
        self.error = None
        self._callback_fn = callback_fn
    def start(self) -> None:
        try:
            self._scanner = serial.Serial(port=self.port,timeout=self.timeout)
            self.running = True
        except serial.SerialException as e:
            self.error = e

    def _cb(self, *args, **kwargs):
        #Call callback fn
        if self._callback_fn:
            return(self._callback_fn(*args,**kwargs))
        
    def next(self):
        try:
            bc = self._scanner.readline().decode('ascii').rstrip('\r\n')
            self.error = None
            #Callback
            if len(bc) > 0:
                self._cb(barcode = bc, error = self.error)
        except serial.SerialException as e:
            self.running=False
            self.error = e
            #Callback
            self._cb(barcode = None, error = self.error)

def main():
    bc = Barcodereader(port = '/dev/ttyACM0', timeout=1, callback_fn=bc_callback)
    while not bc.running:
        bc.start()
        if bc.error is not None: print(bc.error)
        sleep(2)
    while bc.running:
        bc.next()
if __name__ == '__main__':
    main()