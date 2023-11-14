#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import VSlog, dialog
from resources.hosters.hoster import iHoster

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'workupload', 'workupload')

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
    
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
            #(.+?)([^<]+)
        oParser = cParser()
        sStart = '<div id="download" class="row">'
        sEnd = '</div>'
        sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

        sPattern =  'href="(.+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0]):
            api_call = 'https://workupload.com'+aResult[1][0]
        if api_call:
            return True, api_call + '|User-Agent=' + UA
                     
            
        return False, False