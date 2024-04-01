from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog, xbmcgui
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog
import re
from resources.lib import random_ua

UA = random_ua.get_phone_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'filelions', 'filelions')
			
    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        api_call = ''

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        oParser = cParser()
       

        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        from resources.lib.util import Quote
        import unicodedata

        if aResult[0]:
            data = aResult[1][0]
            data = unicodedata.normalize('NFD', data).encode('ascii', 'ignore').decode('unicode_escape')
            sHtmlContent2 = cPacker().unpack(data)
      # (.+?) ([^<]+) .+?

            sPattern = 'file:"(.+?)"'
            aResult = oParser.parse(sHtmlContent2, sPattern)
            VSlog(aResult)
            if aResult[0]:
                api_call = aResult[1][0] 

        if api_call:
            return True, api_call + '|Referer=' + self._url + '&User-Agent=' + UA

        return False, False