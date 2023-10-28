# -*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
#from resources.lib.comaddon import VSlog
from resources.lib.packer import cPacker

TimeOut = 60 
class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'qfilm', 'qFilmXvideo')

    def _getMediaLinkForGuest(self):
        oRequest = cRequestHandler(self._url)
        oRequest.setTimeout(TimeOut)
        sHtmlContent = oRequest.request()

        api_call = ''

        oParser = cParser()
        
        sPattern = '(\s*eval\s*\(\s*function\(p,a,c,k,e(?:.|\s)+?)<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            sHtmlContent = cPacker().unpack(aResult[1][0])
        
        sPattern = 'sources:\s*\[{file:\s*["\']([^"\']+)'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            api_call = aResult[1][0]

        if api_call:
            return True, api_call +'|AUTH=TLS&verifypeer=false'

        return False, False
