#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog
import re,xbmcgui
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'dynamic', 'Dynamic')

    def setUrl(self, sUrl):
        self._url = str(sUrl)

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        sReferer = ""
        sUrl = self._url
        if '|Referer=' in self._url:
            sReferer = self._url.split('|Referer=')[1]
            sUrl = self._url.split('|Referer=')[0]
        
        oRequest = cRequestHandler(sUrl)
        oRequest.addHeaderEntry('user-agent',UA)
        oRequest.addHeaderEntry('Referer',sReferer)
        sHtmlContent = oRequest.request()
        
        oParser = cParser()
        
        sPattern = '(\s*eval\s*\(\s*function\(p,a,c,k,e(?:.|\s)+?)<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                sHtmlContent = cPacker().unpack(aEntry)
        
                sPattern = 'src=["\']([^"\']+)["\']'
                aResult = re.findall(sPattern, sHtmlContent)
                if aResult:
                    url = aResult[0]
                    if '.m3u8' in url:
                        api_call = url
 
            if api_call:
                return True, api_call + '|User-Agent=' + UA + '&Referer=' + sUrl
            
        return False, False
   