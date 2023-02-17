#coding: utf-8
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui
from resources.lib.comaddon import dialog
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'

import xbmcgui

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'extremenow', 'extremenow')
			
    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self):
        
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        VSlog(self._url)
        
        oParser = cParser()
        
            # (.+?) .+?
        sPattern = '{file:"(.+?)",label:"(.+?)"}'
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
                return True, api_call + '|User-Agent=' + UA + '&Referer=' + self._url +'&verifypeer=false'

        return False, False
        
