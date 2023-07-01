#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#http://uqload.com/embed-xxx.html
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog
UA = 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'gettyshare', 'gettyshare')

    def setUrl(self, url):
        self._url = str(url)
        # lien embed obligatoire
        if '/video/embed/' not in self._url:
            self._url = self._url.replace('https://gettyshare.com/','https://gettyshare.com/video/embed/')

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        api_call = ''
        oParser = cParser()

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        oDialog = dialog()

        sPattern1 = 'mp4HD: "(.+?)",'

        aResult = oParser.parse(sHtmlContent, sPattern1)
        if aResult[0]:
            api_call = aResult[1][0]

        if api_call:
            return True, api_call + '|User-Agent=' + UA + '&Referer=' + self._url

        return False, False
