from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog, VSlog
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.util import urlHostName
from resources.lib import random_ua
import re, json

UA = random_ua.get_phone_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'dzen', 'Dzen')
			
    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        api_call = ''
        sReferer = f'https://{urlHostName(self._url)}/'

        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Referer', sReferer)
        oRequest.addHeaderEntry('Accept-Language', 'en-US,en;q=0.9')
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()

        json_data = re.search(r'"streams":\s*\[(.*?)]', sHtmlContent, re.DOTALL).group(0)
        sHtmlContent = json.loads(f"{{{json_data}}}")
        url = []
        qua = []
        for link in reversed(sHtmlContent["streams"]):
            url.append(link["url"])
            qua.append((link["type"]).upper())

        api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call + '|User-Agent=' + UA + '&Referer=' + sReferer + '&Host=' + f'https://{urlHostName(self._url)}'

        return False, False