#-*- coding: utf-8 -*-
#https://www.vidlo.us/embed-xxx

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.packer import cPacker
from resources.lib.comaddon import dialog
from resources.lib.comaddon import VSlog

UA = 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidlo', 'vidlo')

    def _getMediaLinkForGuest(self):
        VSlog(self._url)

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

            # (.+?) .+? ([^<]+)
        oParser = cParser()
        #test pour voir si code
        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] :
            sHtmlContent = cPacker().unpack(aResult[1][0])
        sPattern = ',{file:"(.+?)",label:"(.+?)"}'
        aResult = oParser.parse(sHtmlContent, sPattern)
        api_call = False

        if aResult[0] :
            
            #initialisation des tableaux
            url=[]
            qua=[]
            
            #Replissage des tableaux
            for i in aResult[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))

            api_call = dialog().VSselectqual(qua, url)

            if api_call:
                return True, api_call + '|User-Agent=' + UA + '&Referer=https://www.vidlo.us/' 

        return False, False