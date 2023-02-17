#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog

class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'dailymotion', 'dailymotion')

    def isDownloadable(self):
        return True

    def setUrl(self, sUrl):
        self._url = str(sUrl)
        if not "metadata" in self._url:
            if 'embed/video' in self._url:
                self._url = "https://www.dailymotion.com/player/metadata/video/" + self._url.split('/')[5]
            elif '/swf/video' in self._url:
                self._url = "https://www.dailymotion.com/player/metadata/video/" + self._url.split('/')[5]
            else:
                self._url = "https://www.dailymotion.com/player/metadata/video/" + self._url.split('/')[4]                

    def _getMediaLinkForGuest(self):
        api_call = False
        url=[]
        qua=[]

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        VSlog(self._url)

        oParser = cParser()

        sPattern =  '{"type":"application.+?mpegURL","url":"([^"]+)"}'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            oRequest = cRequestHandler(aResult[1][0])
            oRequest.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0')
            oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
            sHtmlContent = oRequest.request()
            cookies = oRequest.GetCookies() 

            sPattern = 'NAME="([^"]+)"(,PROGRESSIVE-URI="([^"]+)"|http(.+?)\#)'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                for aEntry in reversed(aResult[1]):
                    quality = aEntry[0].replace('@60', '')
                    if quality not in qua:
                        qua.append(quality)
                        link = aEntry[2] if aEntry[2]  else 'http' + aEntry[3]
                        url.append(link)

            api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call+ '|Referer=' +self._url+'&cookie='+cookies

        return False, False