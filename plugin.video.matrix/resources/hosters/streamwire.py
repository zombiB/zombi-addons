#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import cRequestHandler 
from resources.lib.comaddon import dialog
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser 
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog
import re,xbmcgui

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'streamwire'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName
        
    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'streamwire'
        
    def setHD(self, sHD):
        self.__sHD = ''
        
    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return False

    def isJDownloaderable(self):
        return False

    def getPattern(self):
        return ''
    
    def __getIdFromUrl(self, sUrl):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return
    
    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        VSlog(self.__sUrl)
    
        sUrl = self.__sUrl
        
        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()

        oParser = cParser()
            
        sPattern =  'src: "(.+?)",' 
        aResult = oParser.parse(sHtmlContent,sPattern)
        if (aResult[0] == True):
            m3url = aResult[1][0] 
            oRequest = cRequestHandler(m3url)
            sHtmlContent = oRequest.request()
   
        sPattern =  ',RESOLUTION=(.+?),.+?(http.+?m3u8)' 
        aResult = oParser.parse(sHtmlContent,sPattern)
        if (aResult[0] == True):
            #initialisation des tableaux
            url=[]
            qua=[]
            #Replissage des tableaux
            for i in aResult[1]:
                url.append(str(i[1]))
                qua.append(str(i[0]))

            api_call = dialog().VSselectqual(qua, url)

            if (api_call):
                return True, api_call

        return False, False
