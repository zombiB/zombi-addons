#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#https://letsupload.co/plugins/mediaplayer/site/_embed.php?u=1r0c1&w=770&h=320
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.comaddon import VSlog

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'letsupload', 'Letsupload')

    def isDownloadable(self):
        return False

    def setUrl(self, sUrl):
        self._url = str(sUrl)
        if 'embed' in sUrl:
            self._url = self._url.replace("embed-","")
        if 'mediaplayer' not in sUrl:
            parts = self._url.split('/')[3]
            self._url = "https://letsupload.co/plugins/mediaplayer/site/_embed.php?u="+parts


    def _getMediaLinkForGuest(self):
        VSlog(self._url)

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        oParser = cParser()
        

        sPattern = 'mp4HD: "(.+?)",'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            api_call = aResult[1][0] +'|User-Agent=' + UA + '&Referer=' + self._url
        
        sPattern = "source:'([^<]+)',"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0]):
            api_call = aResult[1][0]

        if (api_call):
            return True, api_call

        return False, False