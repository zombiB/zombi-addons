#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.util import urlHostName
from resources.lib.comaddon import dialog, VSlog
from resources.lib import random_ua

UA = random_ua.get_phone_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'anafasts', 'Anafasts')

    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self, autoPlay = False):
        self._url = self._url.replace('embed-','')
        sReferer = f'https://{urlHostName(self._url)}/'
        VSlog(self._url)

        oParser = cParser()
        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Accept-Language', 'en-US,en;q=0.9')
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()

        list_q = []
        list_url = []
        api_call = False
        
        sPattern = 'file:"([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            url2 = aResult[1][0]
            
            oRequestHandler = cRequestHandler(url2)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Accept-Language', 'en-US,en;q=0.9')
            sHtmlContent2 = oRequestHandler.request()

            sPattern = 'PROGRAM-ID.+?RESOLUTION=(\d+x\d{0,3}).+?(http.+?)(#|$)'
            aResult = oParser.parse(sHtmlContent2, sPattern)
            for aEntry in aResult[1]:
                list_q.append(aEntry[0].split('x')[1]+"p") 
                list_url.append(aEntry[1]) 

            if list_url:
                api_call = dialog().VSselectqual(list_q,list_url)

            if api_call:
                return True, f'{api_call}|User-Agent={UA}&Referer={sReferer}&verifypeer=false&Accept-Language=en-US,en;q=0.9'

        return False, False