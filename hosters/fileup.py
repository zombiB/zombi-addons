#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#http://cloudvid.co/embed-xxxx.html
#https://clipwatching.com/embed-xxx.html
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.packer import cPacker
from resources.lib.comaddon import dialog
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'fileup'
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
        return 'fileup'

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
        if not self.__sUrl.endswith('.html'):
            self.__sUrl = self.__sUrl + '.html'
            
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

        if 'File was deleted' in sHtmlContent:
            return False,False

        oParser = cParser()
        sPattern = "</script><script type='text/javascript'>([^<]+)</script></div>"
        aResult = oParser.parse(sHtmlContent,sPattern)

        if (aResult[0] == True):
            sHtmlContent = cPacker().unpack(aResult[1][0])

            sPattern = 'file:"([^"]+)",flashplayer:'
            aResult = oParser.parse(sHtmlContent,sPattern)
            if (aResult[0] == True):
				api_call = aResult[1][0] + '|User-Agent=' + UA + '&Referer=' + self.__sUrl
				
        if (api_call):
            return True, api_call

        return False, False