#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=I0011,C0103,C0111

from __future__ import print_function
from time import time, sleep
import requests

from utils import APP_KEY, headers, getSign

_logger = None

def setLogger(logger):
    global _logger
    _logger = logger

def main(ACCESS_KEY):
    errCount = 0
    for _ in range(32):
        params = {'access_key': ACCESS_KEY, 'appkey': APP_KEY, 'actionKey': 'appkey', 'build': '5370000', 'channel': 'bilih5', 'device': 'android', 'mobi_app': 'android', 'platform': 'android'}
        params['ts'] = str(int(time()))
        params['sign'] = getSign(params)
        r = requests.get('https://api.live.bilibili.com/mobile/freeSilverCurrentTask',
                         params=params, headers=headers) # or 'https://api.live.bilibili.com/lottery/v1/SilverBox/getCurrentTask'
        _logger.debug(r.text)
        res = r.json()
        if res['code'] == 0:
            wait = res['data']['time_end'] - time() + 5

            if wait > 0:
                _logger.info('Waiting for %d seconds' % wait)
                sleep(wait)

            params['time_start'] = res['data']['time_start']
            params['time_end'] = res['data']['time_end']
            params.pop('sign')
            params['ts'] = str(int(time()))
            params['sign'] = getSign(params)
            r = requests.get('https://api.live.bilibili.com/mobile/freeSilverAward',
                             params=params, headers=headers)
            _logger.debug(r.text)
            j = r.json()
            if j['code'] != 0:
                errCount += 1
                _logger.info(res['message'])
                sleep(5)
        else:
            errCount += 1
            _logger.error('freeSilverCurrentTask returned error! Error message:' + res['message'])
            if res['code'] == -10017:
                return
            if res['code'] == -101 or json['code'] == -500:  # Not login
                return 1 # Restart
            sleep(5)

        if errCount >= 5:
            return

if __name__ == '__main__':
    from logger import getLogger
    setLogger(getLogger())
    main('ACCESS_KEY')
