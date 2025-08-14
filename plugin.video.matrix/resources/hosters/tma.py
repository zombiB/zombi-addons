#-*- coding: utf-8 -*-

import base64
import requests
from resources.hosters.hoster import iHoster

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'tma', 'TheMovieArchive')

    def setUrl(self, url):
        self._url = str(url).replace('+', '%2B').split('#')[0]

    def _getMediaLinkForGuest(self, autoPlay = False):
        api_call = ''
        sMain = base64.b64decode('aHR0cHM6Ly93d3cuYnJhZmxpeC52aWRlbw==').decode('utf8',errors='ignore')
        sMain2 = base64.b64decode('aHR0cHM6Ly92aWRzcmMuYnJhZmxpeC52aWRlby92aWRzcmMv').decode('utf8',errors='ignore')

        SubTitle = ''
        if ('sub.info' in self._url):
            sID = self._url.split('sub.info=')[1]
            api_call = self._url.split('?sub.info=')[0] + '|User-Agent=' + UA + '&Referer=' + sMain + '/' + '&Origin=' + sMain
        
        headers = {
        'sec-ch-ua':'"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile':'?0',
        'user-agent':UA,
        'sec-ch-ua-platform':'"Windows"',
        'accept':'*/*',
        'origin':sMain,
        'sec-fetch-site':'same-site',
        'sec-fetch-mode':'cors',
        'sec-fetch-dest':'empty',
        'referer':sMain + '/',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'en-US,en;q=0.9'}
        payload=None

        subs = requests.request("GET", f'{sMain2}{sID}', headers=headers, data=payload).json()

        if subs:
            arabic_subtitles = [sub for sub in subs[0]['data']['sub'] if sub['lang'] == 'Arabic']
            if arabic_subtitles:
                for subtitle in arabic_subtitles:
                    SubTitle = subtitle['file']
            else:
                SubTitle = ''

        if api_call:
            if ('http' in SubTitle):
                return True, api_call, SubTitle
            else:
                return True, api_call

        return False, False
