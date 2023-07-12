#!/usr/bin/env python3

import argparse
import json
import logging
import os
import re
import sys
import time

import kioconfig
import kiogpio
import kioprint
import kioreport
import kioutils
from kiobcr import Barcodereader

# Global vars & constants
wdObj = None
config = {}
kiosk_bcr = None
kiosk_leds = None
kiosk_buttons = None
kiosk_printer = None
app_dir = os.path.dirname(os.path.realpath(__file__))
lang = None

def make_URL(bar_code,lang):
    '''
    Accepts: request barcode, language
    Returns url for HTTP request
    '''

    #Remove bc type prefix if present
    if not bar_code[0].isnumeric():
        bar_code=bar_code[1:]
    req_code = re.search(config['bc_regex'],bar_code)
    if req_code is not None:
        req_code = req_code.group(0)
        req_code = req_code.replace('#','%23')
        return(config['url'].format(config['host'],req_code,lang))

    return(None)

def bcr_callback(**kargv):
    '''
    Callback for barcode reader
    Varifies barcode
    Prints testing report 
    '''
    global lang
    global config
    global app_dir
    global kiosk_printer
    global kiosk_leds
    global kiosk_buttons
    global kiosk_bcr
 
    def reset_button_panel():
        kiosk_leds.off()
        kiosk_leds.blink(leds=[active_button],n=None,on_time=config['led_on_time'],off_time=config['led_off_time'],
            fade_in_time=config['led_fade_in'],fade_out_time=config['led_fade_out'])   
    active_button = kiosk_buttons.activeButton
    #Prevent repeated scans 
    report_URL = make_URL(kargv['barcode'],lang)

    if report_URL is None:
        if config['button_panel']:
            kiosk_leds.pulse()
            kioutils.speak_status('{}/error-attn.wav'.format(app_dir),background=False)
            kioutils.speak_status('{}/barcode_invalid{}.wav'.format(app_dir,lang))
            kiosk_buttons.beep(n=2,background=False)
            reset_button_panel()
        logging.error('{} - invalid barcode'.format(kargv['barcode']))
        return

    report_status,report_file = kioreport.get_report(report_URL,config['httpreq_timeout'])
    #Request valid but testing not finished
    if report_status == 404:
        if config['button_panel']:
            kiosk_leds.pulse()
            kioutils.speak_status('{}/attn.wav'.format(app_dir),background=False)
            kioutils.speak_status('{}/not_ready{}.wav'.format(app_dir,lang))
            kiosk_buttons.beep(n=1,background=False)
            reset_button_panel()
        logging.info('{} - Testing not finished'.format(kargv['barcode']))
        return

    #print(report_status,report_file,config['httpreq_timeout'])
    #Everything ok - go on with peinting
    if report_status == 200 and report_file is not None:
        if config['button_panel']:
            kiosk_leds.pulse()
            kioutils.speak_status('{}/attn.wav'.format(app_dir),background=False)
            kioutils.speak_status('{}/start_print{}.wav'.format(app_dir,lang))
        #Cancel all pending jobs if present for privacy 
        try:
            kiosk_printer.cancelAllJobs(kiosk_printer.name)
        except Exception as e:
            logging.error(e)
        job_id = None
        try:
            #print('Printing....')
            job_id = kiosk_printer.printFile(printer=kiosk_printer.name,filename = report_file,title = 'Report',options ={'print-color-mode': 'monochrome'})
            logging.info('Report: {}, jobID: {}, lang: {}, http resp.: {}, sent to {}'.format(kargv['barcode'],job_id,lang, report_status, kiosk_printer.name))
        except Exception as e:
            logging.error(e)
        logging.info('{} - Report sent to printer, {}'.format(kargv['barcode'],lang))

        #Blink lights when printing
        time.sleep(config['report_delay'])
        if config['button_panel']:
            kioutils.speak_status('{}/end_print{}.wav'.format(app_dir,lang))
            kiosk_buttons.beep(n=1,background=True)
            reset_button_panel()

    #Remove temporary PDF
    try:
        os.remove(report_file)
    except FileNotFoundError:
        pass


