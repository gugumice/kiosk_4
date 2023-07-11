#!/usr/bin/env python3
import configparser
import logging
import os

def read_config(filename):
    '''
    Sets default config values values
    Reads values from config file
    '''
    kiosk_config = {
        'log_file': None,
        'button_panel': False,
        'button_pins': [17,27,22],
        'led_pins': [13,19,26],
        'led_on_time': 3,
        'led_off_time':.5,
        'led_fade_in': .5,
        'led_fade_out': .5,

        'buzzer_pin': 12,
        'default_button' : 0,
        'button_timeout' : 10,
        'melody': ["C4","A4","C4"],
        'sound_interval': .12,
        'languages' : ['LAT','ENG','RUS'],
        'delay':2,

        'bc_reader_port' : '/dev/ttyACM0',
        'bc_timeout' : .5,
        'bc_regex' : '^\d{7,9}#\d{4,5}',

        'host' : '10.100.50.104',
        'httpreq_timeout': 15, 
        'report_delay' : 5,
        'url' : 'http://{}/csp/sarmite/ea.kiosk.pdf.cls?HASH={}&LANG={}',
        'url_test' : 'http://10.100.50.102/sarmite/m5menu.csp',
        'printers':  {"HP": "HP LaserJet Series PCL 6 CUPS"},
        'button_printer_reset' : [1],
        'watchdog_device' : None
    }
    if not os.path.isfile(filename):
        logging.critical("Config file {} does not exist!".format(filename))
        return(None)
    cf = configparser.ConfigParser(allow_no_value=True,
                            converters={'list': lambda x: [int(i.strip()) for i in x.split(',')],
                                        'list_s' : lambda x: [i.strip() for i in x.split(',')]})
    cf.read(filename)
    #Tuple containing load commands
    commands =(
        "kiosk_config['log_file'] = cf.get('INTERFACE','log_file')",
        "kiosk_config['button_panel'] = cf.getboolean('INTERFACE','button_panel')",
        "kiosk_config['button_pins'] = cf.getlist('INTERFACE','button_pins')",
        "kiosk_config['led_pins'] = cf.getlist('INTERFACE','led_pins')",
        "kiosk_config['led_on_time'] = cf.getfloat('INTERFACE','led_on_time')",
        "kiosk_config['led_off_time'] = cf.getfloat('INTERFACE','led_oFF_time')",
        "kiosk_config['led_fade_in'] = cf.getfloat('INTERFACE','led_fade_in')",
        "kiosk_config['led_fade_out'] = cf.getfloat('INTERFACE','led_fade_out')",
        "kiosk_config['buzzer_pin'] = cf.getint('INTERFACE','buzzer_pin')",
        "kiosk_config['default_button'] = cf.getint('INTERFACE','default_button')",
        "kiosk_config['button_timeout'] = cf.getint('INTERFACE','button_timeout')",
        "kiosk_config['melody'] = cf.getlist_s('INTERFACE','melody')",
        "kiosk_config['sound_interval'] = cf.getfloat('INTERFACE','sound_interval')",
        "kiosk_config['languages'] = cf.getlist_s('INTERFACE','languages')",
        "kiosk_config['delay'] = cf.getfloat('INTERFACE','delay')",

        "kiosk_config['bc_reader_port'] = cf.get('BARCODE','bc_reader_port')",
        "kiosk_config['bc_timeout'] = cf.getfloat('BARCODE','bc_timeout')",
        "kiosk_config['bc_regex'] = r'{}'.format(cf.get('BARCODE','bc_regex'))",

        "kiosk_config['host'] = cf.get('REPORT','host')",
        "kiosk_config['httpreq_timeout'] = cf.getint('REPORT','httpreq_timeout')",
        "kiosk_config['report_delay'] = cf.getint('REPORT','report_delay')",
        "kiosk_config['url'] = cf.get('REPORT','url')",
        "kiosk_config['url_test'] = cf.get('REPORT','url_test')",
        "kiosk_config['button_printer_reset'] = cf.getlist('REPORT','button_printer_reset')",
        "kiosk_config['printers'] = cf.get('REPORT','printers')",

        "kiosk_config['watchdog_device'] = cf.get('WATCHDOG','watchdog_device')"
        )
    for c in commands:
        try:
            #print('Executing: {}'.format(c))
            exec(c)
        except configparser.Error as e:
            logging.error(e)
    return(kiosk_config)

def main():
    f = '{}/{}'.format(os.getcwd(),'kiosk.ini')
    cfg = read_config(f)
    print(cfg)

if __name__ == '__main__':
    main()
