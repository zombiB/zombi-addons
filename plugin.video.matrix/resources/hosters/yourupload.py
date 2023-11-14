#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog, VSlog
from resources.hosters.hoster import iHoster

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'yourupload', 'yourupload')

    def setUrl(self, sUrl):
        self._url = str(sUrl)
        if 'embed' not in self._url:
            self._url = self._url.replace("/watch/","/embed/")

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        
        #https://www.yourupload.com/embed/8a7isfMAQ1T1
        
        oParser = cParser()
        
            # (.+?) .+?
        sPattern = "file: '(.+?)',"
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        api_call = False

        if aResult[0]:
            for aEntry in aResult[1]:
                if 'http' not in aEntry:
                    continue 
                api_call = aEntry

                if api_call:
                    return True, api_call + '|User-Agent=' + UA+ '&Referer=' + self._url
        