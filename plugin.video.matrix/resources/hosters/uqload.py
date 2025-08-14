#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog

UA = 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'uqload', 'Uqload')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        api_call = ''
        oParser = cParser()

        oRequest = cRequestHandler(self._url)
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()

        sPattern1 = 'sources.+?"([^"]+mp4)"'

        aResult = oParser.parse(sHtmlContent, sPattern1)
        if aResult[0]:
            api_call = aResult[1][0]

        if api_call:
            return True, api_call + '|User-Agent=' + UA + '&Referer=' + self._url.rsplit("/",1)[0]+'/' + '&Host=' + api_call.rsplit("/",3)[1]

        return False, False
