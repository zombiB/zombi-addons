#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:62.0) Gecko/20100101 Firefox/62.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'upstream', 'Upstream')

    def isDownloadable(self):
        return False
			
    def setUrl(self, sUrl):
        self._url = str(sUrl)
        if not 'embed-' in self._url:
            self._url = self._url.replace('-','')

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        api_call = ''

        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry("User-Agent",UA)
        sHtmlContent = oRequest.request()

        sPattern = "(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>"
        aResult_1 = re.findall(sPattern, sHtmlContent)

        if (aResult_1):
            sUnpacked = cPacker().unpack(aResult_1[0])
            sHtmlContent = sUnpacked

        sPattern = 'sources: *\[\{file:"([^"]+)"'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] :
            api_call = aResult[1][0]
        elif len(aResult_1) > 1 :
            sUnpacked = cPacker().unpack(aResult_1[1])
            sHtmlContent = sUnpacked
            sPattern = 'sources: *\[\{file:"([^"]+)"'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] :
                api_call = aResult[1][0]

        if api_call:
            return True, api_call + '|Referer=' + self._url

        return False, False
