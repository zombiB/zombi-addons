#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import cRequestHandler 
from resources.lib.comaddon import dialog
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser 
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog
import re,xbmcgui
UA = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidforup', 'vid4up')

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
    
        sUrl = self._url
        
        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()
     # (.+?) ([^<]+)
        oParser = cParser()
        sPattern =  '<source src="([^<]+)" type=.+?res="([^<]+)">' 
        aResult = oParser.parse(sHtmlContent,sPattern)
        if (aResult[0] == True):
            #initialisation des tableaux
            url=[]
            qua=[]
            #Replissage des tableaux
            for i in aResult[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))

            api_call = dialog().VSselectqual(qua, url)
            stoken = ""
            stoken = api_call.split('token=')[1]

            if (api_call):
                return True,api_call+'|token='+stoken+ '&User-Agent=' + UA + '&Referer=https://blkom.com'  

        return False, False
