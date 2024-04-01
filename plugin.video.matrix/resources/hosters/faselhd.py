#coding: utf-8
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog
from resources.lib import random_ua

UA = random_ua.get_phone_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'faselhd', 'FaselHD', 'gold')

    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self, autoPlay = False):
        api_call = self._url
        VSlog(self._url)
        oParser = cParser()   

        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('user-agent',UA)
        sHtmlContent = oRequest.request()

        sPattern = ',RESOLUTION=(.+?),.+?(http.+?m3u8)'
        aResult = oParser.parse(sHtmlContent, sPattern)	
        if aResult[0]:
            sLink = []
            sQual = []
            for Stream in aResult[1]:
                sLink.append(str(Stream[1]))
                sQual.append(str(Stream[0]))
            api_call = dialog().VSselectqual(sQual, sLink)

        if api_call:
            return True, api_call + '|User-Agent=' + UA

        return False, False