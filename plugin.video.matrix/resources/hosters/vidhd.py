#coding: utf-8
#
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog, VSlog
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidhd', 'vidhd')

    def setUrl(self, sUrl):
        self._url = str(sUrl)
        if 'embed' in sUrl:
            self._url = self._url.replace("embed-","")

    def _getMediaLinkForGuest(self):
        VSlog(self._url)

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        oParser = cParser()
        
        #lien indirect
        sPattern = '<iframe.+?src="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            oRequest = cRequestHandler(aResult[1][0])
            sHtmlContent = oRequest.request()
        
        #test pour voir si code
        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sHtmlContent = cPacker().unpack(aResult[1][0])
        
        sPattern = 'file:"([^"]+\.mp4)"(?:,label:"([^"]+)")*'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        api_call = False

        if aResult[0]:
            
            #initialisation des tableaux
            url=[]
            qua=[]
            
            #Replissage des tableaux
            for i in aResult[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))
            api_call = dialog().VSselectqual(qua, url)
 
            if api_call:
                return True, api_call 

        return False, False
