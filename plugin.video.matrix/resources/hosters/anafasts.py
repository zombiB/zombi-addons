#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog
import re,xbmcgui
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'anafasts'
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
        return 'anafasts'

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
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        VSlog(self.__sUrl)
        
        oParser = cParser()

        list_q = []
        list_url = []
        
            # (.+?) .+?
        sPattern = 'file:"(.+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            url2 = aResult[1][0]
            oRequestHandler = cRequestHandler(url2)
            sHtmlContent2 = oRequestHandler.request()
            sPattern = 'PROGRAM-ID.+?RESOLUTION=(\w+).+?(https.+?m3u8)'
            aResult = oParser.parse(sHtmlContent2, sPattern)
            for aEntry in aResult[1]:
                list_q.append(aEntry[0]) 
                list_url.append(aEntry[1]) 

            if list_url:
                api_call = dialog().VSselectqual(list_q,list_url)


            if (api_call):
                return True, api_call

        return False, False
        
