#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog
from resources.lib.util import urlHostName
import re

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'dynamic', 'Dynamic')

    def setUrl(self, sUrl):
        self._url = str(sUrl)

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        api_call =  False
        sReferer = ""
        sUrl = self._url
        if '|Referer=' in self._url:
            sReferer = self._url.split('|Referer=')[1]
            sUrl = self._url.split('|Referer=')[0]

        oRequest = cRequestHandler(sUrl)
        oRequest.addHeaderEntry('user-agent',UA)
        oRequest.addHeaderEntry('Referer', f'https://{urlHostName(sReferer)}/')
        oRequest.addHeaderEntry('Accept-Language', "en-US,en;q=0.9")
        sHtmlContent = oRequest.request()
              
        pattern = r"(\s*eval\s*\(\s*function\(p,a,c,k,e(?:.|\s)+?)<\/script>"
        matches = re.finditer(pattern, sHtmlContent)
        second_match = None
        for i, match in enumerate(matches, start=1):
            if i == 2:
                second_match = match
                break

        if second_match:
            sHtmlContent = cPacker().unpack(second_match.group())
        else:
            sPattern = '(\s*eval\s*\(\s*function(?:.|\s)+?{}\)\))'
            aResult = re.findall(sPattern, sHtmlContent)
            if aResult:
                sstr = aResult[0]
                if not sstr.endswith(';'):
                    sstr = sstr + ';'
                sHtmlContent = cPacker().unpack(sstr)


        sPattern = 'src=["\']([^"\']+)["\']'
        aResult = re.findall(sPattern, sHtmlContent)
        if aResult:
            url = aResult[0]
            if '.m3u8' in url:
                api_call = url
 
            if api_call:
                return True, api_call + '|User-Agent=' + UA + '&Referer=' + sUrl
            
        return False, False
   