def kio_init():
    """
    Init & test peripherials for kiosk operation
    """
    global config
    global kiosk_bcr
    global kiosk_leds
    global kiosk_buttons
    global wdObj
    global kiosk_printer
    global app_dir

    kiosk_leds = kiogpio.kioskPWMLeds(pins=config["led_pins"])
    kiosk_buttons = kiogpio.kioskButtons(
        pins=config["button_pins"],
        default=config["default_button"],
        timeout=config["button_timeout"],
    )

    kiosk_leds.on()
    time.sleep(config["delay"])
    # ____Init barcode scanner, keep on until success_____
    kiosk_leds.pulse([2], fade_in_time=0.1, fade_out_time=0.1, n=None)
    kiosk_bcr = Barcodereader(
        port=config["bc_reader_port"], timeout=config["bc_timeout"], callback_fn = bcr_callback, f = config['report_delay']/2
    )
    while not kiosk_bcr.running:
        kiosk_bcr.start()
        time.sleep(config["delay"])
    kiosk_leds.off(leds=[2])
    logging.info(
        "BCR on {} timeout {}".format(config["bc_reader_port"], config["bc_timeout"])
    )
    # ___BCR END ________
    # Init printer
    kiosk_leds.pulse([1], fade_in_time=0.1, fade_out_time=0.1, n=None)
    # Beep & delay to allow doing reset
    if config['button_panel']:
        kiosk_buttons.beep(background=False)
    time.sleep(config["delay"])

    kiosk_printer = kioprint.kioPrinter(json.loads(config["printers"]), testpage=True)
    kiosk_printer.start()
    # Reset printsystem if reset button is pressed
    if kiosk_buttons.pressed() and kiosk_buttons.pressedButtons == [1]:
        logging.info("User printsystem reset initiated")
        kiosk_printer.deleteAllPrinters()
        kiosk_printer.addKioPrinter()
    # Start printsystem
    while not kiosk_printer.running:
        kiosk_printer.start()
        time.sleep(config["delay"])
    kiosk_leds.off(leds=[1])
    logging.info("Printer {} on CUPS".format(kiosk_printer.name))
    # ___PRINTER END ________

    # Init connection with, host check foe valid http response
    logging.info("IP address: {}".format(kioutils.get_IP()))
    kiosk_leds.pulse([0], fade_in_time=0.1, fade_out_time=0.1, n=None)
    kioutils.speak_ip(ip=kioutils.get_IP(),lang='lat',dir=app_dir)

    while not kioreport.connection_ok(config['url_test']):
        time.sleep(config['delay'])
    kiosk_leds.off(leds=[0])
    kioutils.speak_status('{}/ready_{}.wav'.format(app_dir,config['languages'][config['default_button']]))

    # Init Watchdog
    if config["watchdog_device"] is not None:
        try:
            wdObj = open(config["watchdog_device"], "w")
            logging.info("Watchdog enabled on {}".format(config["watchdog_device"]))
        except Exception as e:
            logging.error(e)
    else:
        logging.info("Watchdog disabled")

def kio_run():
    """
    Run kiosk
    """
    global config
    global kiosk_bcr
    global kiosk_leds
    global kiosk_buttons
    global wdObj
    global kiosk_printer
    global app_dir
    global lang
    
    lang = config['languages'][config['default_button']]
    kiosk_leds.activeButton = config['default_button']
    #
    if config['button_panel']:
        kiosk_leds.blink(leds=[kiosk_leds.activeButton],n=None,on_time=config['led_on_time'],off_time=config['led_off_time'],
            fade_in_time=config['led_fade_in'],fade_out_time=config['led_fade_out'])
    #========= Main loop start==========
    while kiosk_bcr.running:
        #Pat watchdog
        if wdObj is not None:
            print('1',file = wdObj, flush = True)
        
        #Check if panel is enabled, button is pressed or timed-out and set chosen language
        if config['button_panel'] and kiosk_buttons.pressed():
            kiosk_leds.off()
            #Allow LED driver threads to finish
            time.sleep(.5)
            kiosk_leds.blink(leds=[kiosk_buttons.activeButton],n=None,on_time=config['led_on_time'],off_time=config['led_off_time'],
                fade_in_time=config['led_fade_in'],fade_out_time=config['led_fade_out'])
            lang=config['languages'][kiosk_buttons.activeButton]
            kioutils.speak_status('{}/lang_{}.wav'.format(app_dir,lang.upper()))
            logging.debug('{} selected'.format(lang))
        #Read scanner
        kiosk_bcr.next()

def main():
    run_directory = os.path.dirname(os.path.realpath(__file__))
    parser = argparse.ArgumentParser(description="EGL testing report kiosk")
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        metavar="file",
        help="Name config file. Default: config.ini",
        default="{}/kiosk.ini".format(run_directory),
    )
    args = parser.parse_args()
    # Read from config file
    global config
    config = kioconfig.read_config(args.config)
    #logging.info('Logfile: ',config["log_file"])
    if config["log_file"] is None:
        logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.DEBUG)
    else:
        logging.basicConfig(
            format="%(asctime)s - %(message)s",
            filename=config["log_file"],
            filemode="w",
            level=logging.INFO,
        )
    kio_init()
    logging.info('Starting main loop...')
    if config['button_panel']:
        kiosk_buttons.beep(n=3,background=True)
    kio_run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        if wdObj is not None:
            print("V", file=wdObj, flush=True)
        print("\nExiting...")
        sys.exit()
