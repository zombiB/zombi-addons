#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog

UA = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'arabseed', 'arabseed')

    def isDownloadable(self):
        return True

    def setUrl(self, sUrl):
        self._url = str(sUrl)

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        sUrl = self._url

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        oParser = cParser()
            # (.+?) .+?
        sPattern = '<source src="(.+?)" type="video/mp4"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        api_call = False

        if aResult[0] :
            api_call = aResult[1][0]

        if api_call:
            return True, api_call+ '|User-Agent=' + UA +'&verifypeer=false'

        return False, False
        
