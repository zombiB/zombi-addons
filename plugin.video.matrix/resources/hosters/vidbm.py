#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#https://www.vidbm.com/emb.html?xxx=img.vidbm.com/xxx
#https://www.vidbm.com/embed-xxx.html?auto=1
#https://www.vidbm.com/embed-xxx.html
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.aadecode import decodeAA
from resources.lib.packer import cPacker
from resources.lib.aadecode import AADecoder
import re
from resources.lib.comaddon import VSlog

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:72.0) Gecko/20100101 Firefox/72.0'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'VidBM'
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
        return 'vidbm'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return False

    def setUrl(self, sUrl):
        self.__sUrl = re.sub('=img.vidbm.com/.+?','',str(sUrl))
        self.__sUrl = self.__sUrl.replace('embed-', '')
        self.__sUrl = self.__sUrl.replace('emb.html?', '')
        self.__sUrl = self.__sUrl.replace('.html?auto=1','')
        self.__sUrl = self.__sUrl.replace('.html','')
  
    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        url = self.__sUrl

        oRequest = cRequestHandler(url)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        
        #VSlog(self.__sUrl)

        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        #VSlog(sHtmlContent)
        oParser = cParser()
        
        api_call = False
        
        sPattern =  '(?:[>;]\s*)(ﾟωﾟ.+?\(\'_\'\);)'
        aResult = oParser.parse(sHtmlContent, sPattern)
         
		
        if aResult[0]:
            for i in aResult[1]:
                decoded = AADecoder(i).decode()

                r = re.search('file:"([^<]+)",', decoded, re.DOTALL | re.UNICODE)
                if r:
                    api_call = r.group(1)
                    break
        
        #VSlog(api_call)

        if (api_call):
            return True, api_call

        return False, False