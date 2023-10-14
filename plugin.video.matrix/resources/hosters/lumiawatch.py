#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog
import re
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'lumiawatch', 'lumiawatch')

    def setUrl(self, url):
        self._url = str(url)
        if not '/v/' in self._url:
             self._url = self._url.replace("/d/","/v/")

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        sReferer = self._url
        url = self._url
        
        oRequest = cRequestHandler(url)
        oRequest.addHeaderEntry('user-agent',UA)
        oRequest.addHeaderEntry('Referer',sReferer)
        sHtmlContent = oRequest.request()
        
        oParser = cParser()
        
        sPattern = "<script type='text/javascript'>(.+?)</script>"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            sHtmlContent = cPacker().unpack(aResult[1][0])
            # (.+?) .+?
            sPattern = 'file:"(.+?)"'
            aResult = oParser.parse(sHtmlContent, sPattern)
            VSlog(aResult)
            if aResult[0]:
               api_call = aResult[1][0] 
 
        if (api_call):
           return True, api_call+'|AUTH=TLS&verifypeer=false'  + '&User-Agent=' + UA + '&Referer=' + sReferer
            
        return False, False
   