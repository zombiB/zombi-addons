#-*- coding: utf-8 -*-


from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog, VSlog
from resources.hosters.hoster import iHoster

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'yadisk', 'yadisk')

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        api_call = False

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        oParser = cParser()
        sPattern =  '"height":(.+?)},"url":"(.+?)"}'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0]):

            url=[]
            qua=[]
            api_call = False

            for aEntry in aResult[1]:
                url.append(aEntry[1])
                qua.append(aEntry[0])

            api_call = dialog().VSselectqual(qua, url)

            if api_call:
                return True, api_call

        return False, False
