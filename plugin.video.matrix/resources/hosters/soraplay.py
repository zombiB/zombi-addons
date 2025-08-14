#-*- coding: utf-8 -*-

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
import re
import requests

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'soraplay', 'SoraPLay')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        sReferer = self._url 
        if '|Referer=' in self._url:
            sReferer = self._url.split('|Referer=')[1]
            self._url = self._url.split('|Referer=')[0]

        headers = {'User-Agent': UA,
                   'Referer': sReferer
                   }
        s = requests.session()
        sHtmlContent = s.get(self._url, headers=headers, timeout=60).text

        api_call = ''

        aResult = re.findall(r'"file":"(.*?)"', sHtmlContent)
        if aResult:
            api_call = aResult[0]
        else:
            return False
        
        if api_call:
            return True, api_call + '|User-Agent=' + UA + '&Referer=' + self._url

        return False, False
