#!/usr/bin/env python3
import serial
from time import sleep,time

def bc_callback(**kargv):
    #print('Barcode: {} {}'.format(kargv['barcode']))
    print(kargv)

class Barcodereader(object):
    def __init__(self, port = '/dev/ttyACM0', timeout=1, callback_fn=None, f=2) -> None:
        self.port = port
        self.timeout = timeout
        self.running = False
        self._scanner = None
        self.error = None
        self._callback_fn = callback_fn
        self._f = f
        self.prev_scan = time() - f
    def start(self) -> None:
        try:
            self._scanner = serial.Serial(port=self.port,timeout=self.timeout)
            #Flush buffer
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
            if len(bc) > 0 and (time()>self.prev_scan+self._f):
                self._cb(barcode = bc, error = self.error, )
                self.prev_scan = time()
        except serial.SerialException as e:
            self.running=False
            self.error = e
            #Callback
            self._cb(barcode = None, error = self.error)

def main():
    bc = Barcodereader(port = '/dev/ttyACM0', timeout=.5, callback_fn=bc_callback, f=5)
    while not bc.running:
        bc.start()
        if bc.error is not None: print(bc.error)
        sleep(2)
    while bc.running:
        bc.next()
        print('.')
        sleep(2)
        
    main()
if __name__ == '__main__':
    main()