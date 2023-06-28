#!/usr/bin/env python3
import requests
import tempfile

def connection_ok(url) -> None:
    '''
    Test connection to host
    '''
    try:
        requests.head(url,timeout=10)
        return(True)
    except requests.ConnectionError:
        return(False)

def get_report(url, timeout = 10):
    '''
    Gets testing report from server, saves it to temporary file
    Returns status and link to temporary file
    '''
    req = requests.get(url, timeout = timeout)
    #Check req and it's type
    if req.ok and req.headers.get('Content-Type') == 'application/pdf':
        #Create tmp file for CUPS
        temp_file = tempfile.NamedTemporaryFile(prefix='kio_',suffix='.pdf', delete=False,)
        #Write content to tmp file
        with open(temp_file.name, 'wb') as tf:
            tf.write(req.content)
        return(req.status_code, temp_file.name)
    return(req.status_code,None)
    
def main(): 
    # driven code
    url = 'http://10.100.50.104/csp/sarmite/ea.kiosk.pdf.cls?HASH=13621914%238444&LANG=RUS'
    url_test = 'http://10.100.50.102/sarmite/m5menu.csp'
    #url = "https://www.geeksforgeeks.org/"
    
    print(get_report(url, timeout = 5))
    print(connection_ok(url_test))

if __name__ == '__main__':
    main()