#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog
from resources.lib.util import urlEncode

class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'dailymotion', 'Dailymotion')

    def isDownloadable(self):
        return True

    def setUrl(self, sUrl):
        self._url = str(sUrl)
        self.embedder = self._url

        if "metadata" not in self._url:
            url_path = self._url.split('?')[0]

            if 'embed/video' in url_path or '/swf/video' in url_path:
                video_id = url_path.split('/')[5]
            else:
                video_id = url_path.split('/')[4]

            self._url = (
                f"https://www.dailymotion.com/player/metadata/video/{video_id}"
                f"?embedder={self.embedder}"
            )

    def _getMediaLinkForGuest(self, autoPlay = False):
        api_call = False
        url=[]
        qua=[]

        oRequest = cRequestHandler(self._url)
        oRequest.enableCache(False)
        sHtmlContent = oRequest.request()
        VSlog(self._url)

        oParser = cParser()

        sPattern =  '{"type":"application.+?mpegURL","url":"([^"]+)"}'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            api_call = aResult[1][0]
            oRequest = cRequestHandler(api_call)
            oRequest.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0')
            oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
            oRequest.enableCache(False)
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
            return True, api_call+ '|Referer=https://www.dailymotion.com/'

        return False, False