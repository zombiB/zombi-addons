#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
import re

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'anafasts', 'anafasts')


    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self):
        
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        VSlog(self._url)
        
        oParser = cParser()

        list_q = []
        list_url = []
        
            # (.+?) .+?
        sPattern = 'file:"(.+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            url2 = aResult[1][0]
            oRequestHandler = cRequestHandler(url2)
            sHtmlContent2 = oRequestHandler.request()
            sPattern = 'PROGRAM-ID.+?RESOLUTION=(\w+).+?(https.+?m3u8)'
            aResult = oParser.parse(sHtmlContent2, sPattern)
            for aEntry in aResult[1]:
                list_q.append(aEntry[0].split('x')[1]+"p") 
                list_url.append(aEntry[1]) 

            if list_url:
                api_call = dialog().VSselectqual(list_q,list_url)


            if api_call:
                return True, api_call

        return False, False
        
