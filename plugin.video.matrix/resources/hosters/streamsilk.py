#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.hunter import hunter
from resources.lib.comaddon import VSlog
from resources.lib.util import urlHostName

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'streamsilk', 'StreamSilk')

    def _getMediaLinkForGuest(self, autoPlay = False):
        hls_url = False
        VSlog(self._url)

        sHost = urlHostName(self._url)
        sRefer = self._url
        if '|Referer=' in self._url:
            sRefer = self._url.split('|Referer=')[1]
            self._url = self._url.split('|Referer=')[0]

        self._url = self._url.replace('/d/','/p/')
        oParser = cParser()
        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()

        sPattern = 'return decodeURIComponent\(escape\(r\)\)}\("([^,]+)",([^,]+),"([^,]+)",([^,]+),([^,]+),([^,\))]+)\)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            l = aResult[1]
            for j in l:
                unpacked = hunter(j[0],int(j[1]),j[2],int(j[3]),int(j[4]),int(j[5]))

                sPattern = 'var urlPlay =\s*"(.*?m3u8.*?)"'
                aResult = oParser.parse(unpacked, sPattern)
                if aResult[0]:  
                    hls_url = aResult[1][0] 

        if hls_url:
            return True, f'{hls_url.strip()}|User-Agent={UA}&Referer={sRefer}&Host={sHost}'

        return False, False
