#-*- coding: utf-8 -*-

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
from resources.lib import random_ua

UA = random_ua.get_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'direct_link', 'Direct Link', 'gold')

    def setUrl(self, url):
        self._url = str(url).replace('+', '%20') 

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)

        api_call = self._url

        SubTitle = ''
        if ('sub.info' in self._url):
            SubTitle = self._url.split('sub.info=')[1]
            self._url = self._url.replace('+', '%2B').split('?sub.info=')[0]

        api_call = self._url.replace("rrsrr","cimanow").replace('rrsrrsn','newcima')
 	   
        if 'ffsff' in api_call:
            api_call = self._url.replace("ffsff","moshahda")
            sReferer = self._url.split('|Referer=')[1]      
            api_call = api_call + '|User-Agent=' + UA + '&Referer=' + sReferer
      
        if 'panet' in api_call:
            api_call = api_call + '|AUTH=TLS&verifypeer=false' 

        if 'scorarab' in api_call:
            api_call = api_call + '|&User-Agent=' + UA + '&Referer=' + 'https://live.scorarab.com/'

        if 'beintube' in api_call:
            api_call = api_call + '|AUTH=TLS&verifypeer=false&Referer=' + 'https://bein-match.net/'

        if 'cimanow' in api_call:
            api_call = api_call + '|AUTH=TLS&verifypeer=false' + '&User-Agent=' + UA + '&Referer=' + 'https://cimanow.cc/'
       
        if '?src=' in api_call:
            api_call = api_call.split('?src=')[1]
       
        if '+' in api_call:
            api_call = api_call.replace("[","%5B").replace("]","%5D").replace("+","%20")
        	   
        if 'goal4live.com' in api_call:
            api_call = api_call + '|User-Agent=' + UA 

        if 'fushaar' in api_call:
            api_call = f'{api_call}|User-Agent={UA}&Referer={self._url}&verifypeer=false'

        if api_call:
            if ('http' in SubTitle):
                return True, api_call, SubTitle
            else:
                return True, api_call

        return False, False
