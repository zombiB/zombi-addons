#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'lanesh', 'Direct-Link')
			
    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self):
        api_call = ''
        VSlog(self._url)

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        oParser = cParser()

        url = []
        qua = []   
        oParser = cParser()
        sPattern = "RESOLUTION=(\d+x\d+).*?(http.+?)#"

        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                url.append(aEntry[1])
                qua.append(aEntry[0])

            if (url):
                api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call

        return False, False