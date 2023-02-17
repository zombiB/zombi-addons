#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import VSlog
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
import re
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'shared', '4shared')

    def setUrl(self, sUrl):
        self._url = str(sUrl)
        if '/video/' in self._url:
            self._url = self._url.split('/')[4]
            self._url = "https://www.4shared.com/web/embed/file/"+self._url

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
 
        api_call = ''
        
        oParser = cParser()
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        sPattern = 'src="([^<]+)" type="video/mp4">'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = aResult[1][0]


        if api_call:
            return True, api_call+'|User-Agent=' + UA 
        


        return False, False
