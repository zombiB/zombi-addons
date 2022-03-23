#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog, xbmcgui
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
import re,requests
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'cimanow'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR] [COLOR khaki]'+self.__sHD+'[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'cimanow'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return '';
        
    def __getIdFromUrl(self, sUrl):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = sUrl

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        VSlog(self.__sUrl)
        s = requests.Session()
        r = s.get(self.__sUrl).content

        oParser = cParser()
        sPattern =  '<source src="([^"]+)" type=\'(.+?)\'>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            url = []
            qua = []
            for x in aResult[1]:
                url.append(x[0])
                qua.append(x[1])
                	
                api_call = dialog().VSselectqual(qua,url)
                    
        if (api_call):
            return True, api_call + '|User-Agent=' + UA 
            
        return False, False