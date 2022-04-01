from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog, xbmcgui
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog
import re

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'hdup', 'hdup')
			
    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        api_call = ''

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        oParser = cParser()
        

        sPattern = 'file:"([^<]+)",label'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            api_call = aResult[1][0] +'|User-Agent=' + UA + '&Referer=' + self._url
       
        sPattern = "(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            sdata = cPacker().unpack(aResult[1][0])
            sPattern = 'file:"(.+?)",label:".+?"}'
            aResult = oParser.parse(sdata,sPattern)
            if aResult[0] is True:
                api_call = aResult[1][0] 

        if api_call:
            return True, api_call

        return False, False