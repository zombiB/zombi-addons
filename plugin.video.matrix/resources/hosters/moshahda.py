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
        self.__sDisplayName = 'moshahda'
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
        return 'moshahda'

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
        if not "embed" in self.__sUrl:
               self.__sUrl = self.__sUrl.replace("https://moshahda.net/","https://moshahda.net/embed-")

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        sReferer = ""
        url = self.__sUrl.split('|Referer=')[0]
        sReferer = self.__sUrl.split('|Referer=')[1]
        
        oRequest = cRequestHandler(url)
        oRequest.addHeaderEntry('user-agent',UA)
        oRequest.addHeaderEntry('Referer',sReferer)
        sHtmlContent = oRequest.request()
        VSlog(self.__sUrl)
        
        oParser = cParser()
        
        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            sHtmlContent = cPacker().unpack(aResult[1][0])
        
            # (.+?) .+?
        sPattern = 'file: "(.+?)"}'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        api_call = False

        if (aResult[0] == True):
            oRequest = cRequestHandler(aResult[1][0])
            data = oRequest.request()
        	
            sPattern =  ',RESOLUTION=(.+?),CODECS=".+?"(.+?).15'
            aResult = oParser.parse(data, sPattern)
            if (aResult[0] == True):
               url=[]
               qua=[]
               for i in aResult[1]:
                  url.append(str(i[1])+".15")
                  qua.append(str(i[0]).split('x')[1]+"p")
               api_call = dialog().VSselectqual(qua, url)
 
            if (api_call):
                return True, api_call + '|User-Agent=' + UA + '&Referer=' + sReferer
            
        return False, False
   