#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler 
from resources.lib.parser import cParser 
from resources.lib.comaddon import dialog, xbmcgui
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'watchvideo'        
        self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName
        
    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'watchvideo'
        
    def setHD(self, sHD):
        self.__sHD = ''
        
    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

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
        
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        oParser = cParser()
        
        #lien indirect
        sPattern = '<iframe.+?src="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            oRequest = cRequestHandler(aResult[1][0])
            sHtmlContent = oRequest.request()
        
        #test pour voir si code
        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            sHtmlContent = cPacker().unpack(aResult[1][0])
        
        sPattern = 'file:"(.+?m3u8)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        api_call = False

        if (aResult[0] == True):

            api_call = aResult[0]
            if (api_call):
                return True, api_call
        
        sPattern = 'file:"([^"]+\.mp4)"(?:,label:"([^"]+)")*'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        api_call = False

        if (aResult[0] == True):
            
            #initialisation des tableaux
            url=[]
            qua=[]
            
            #Replissage des tableaux
            for i in aResult[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))

            api_call = dialog().VSselectqual(qua, url)

            if (api_call):
                return True, api_call

        return False, False