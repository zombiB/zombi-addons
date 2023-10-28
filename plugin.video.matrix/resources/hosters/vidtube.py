from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog, xbmcgui
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog
import re

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidtube', 'VidTube')
			
    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        sReferer = ''
        if '/d/' in self._url:
            self._url = self._url.replace('/d/','/embed-')
        if '/e/' in self._url:
            self._url = self._url.replace('/e/','/embed-')
        if '|Referer=' in self._url:
            sReferer = self._url.split('|Referer=')[1]            
            self._url = self._url.split('|Referer=')[0]
        VSlog(self._url)

        api_call = ''

        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('Referer', sReferer)
        sHtmlContent = oRequest.request()
        sPattern = "(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>"
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            sHtmlContent = cPacker().unpack(aResult[1][0])
        
        sPattern = 'file:"([^"]+)".+?label:"([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            url = []
            qua = []
            for i in aResult[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))

            api_call = dialog().VSselectqual(qua, url)

        sPattern =  'sources: *\[{file:"([^"]+)"' 
        aResult = oParser.parse(sHtmlContent,sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:            
                api_call = aEntry

        if api_call:
            return True, api_call

        return False, False