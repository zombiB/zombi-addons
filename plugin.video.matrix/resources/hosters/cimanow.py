#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog, VSlog
from resources.hosters.hoster import iHoster
from resources.lib.util import urlHostName
from resources.lib import helpers
from resources.lib import random_ua

UA = random_ua.get_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'cimanow', 'CimaNow', 'gold')
			
    def setUrl(self, sUrl):
        self._url = str(sUrl).replace('rrsrrs','cimanow').replace('rrsrrsn','newcima')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)

        oParser = cParser()
        sReferer = "https://cimanow.cc/"
        sHost = f'https://{urlHostName(self._url)}'
        surl = self._url

        oRequest = cRequestHandler(surl)
        oRequest.addHeaderEntry('Referer', sReferer)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.enableCache(False)
        oRequest.disableSSL()
        sHtmlContent = oRequest.request()

        list_url=[]
        list_q=[]
        sPattern = '<source src="(.+?)" type="video/mp4" size="(.+?)">' 
        aResult = oParser.parse(sHtmlContent,sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                    list_q.append(aEntry[1]) 
                    list_url.append(aEntry[0]) 
                    
            api_call = dialog().VSselectqual(list_q,list_url)
            api_call = sHost + api_call

        sPattern = (r'\[([0-9]+p)\]\s*([^,]+)"')
        aResult = oParser.parse(sHtmlContent,sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                    list_q.append(aEntry[0]) 
                    list_url.append(aEntry[1]) 
                    
            api_call = dialog().VSselectqual(list_q,list_url)
            api_call = sHost + api_call.strip()

        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "identity;q=1, *;q=0",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Host": urlHostName(self._url),
            "Referer": self._url,
            "User-Agent": UA,
            'verifypeer': 'false'
        }

        if api_call:
                    return True, api_call.replace(' ', '%20') + helpers.append_headers(headers)

        return False, False