#-*- coding: utf8 -*-
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import VSlog, xbmcgui
from resources.lib.gui.gui import cGui
from resources.hosters.hoster import iHoster
import  re

from resources.lib.packer import cPacker

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Thevid'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'thevid'

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
                    
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        if 'Not Found' in sHtmlContent:
        	dialog().VSinfo("404 Not Found")
        
        oParser = cParser()
              
        #Dean Edwards Packer
        sPattern = "(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            sUnpacked = cPacker().unpack(aResult[1][0])
        
        #fh = open('c:\\test.txt', "w")
        #sfilea="http://s005.thevid.net/v/892925a1c517aa9b70944ec53ec94aa3.mp4?e=1533859029&sa=CgOo0MoVWKjHhnVBzRFrAw&st=kW53T1epyxSYivAYzfvSxg";
        
        if (sUnpacked):

            sPattern ='var vldAb="(.+?)";'
            aResult = oParser.parse(sUnpacked, sPattern)
            
            #print aResult
            
            if (aResult[0] == True):
                return True , aResult[1][0]
        
        
        return False, False
        
        
