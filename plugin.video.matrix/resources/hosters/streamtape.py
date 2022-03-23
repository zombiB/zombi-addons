#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog

import re
UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Streamtape'
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
        return 'streamtape'

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
        api_call = ''
        oParser = cParser()

        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        
        src = re.search(r'''ById\('vi.+?=\s*(["'][^;<]+)''', sHtmlContent)
        VSlog(self.__sUrl)
        
        if src:
            src_url = ''
            parts = src.group(1).split('+')
            for part in parts:
                p1 = re.findall(r'''['"]([^'"]*)''', part)[0]
                p2 = int(part.split(".substring(")[-1][:-1]) if 'substring' in part else 0
                src_url += p1[p2:]
            src_url += '&stream=1'
            src_url = 'https:' + src_url if src_url.startswith('//') else src_url
            api_call = src_url

        if (api_call):
            return True, src_url + '|User-Agent=' + UA + '&Referer=' + self.__sUrl

        return False, False