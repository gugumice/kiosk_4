#!/usr/bin/env python3
from time import sleep, time

from gpiozero import LED, PWMLED, TonalBuzzer, Button
from gpiozero.tones import Tone
import threading

class kioskPWMLeds(object):
    '''
    Class for button panel PWMleds
    "leds' argument list or int
    '''
    def __init__(self, pins = [13,19,26]):
        self._leds=[]
        for p in pins:
            self._leds.append(PWMLED(p))
        self._c=len(self._leds)

    def on(self,leds=None):
    
        if leds is None:
            for i in range(0,self._c):
                self._leds[i].on()
        else:
            try:
                for i in leds:
                    self._leds[i].on()
            except TypeError:
                self._leds[leds].on()

    def off(self,leds=None):
        if leds is None:
            for i in range(0,self._c):
                self._leds[i].off()
        else:
            try:
                for i in leds:
                    self._leds[i].off()
            except TypeError:
                self._leds[leds].off()

    def blink(self, leds = None, on_time=1, off_time=1, fade_in_time=0, fade_out_time=0, n=1, background=True):
        if leds is None:
            for i in range(0,self._c):
                self._leds[i].blink(on_time=on_time, off_time=off_time, fade_in_time=fade_in_time, fade_out_time=fade_out_time, n=n, background=background)
        else:
            try:
                for i in leds:
                    self._leds[i].blink(on_time=on_time, off_time=off_time, fade_in_time=fade_in_time, fade_out_time=fade_out_time, n=n, background=background)
            except TypeError:
                self._leds[leds].blink(on_time=on_time, off_time=off_time, fade_in_time=fade_in_time, fade_out_time=fade_out_time, n=n, background=background)

    def pulse(self,leds=None,fade_in_time=1,fade_out_time=1,n=None):
        if leds is None:
            for i in range(0,self._c):
                self._leds[i].pulse(fade_in_time=fade_in_time,fade_out_time=fade_out_time,n=n, background = True)
        else:
            try:
                for i in leds:
                    self._leds[i].pulse(fade_in_time=fade_in_time,fade_out_time=fade_out_time,n=n, background = True)
            except TypeError:
                self._leds[leds].pulse(fade_in_time=fade_in_time,fade_out_time=fade_out_time,n=n, background = True)
    
    def wave(self, interval=.1,n=1,background=True):
        if background is False:
            self._wave(interval=interval, n=n)
        else:
            t = threading.Thread(target=self._wave, kwargs={'interval': interval,'n':n})
            t.start()

    def _wave(self,interval=.1,n=5):
        for num_cycles in range(0,n):
            for i in range(0,self._c):
                self._leds[i].on()
                sleep(interval)
            for i in reversed(range(0,self._c)):
                self._leds[i].off()
                sleep(interval)
class kioskLeds(object):
    '''
    Class for button panel LEDs
    '''
    def __init__(self, pins = [13,19,26]):
        self._leds=[]
        for p in pins:
            self._leds.append(LED(p))
        self._c=len(self._leds)

    def on(self,leds=None):
        if leds is None:
            for i in range(0,self._c):
                self._leds[i].on()
        else:
            try:
                for i in leds:
                    self._leds[i].on()
            except TypeError:
                self.leds.on(leds)

    def off(self,leds=None):
        if leds is None:
            for i in range(0,self._c):
                self._leds[i].off()
        else:
            try:
                for i in leds:
                    self._leds[i].off()
            except TypeError:
                self._leds[leds].off()
    def blink(self, leds = None, on_time=1, off_time=1, n=1, background=True):
        if leds is None:
            for i in range(0,self._c):
                self._leds[i].blink(on_time=on_time, off_time=off_time, n=n, background=background)
        else:
            try:
                for i in leds:
                    self._leds[i].blink(on_time=on_time, off_time=off_time,  n=n, background=background)
            except TypeError:
                     self._leds[leds].blink(on_time=on_time, off_time=off_time,  n=n, background=background)
    
    def wave(self, interval=.1,n=1,background=True):
        if background is False:
            self._wave(interval=interval, n=n)
        else:
            t = threading.Thread(target=self._wave, kwargs={'interval': interval,'n':n})
            t.start()

    def _wave(self,interval=.1,n=1):
        for num_cycles in range(0,n):
            for i in range(0,self._c):
                self._leds[i].on()
                sleep(interval)
            for i in reversed(range(0,self._c)):
                self._leds[i].off()
                sleep(interval)

