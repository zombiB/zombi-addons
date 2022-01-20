#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#https://sama-share.com/embed-shsaa6s49l55-750x455.html
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog
import re

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'uppom'
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
        return 'uppom'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True
        
    def getPattern(self):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = sUrl
        d = re.findall('https://(.*?)/(.*?)',self.__sUrl)
        for aEntry1 in d:
            sId= aEntry1[0]
        #lien embed obligatoire
        if not 'embed-' in self.__sUrl:
            sfd= self.__sUrl.rsplit('/', 1)[1]
            self.__sUrl = 'https://'+sId+'/embed-'+sfd+'-750x455.html'
            VSlog(self.__sUrl)

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        VSlog(self.__sUrl)
        api_call = False

        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()

        oParser = cParser()
        sPattern =  '(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for i in aResult[1]:
                decoded = cPacker().unpack(i)
 
                if decoded:
                    r = re.search('file:"(.+?)",', decoded, re.DOTALL)
                    if r:
                        api_call = r.group(1)
                    r2 = re.search('src="(.+?)"', decoded, re.DOTALL)
                    if r2:
                        api_call = r2.group(1)


        if (api_call):
            return True, api_call + '|User-Agent=' + UA

        return False, False