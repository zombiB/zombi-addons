# -*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog
from resources.lib.parser import cParser
import requests

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'febb', 'Direct Link', 'gold')

    def setUrl(self, url):
        self._url = str(url).replace('+', '%2B').split('?sub.info=')[0]
        self._url0 = str(url)

    def _getMediaLinkForGuest(self, autoPlay = False):
        api_call = self._url
        VSlog(api_call)

        if ('sub.info' in self._url0):
            SubTitle = self._url0.split('sub.info=')[1]
            if '&t=' in SubTitle:
                SubTitle = SubTitle.split('&t=')[0]

            if SubTitle is False:
                SubTitle = ''
            else:
                if 'http' in SubTitle:
                    if '.txt' in SubTitle:
                        SubTitle = requests.get(SubTitle).url
                    else:
                        oRequest0 = cRequestHandler(SubTitle)
                        sHtmlContent0 = oRequest0.request().replace('\\','')
                        oParser = cParser()

                        sPattern = '"file":"([^"]+)".+?"label":"(.+?)"'
                        aResult = oParser.parse(sHtmlContent0, sPattern)
                        if aResult[0]:
                            url = []
                            qua = []
                            for i in aResult[1]:
                                url.append(str(i[0]))
                                qua.append(str(i[1]))
                            SubTitle = dialog().VSselectsub(qua, url)

        api_call = self._url

        if api_call:
            if ('http' in SubTitle):
                return True, api_call, SubTitle
            else:
                return True, api_call

        return False, False
