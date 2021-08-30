#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import dialog
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
import json
UA = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'fajerlive'
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
        return 'fajerlive'

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

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        VSlog(self.__sUrl)

        url = 'https://fajer.live/api/source/' + self.__sUrl.rsplit('/', 1)[1]

        postdata = 'r=&d=fajer.live'

        oRequest = cRequestHandler(url)
        oRequest.setRequestType(1)
        oRequest.addHeaderEntry('User-Agent', UA)
        # oRequest.addHeaderEntry('Accept', '*/*')
        # oRequest.addHeaderEntry('Accept-Encoding','gzip, deflate, br')
        # oRequest.addHeaderEntry('Accept-Language','fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        # oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
        oRequest.addHeaderEntry('Referer', self.__sUrl)
        oRequest.addParametersLine(postdata)

        sHtmlContent = json.loads(oRequest.request())
        if sHtmlContent:
            url = []
            qua = []
            for x in sHtmlContent['data']:
                url.append(x['file'])
                qua.append(x['label'])

            if (url):
                api_call = dialog().VSselectqual(qua, url)

        if (api_call):
            return True, api_call + '|User-Agent=' + UA + '&Referer=' + self.__sUrl+ '&Origin=https://fajer.live' +'&verifypeer=false'

        return False, False