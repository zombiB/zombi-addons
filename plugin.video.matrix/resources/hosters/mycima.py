#-*- coding: utf-8 -*-

import re
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog, dialog
from resources.lib.util import Unquote
from resources.lib.parser import cParser
from resources.lib import random_ua

UA = random_ua.get_phone_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'mycima', 'WeCima', 'gold')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        sReferer = self._url
        if '|Referer=' in self._url:
            sReferer = self._url.split('|Referer=')[1]
            self._url = self._url.split('|Referer=')[0]

        oRequestHandler = cRequestHandler(self._url)
        oRequestHandler.disableSSL()
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', sReferer)
        oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
        oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        oRequestHandler.enableCache(False)
        sHtmlContent = oRequestHandler.request()

        r2 = re.search(' src="([^<]+)" type="video/mp4">', sHtmlContent)

        if (r2):
            api_call = r2.group(1)
            api_call = Unquote(api_call)
            return True, api_call.replace(' ', '%20') + "|Referer=" + sReferer + '&User-Agent=' + UA + '&verifypeer=false'

        oParser = cParser()
        sPattern = ' src="([^<]+)" type="video/mp4" size="([^"]+)">'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            shost = self._url.split('/e/')[0]
            url = []
            qua = []

            for aEntry in aResult[1]:
                url.append(aEntry[0])
                qua.append(f'{aEntry[1]}p')

            mUrl = dialog().VSselectqual(qua, url)
            api_call = f'{shost}{mUrl}'

            api_call = Unquote(api_call)
            return True, api_call.replace(' ', '%20') + "|Referer=" + sReferer + '&User-Agent=' + UA + '&verifypeer=false'

        return False, False
