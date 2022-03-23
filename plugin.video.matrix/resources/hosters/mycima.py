#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
import re
UA = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'


class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'mycima'
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
        return 'mycima'
        
    def setHD(self, sHD):
        self.__sHD = ''
        
    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
    
    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        VSlog(self.__sUrl)



        oRequestHandler = cRequestHandler(self.__sUrl)
        oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
        oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
        oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        sHtmlContent = oRequestHandler.request()

        r2 = re.search(' src="([^<]+)" type="video/mp4">', sHtmlContent)
        if (r2):
        	api_call = r2.group(1)
 
        if (api_call):
        	return True, api_call  + '|User-Agent=' + UA + '&Referer=' + self.__sUrl

        return False, False