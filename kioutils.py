#!/usr/bin/env python3
#gtts-cli -s --lang en 'Scanner ready' --output scanner_readyEN.mp3
#for f in *.mp3 ; do ffmpeg -i "$f"  "${f%.*}.wav" ; done
from subprocess import check_output
import os
from time import sleep
def speak_ip(ip,lang,dir='') -> None:
    '''
    Speak host's IP address
    '''
    for char in ip:
        f = ('{}/{}_{}.wav'.format(dir,char.replace('.','dot'),lang.upper()))
        try:
            os.system('aplay -q {} 2>&1'.format(f))
        except Exception as e:
            pass

def get_IP() -> None:
    '''
    Get host's IP address
    '''
    try:
        ip = check_output(['hostname', '-I']).decode('utf-8')
        return(ip.strip())
    except:
        return(None)
def speak_status(f,background = True)-> None:
    '''
    Speak status messages
    '''
    if background:
        try:
            os.popen('aplay -q {} 2>&1'.format(f))
        except:
            pass
    else:
        try:
            os.system('aplay -q {} 2>&1'.format(f))
        except Exception as e:
            pass


def main():
    dir = (os.path.dirname(os.path.realpath(__file__)))
    print(get_IP())
    speak_ip(ip=get_IP(),lang='lat',dir=dir)
    speak_status('{}/ready_{}.wav'.format(dir,'LAT'))
    print('{}/{}.wav'.format(dir,'ready_LV'))


if __name__ == '__main__':
    main()