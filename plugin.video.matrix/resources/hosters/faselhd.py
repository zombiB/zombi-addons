#coding: utf-8
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog
from resources.lib.comaddon import progress, VSlog
import re
import base64
UA = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'faselhd'
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
        return 'faselhd'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''

    def __getIdFromUrl(self):
        return ''

    def __modifyUrl(self, sUrl):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = sUrl

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        VSlog("getMediaLink")
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        api_call = ''

        oRequest = cRequestHandler(self.__sUrl)
        oRequest.addHeaderEntry('Referer',self.__sUrl)
        sHtmlContent = oRequest.request()

        #VSlog(sHtmlContent)
        #print sHtmlContent
        oParser = cParser()
        sPattern = ";var hide_my_HTML.+?=([^<]+);.+?var"
        aResult = oParser.parse(sHtmlContent, sPattern)
        #VSlog(aResult)
        if (aResult[0] == True):

            media =  aResult[1][0]

            media =  media.replace(";var _0x0dd0=['fromCharCode','replace','write','forEach'];(function(_0x4792fc,_0x352491){var _0xd23cef=function(_0x332eb8){while(--_0x332eb8){_0x4792fc['push'](_0x4792fc['shift']());}};_0xd23cef(++_0x352491);}(_0x0dd0,0x1cf))",'')
            media =  media.replace("'",'')
            media =  media.replace("+",'')
            media =  media.replace("\n",'') 
            media =  media.split('.') 
            for elm in media: 
				media2 = base64.b64decode(elm+'==')


            print media2


            #cPacker decode
            from resources.lib.packer import cPacker
            media = cPacker().unpack(media)
            #print media 
            #VSlog(media)
            if (media):

                sPattern = '"src":"(.+?)","label":"(.+?)",'
                aResult = oParser.parse(media, sPattern)
                #VSlog(aResult)
                if (aResult[0] == True):
                #initialisation des tableaux
                    url=[]
                    qua=[]
                #Remplissage des tableaux
                    for i in aResult[1]:
                        url.append(str(i[0]))
                        qua.append(str(i[1]))
                #Si une seule url
                    api_call = dialog().VSselectqual(qua, url)

        if (api_call):
            return True, api_call+'|User-Agent=' + UA + '&Referer=' + self.__sUrl
        print api_call 

        return False, False
