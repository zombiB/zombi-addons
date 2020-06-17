#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'DailyMotion'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR] [COLOR khaki]' + self.__sHD + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def setHD(self, sHD):
        if 'hd' in sHD:
            self.__sHD = 'HD'
        else:
            self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def getPluginIdentifier(self):
        return 'dailymotion'

    def isDownloadable(self):
        return True

    def getPattern(self):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        self.__sUrl = self.__sUrl.replace('http://dai.ly/', '')
        self.__sUrl = self.__sUrl.replace('http://www.dailymotion.com/', '')
        self.__sUrl = self.__sUrl.replace('https://www.dailymotion.com/', '')
        self.__sUrl = self.__sUrl.replace('embed/', '')
        self.__sUrl = self.__sUrl.replace('video/', '')
        self.__sUrl = self.__sUrl.replace('sequence/', '')
        self.__sUrl = self.__sUrl.replace('swf/', '')

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        api_call = True

        if (api_call):
            return True, 'plugin://plugin.video.dailymotion_com/?url=' + self.__sUrl + '&mode=playVideo'
        
        return False, False