from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.util import urlHostName
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog
from resources.lib import random_ua

UA = random_ua.get_phone_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'upzur', 'Upzur')
			
    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        api_call = ''
        if '|Referer=' in self._url:
            sReferer = self._url.split('|Referer=')[1]
            self._url = self._url.split('|Referer=')[0]
        else:
            sReferer = f'https://{urlHostName(self._url)}/'
        sOrigin = f'https://{urlHostName(self._url)}'

        oParser = cParser()
        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request().encode("utf8",errors='ignore').decode("unicode_escape")

        sPattern = r'var\s+(\w+)\s*=\s*\[(.*?)\]'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:

                src = aEntry[1]
                items = src.split(',')
                char_list = [item.strip()[1:-1] if item.strip()[0] == item.strip()[-1] and item.strip()[0] in ('"', "'") else item.strip() for item in items]
                src_reverse = char_list[::-1]
                sHtmlContent = ''.join(src_reverse)

        sPattern = r'source\s*src="(.+?)"\s*type='
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = aResult[1][0]

        if api_call:
            return True, f'{api_call}|Referer={sReferer}&verifypeer=false&Origin={sOrigin}'

        return False, False