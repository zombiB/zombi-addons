# coding: utf-8

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog, dialog
from resources.lib.packer import cPacker


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'tuktuk', 'TukTuk', 'gold')

    def _getMediaLinkForGuest(self, autoPlay = False):
        self._url = self._url.replace('/f/','/e/').replace('/d/','/v/')
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        api_call = ''

        oParser = cParser()
        
        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            sHtmlContent = cPacker().unpack(aResult[1][0])

        sPattern = ',file:"(.+?)",thumbnails'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] :
            for aEntry in aResult[1]:
                sHtmlContent = aEntry

            sPattern = '(.+?)(http.+?.mp4)'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                url = []
                qua = []
                for i in aResult[1]:
                    url.append(str(i[1]))                  
                    qua.append(str(i[0].replace(',','')))

                api_call = dialog().VSselectqual(qua, url) + '|Referer=' + self._url

        sPattern = 'sources:\s*\[{file:\s*["\']([^"\']+)'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:
            api_call = aResult[1][0]

        if api_call:
            return True, api_call + '|Referer=' + self._url + '&AUTH=TLS&verifypeer=false'

        return False, False