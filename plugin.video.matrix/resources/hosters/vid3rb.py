
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog, siteManager
from resources.lib.util import urlHostName
from resources.lib import random_ua

UA = random_ua.get_pc_ua()

class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'vid3rb', 'Vid3rb', 'gold')

    def _getMediaLinkForGuest(self, autoPlay = False):
        api_call = False

        oRequest = cRequestHandler(self._url.replace('amp;',''))
        oRequest.enableCache(False)
        oRequest.addHeaderEntry('Referer', siteManager().getUrlMain('anime3rb'))
        oRequest.addHeaderEntry('Acccept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7')
        oRequest.addHeaderEntry('Sec-Fetch-Dest', 'iframe')
        oRequest.addHeaderEntry('Host', urlHostName(self._url))
        oRequest.addHeaderEntry('User-Agent', UA)
        sHtmlContent = oRequest.request()

        oParser = cParser()
        sPattern = 'src:\s*["\']([^"\']+)["\'],\s*type:.+?label:\s*["\']([^"\']+)["\']'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            url = []
            qua = []

            for aEntry in aResult[1]:
                url.append(str(aEntry[0]))
                qua.append(str(aEntry[1]))

            api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, f'{api_call}|Referer={self._url}'

        return False, False