class kioskButtons(object):
    '''
    class for kiosk panel buttons
    '''
    def __init__(self,pins=[17,27,22], default = 0, timeout =10, sound=True, bounce_time=.1, buzzer = 12, melody = ["C4","A4","C4"], interval=.1):
        self._bttns = []
        self._snd=sound
        self._melody=melody
        self._interval=interval
        self._tb=TonalBuzzer(buzzer)
        self._pressedTime=time()
        self._timeout=timeout
        self.pressedButtons=[]
        self.defaultButton=default
        self.activeButton=default
        for b in pins:
            self._bttns.append(Button(b,bounce_time=bounce_time))
        self._c = len(self._bttns)
    
    def timedOut(self):
        '''
        Checks if timout is exceeded
        '''
        return(time()-self._pressedTime>self._timeout)

    def beep(self,n=1,background=True):
        '''
        Beeps piezo buzzer
        '''
        if not background:
            self._beep(n)
        else:
            t = threading.Thread(target=self._beep,args=(n,))
            t.start()
    def _beep(self,n):
        for num_cycles in range(0,n):
            for n in self._melody:
                self._tb.play(Tone(n))
                sleep(self._interval)
            self._tb.stop()
            sleep(self._interval)
        
    def pressed(self):
        '''
        Checks with buttons are pressed and stores their index
        Returns Bool
        '''
        self.pressedButtons=[]
        for i in range(0,self._c):
            if self._bttns[i].is_pressed:
                self.pressedButtons.append(i)
        if len(self.pressedButtons)>0:
            self._pressedTime=time()
            self.activeButton=self.pressedButtons[0]
            if self._snd:
                self.beep()
        else:
            if self.timedOut() and self.activeButton != self.defaultButton:
                self.activeButton = self.defaultButton
                if self._snd:
                    self.beep()
                self.pressedButtons.append(self.activeButton)
        return(True if len(self.pressedButtons)>0 else False)

def callback_test(*argsv,**kwargsv):
    print('Buttons: {}'.format(kwargsv['buttons']))
    kiosk_leds = kioskPWMLeds(pins=[13,19,26])
    kiosk_leds.on(kwargsv['buttons'])
    sleep(2)
    kiosk_leds.off()
    kiosk_leds=None

class kioskButtonsCB(kioskButtons):
    def __init__(self, callback_fn, pins=[17, 27, 22], default=0, timeout=10, sound=True, bounce_time=0.1, buzzer=12, melody=["C4", "A4", "C4"], interval=0.1):
        super().__init__(pins, default, timeout, sound, bounce_time, buzzer, melody, interval)
        self._callback_fn = callback_fn
    def _cb(self, *args, **kwargs):
        #Call callback fn
        if self._callback_fn:
            return(self._callback_fn(*args,**kwargs))
    def next(self):
        '''
        Checks with buttons are pressed and stores their index
        Returns Bool
        '''
        self.pressedButtons=[]
        for i in range(0,self._c):
            if self._bttns[i].is_pressed:
                self.pressedButtons.append(i)
        if len(self.pressedButtons)>0:
            self._pressedTime=time()
            self.activeButton=self.pressedButtons[0]
            if self._snd:
                self.beep()
        else:
            if self.timedOut() and self.activeButton != self.defaultButton:
                self.activeButton = self.defaultButton
                if self._snd:
                    self.beep()
                self.pressedButtons.append(self.activeButton)
        if len(self.pressedButtons)>0:
        
            self._cb(buttons = self.pressedButtons)

def main():
    l = kioskLeds([13,19,26])
    l.on()
    sleep(1)
    for i in range(0,l._c):
        l.off(i)
        sleep(1)
    l = None
    b = kioskButtonsCB(callback_test)
    while True:
        b.next()
        sleep(.5)
if __name__ == '__main__':
    main()