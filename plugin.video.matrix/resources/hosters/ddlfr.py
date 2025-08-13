# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import base64
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog
from resources.lib.packer import cPacker

class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'ddlfr', 'ddlfr')

    def _getMediaLinkForGuest(self, autoPlay = False):
        VSlog(self._url)
        api_call = ''

        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('Referer', self._url)
        sHtmlContent = oRequest.request()

        oParser = cParser()
        sPattern = 'JuicyCodes\.Run\("(.+?)"\);'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:

            media = aResult[1][0].replace('+', '')
            media = base64.b64decode(media)

            media = cPacker().unpack(media)
            if media:
                sPattern = '{"file":"(.+?)","label":"(.+?)"'
                aResult = oParser.parse(media, sPattern)
                if aResult[0]:
                    url = []
                    qua = []

                    for i in aResult[1]:
                        url.append(str(i[0] + '|Referer=' + self._url))
                        qua.append(str(i[1]))

                    api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call

        return False, False
