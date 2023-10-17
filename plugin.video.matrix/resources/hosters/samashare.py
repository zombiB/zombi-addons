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
        iHoster.__init__(self, 'samashare', 'samashare')
			
    def setUrl(self, sUrl):
        self._url = str(sUrl)
        #lien embed obligatoire
        if not 'embed-' in self._url:
            self._url = self._url.rsplit('/', 1)[0] + '/embed-' + self._url.rsplit('/', 1)[1]

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        api_call = False

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        from resources.lib.comaddon import dialog
        oDialog = dialog()
        if 'File was deleted' in sHtmlContent:
            oDialog.VSerror("لم يعد الملف متاحًا حيث انتهت صلاحيته أو تم حذفه.")
            return

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


        if api_call:
            return True, api_call + '|User-Agent=' + UA

        return False, False