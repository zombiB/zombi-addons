#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#https://vidoza.net/embed-xxx.html
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog
from resources.lib.comaddon import VSlog

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidoza', 'Vidoza')

    def isDownloadable(self):
        return False

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        sPattern =  'src: *"([^"]+)".+?label:"([^"]+)"'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] :
            #initialisation des tableaux
            url=[]
            qua=[]
            #Remplissage des tableaux
            for i in aResult[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))

            #dialogue qualité
            api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call

        return False, False
