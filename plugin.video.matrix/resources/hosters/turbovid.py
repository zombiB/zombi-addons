# -*- coding: utf-8 -*-

from resources.lib.parser import cParser
from resources.lib.util import urlEncode
from resources.hosters.hoster import iHoster
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import VSlog, isMatrix
from resources.lib.aadecode import AADecoder
from resources.lib.util import urlHostName
from resources.lib.hunter import hunter
import base64

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'turbovid', 'Turbovid')

    def setUrl(self, url):
        self._url = url

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        api_call = False

        headers4 = {'user-agent': UA,
                    'Referer': self._url
                    }

        oParser = cParser()
        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()

        sPattern = "urlPlay = '([^']+)'"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = aResult[1][0]
            return True, api_call + '|' + urlEncode(headers4)

        sPattern = "data-path = '([^']+)'"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = base64.b64decode(aResult[1][0]).decode('utf8',errors='ignore')
            return True, api_call + '|' + urlEncode(headers4)

        sPattern = "data-hash\s*=\s*'([^']+)'"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = aResult[1][0]
            return True, api_call + '|' + urlEncode(headers4)

        sPattern = 'return decodeURIComponent\(escape\(r\)\)}\("([^,]+)",([^,]+),"([^,]+)",([^,]+),([^,]+),([^,\))]+)\)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            l = aResult[1]
            for j in l:
                unpacked = hunter(j[0],int(j[1]),j[2],int(j[3]),int(j[4]),int(j[5]))

                sPattern = "var urlPlay =\s*'([^']+)'"
                aResult = oParser.parse(unpacked, sPattern)
                if aResult[0]:  
                    hls_url = aResult[1][0]  

                    sRefer = urlHostName(self._url)
                    return True, f'{hls_url.strip()}|User-Agent={UA}&Referer=https://{sRefer}/&Origin=https://{sRefer}'

        return False, False
