#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
#from resources.lib.comaddon import VSlog
from resources.lib.packer import cPacker


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'tuktuk', 'TukTuk', 'gold')

    def _getMediaLinkForGuest(self):
        self._url = self._url.replace('/f','/e')
        VSlog(self._url)
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        api_call = ''

        oParser = cParser()
        
        sPattern = '(\s*eval\s*\(\s*function\(p,a,c,k,e(?:.|\s)+?)<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:
            sHtmlContent = cPacker().unpack(aResult[1][0])
        
        sPattern = 'sources:\s*\[{file:\s*["\']([^"\']+)'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:
            api_call = aResult[1][0]

        if api_call:
            return True, api_call+ '|Referer=https://w.tuktokcinema.com/'

        return False, False
