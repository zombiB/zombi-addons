#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#https://sama-share.com/embed-shsaa6s49l55-750x455.html
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog


UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'filerio', 'filerio')

    def setUrl(self, sUrl):
        self._url = str(sUrl)
        #lien embed obligatoire
        if not 'embed-' in self._url:
            self._url = self._url.rsplit('/', 1)[1]
            self._url = 'https://filerio.in/embed-'+self._url+'-600x320.html'

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        api_call = False

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        oParser = cParser()
        
        sPattern = '<source src="(.+?)" type="video/mp4"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0]):
            api_call = aResult[1][0]


        if api_call:
            return True, api_call + '|User-Agent=' + UA

        return False, False