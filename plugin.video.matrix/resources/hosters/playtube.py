#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import cRequestHandler 
from resources.lib.comaddon import dialog
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser 
from resources.lib.packer import cPacker
import re,xbmcgui
UA = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'playtube'
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
        return 'playtube'
        
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
    
        sUrl = self.__sUrl
        
        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()

        oParser = cParser()
        sPattern = "<script type='text/javascript'>(.+?)</script>"
        aResult = oParser.parse(sHtmlContent,sPattern)
        if (aResult[0] == True):
            sHtmlContent1 = cPacker().unpack(aResult[1][0])
          # ([^<]+) .+? (.+?)
        sPattern = 'file:"(.+?)"'
        aResult = oParser.parse(sHtmlContent1, sPattern)
        if (aResult[0]):
            api_call = aResult[1][0]
        
        #xbmc.log(str(api_call))
        
        if (api_call):
            return True, api_call+ '|User-Agent=' + UA+ '&Referer=' + self.__sUrl
            
        return False, False