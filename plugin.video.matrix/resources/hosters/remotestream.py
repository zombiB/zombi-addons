#-*- coding: utf-8 -*-

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
import re
import requests
import base64

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'remotestream', 'Remotestre.am')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        referer = self._url
        if '?Referer=' in self._url:
            referer = self._url.split('?Referer=')[1]
            self._url = self._url.split('?Referer=')[0]

        headers = {'User-Agent': UA,
                   'Referer': referer
                   }
        s = requests.session()
        sHtmlContent = s.get(self._url, headers=headers).text

        api_call = ''
        SubTitle = ''


        aResult = re.search(r'"subtitle":"(.*?)"', sHtmlContent)
        if aResult:
            SubTitle = aResult.group(1)

        aResult = re.search(r'"file":"(.*?)"', sHtmlContent)
        if aResult:
            api_call = aResult.group(1).replace('\\','') 

        if api_call:
            if SubTitle:
                return True, api_call + '|User-Agent=' + UA + '&Referer=' + referer, SubTitle 
            else:
                return True, api_call + '|User-Agent=' + UA + '&Referer=' + referer

        return False, False