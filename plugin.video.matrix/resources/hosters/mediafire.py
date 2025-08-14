#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import VSlog
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'mediafire', 'mediafire')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
    
        oRequest = cRequestHandler(self._url)
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()

        oParser = cParser()
        sStart = '<div class="dl-utility-nav">'
        sEnd = '</span>'
        sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

        sPattern =  'href="(.+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0]):
            api_call = aResult[1][0]
        if api_call:
            return True, api_call + '|User-Agent=' + UA
                     
        return False, False