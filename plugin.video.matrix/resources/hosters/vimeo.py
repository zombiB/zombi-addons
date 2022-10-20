#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog
from resources.lib.comaddon import VSlog

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vimeo', 'Vimeo')

    def __getIdFromUrl(self, sUrl):
        sPattern = 'vimeo\.com\/(?:event\/)?([0-9]+)'
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if aResult[0] is True:
            return aResult[1][0]

        return ''

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        api_call = False

        sId = self.__getIdFromUrl(self._url)

        web_url = 'https://player.vimeo.com/video/' + sId

        oRequest = cRequestHandler(web_url)
        oRequest.addHeaderEntry('Referer', self._url)
        oRequest.addHeaderEntry('User-Agent', 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1')
        sHtmlContent = oRequest.request()
        sPattern =  ',"url":"(.+?)",.+?"quality":"(.+?)",'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:
            #initialisation des tableaux
            url=[]
            qua=[]

            #Remplissage des tableaux
            for i in aResult[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))

            #tableau
            api_call = dialog().VSselectqual(qua, url)

            if api_call:
                return True, api_call

            return False, False
