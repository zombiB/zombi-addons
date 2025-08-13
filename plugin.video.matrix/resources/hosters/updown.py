from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog
from resources.lib import random_ua
import re
import unicodedata

UA = random_ua.get_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'updown', 'UPdown')
			
    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        sReferer = self._url
        if '|Referer=' in self._url:
            sReferer = self._url.split('|Referer=')[1]            
            self._url = self._url.split('|Referer=')[0]

        api_call = ''

        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('Referer', sReferer)
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()

        oParser = cParser()
        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            data = aResult[1][0]
            data = unicodedata.normalize('NFD', data).encode('ascii', 'ignore').decode('unicode_escape')
            sHtmlContent2 = cPacker().unpack(data)

            sPattern = 'file:"(.+?)"'
            aResult = oParser.parse(sHtmlContent2, sPattern)
            if aResult[0]:
                api_call = aResult[1][0] 

        else:
            d = re.findall('https://(.*?)/([^<]+)', self._url)

            for aEntry in d:
                sHost = aEntry[0]
                file_id = aEntry[1].replace('.html','')
                if '/' in file_id:
                    file_id = file_id.split('/')[0]
                sUrl = f'https://{sHost}/embed-{file_id}.html'

            oRequest = cRequestHandler(sUrl)
            oRequest.addHeaderEntry('Referer', sReferer)
            sHtmlContent = oRequest.request()
            oParser = cParser()
        
            sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                data = aResult[1][0]
                data = unicodedata.normalize('NFD', data).encode('ascii', 'ignore').decode('unicode_escape')
                sHtmlContent2 = cPacker().unpack(data)

                sPattern = 'file:"(.+?)"'
                aResult = oParser.parse(sHtmlContent2, sPattern)
                if aResult[0]:
                    api_call = aResult[1][0] 

        if api_call:
            return True, api_call

        return False, False