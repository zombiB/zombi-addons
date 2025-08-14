# -*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog

class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'downloadgg', 'Download.gg')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        
        self._url = self._url.replace('/file-','/iframe-').replace('/play-','/iframe-')
        api_call = ''
        oParser = cParser()

        oRequest = cRequestHandler(self._url)
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()

        sPattern = '<video src="([^"]+)".*?data-title'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = aResult[1][0]
            
        if api_call:
            return True, api_call 

        return False, False
