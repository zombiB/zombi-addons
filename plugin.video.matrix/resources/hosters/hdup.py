﻿#coding: utf-8
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui
from resources.lib.comaddon import dialog, xbmcgui
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker

import re

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'hdup'
        self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'hdup'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''

    def __getIdFromUrl(self):
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
        
        api_call = ''

        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        oParser = cParser()
        sPattern =  "<script type='text/javascript'>(.+?)</script>"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            stri = cPacker().unpack(aResult[1][0])
            sPattern =  'file:"(.+?)",label:"(.+?)"'
            aResult = oParser.parse(stri, sPattern)
            if (aResult[0] == True):
                url=[]
                qua=[]
                
                for aEntry in aResult[1]:
                    url.append(aEntry[0])
                    qua.append(aEntry[1])

            api_call = dialog().VSselectqual(qua, url)

            if (api_call):
                return True, api_call

        return False, False