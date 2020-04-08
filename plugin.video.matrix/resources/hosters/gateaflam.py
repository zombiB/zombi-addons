#coding: utf-8
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui
from resources.lib.comaddon import dialog
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog
from resources.lib.packer import cPacker
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'

import xbmcgui

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'gateaflam'
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
        return 'gateaflam'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''
        
    def __getIdFromUrl(self):
        sPattern = "v=([^<]+)"
        oParser = cParser()
        aResult = oParser.parse(self.__sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''
        
    def __modifyUrl(self, sUrl):
        return sUrl;
        
    def __getKey(self):
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
        if 'Video is processing now' in sHtmlContent:
			dialog().VSinfo("Video is processing...")
        
        api_call = ''
        #type1/([^"]+)/
        oParser = cParser()

        sPattern =  'url=(.+?)" />' 
        aResult = oParser.parse(sHtmlContent,sPattern)
        if (aResult[0] == True):
            m3url = aResult[1][0] 
            oRequest = cRequestHandler(m3url)
            sHtmlContent = oRequest.request()

        sPattern =  '"file": "(.+?)",' 
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
                return True, api_call + '|User-Agent=' + UA + '&Referer=' + self.__sUrl

        return False, False
