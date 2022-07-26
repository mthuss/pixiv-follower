#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time

from pixivpy3 import AppPixivAPI, PixivError

sys.dont_write_bytecode = True


# get your refresh_token, and replace _REFRESH_TOKEN
#  https://github.com/upbit/pixivpy/issues/158#issuecomment-778919084
_REFRESH_TOKEN = "TOKEN"
_TEST_WRITE = False

# If a special network environment is meet, please configure requests as you need.
# Otherwise, just keep it empty.
_REQUESTS_KWARGS = {
    # 'proxies': {
    #     'https': 'http://127.0.0.1:1087',
    # },
    # 'verify': False,       # PAPI use https, an easy way is disable requests SSL verify
}

def main():
    # app-api
    aapi = AppPixivAPI(**_REQUESTS_KWARGS)

    filename = input("Name of the file containing the IDs: ")

    _e = None
    for _ in range(3):
        try:
            aapi.auth(refresh_token=_REFRESH_TOKEN)
            break
        except PixivError as e:
            _e = e
            print(e)
            time.sleep(10)
    else:  # failed 3 times
        raise _e

    f = open(filename)
    log = open("log.txt","a+")

    for line in f:
        log.seek(0, os.SEEK_SET)
        if(line not in log.read()):
            timeout = False;
            ParsedJSON = aapi.user_follow_add(int(line),restrict="private")
#            print(ParsedJSON)
            if('error' in ParsedJSON and 'user_message' in ParsedJSON['error'] and 'restricted' in ParsedJSON['error']['user_message']): 
                 print("Access Restricted! Try again later")
                 exit(0);
            elif('error' in ParsedJSON and 'message' in ParsedJSON['error'] and 'Rate Limit' in ParsedJSON['error']['message']):
                 print("Timeout! Trying again soon")
                 timeout = True
    
            timeouttime = 0
            while(timeout):
                ParsedJSON = aapi.user_follow_add(int(line),restrict="private")
                time.sleep(10)
                if('error' in ParsedJSON and 'message' in ParsedJSON['error'] and 'Rate Limit' in ParsedJSON['error']['message']): 
                   timeouttime+=10
                else: 
                    print("Timeout took " + str(timeouttime) + " seconds")
                    timeout = False
    
            print("Followed " + line)

            log.seek(0, os.SEEK_END)
            print(int(line),file=log)
    
            #Waits a few seconds before each request to avoid getting rate limited
            #Doesn't seem to work all that well though...
            time.sleep(10)
    f.close()



if __name__ == "__main__":
    main()
