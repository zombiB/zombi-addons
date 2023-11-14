#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#https://www.vidbm.com/emb.html?xxx=img.vidbm.com/xxx
#https://www.vidbm.com/embed-xxx.html?auto=1

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidshare', 'vidshare')

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        api_call = False

        sUrl = self._url
 
        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()
        from resources.lib.comaddon import dialog
        oDialog = dialog()
        if 'File is no longer available as it expired or has been deleted.' in sHtmlContent:
            oDialog.VSerror("لم يعد الملف متاحًا حيث انتهت صلاحيته أو تم حذفه.")
            return


        oParser = cParser()
       
        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
        aResult = oParser.parse(sHtmlContent,sPattern)
        if (aResult[0] == True):
            sHtmlContent = cPacker().unpack(aResult[1][0])
            sPattern = 'file:"(.+?)",label:".+?"}'
            aResult = oParser.parse(sHtmlContent,sPattern)
            if (aResult[0] == True):
                api_call = aResult[1][0] 

        sPattern = 'file:"(.+?)"}'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            api_call = aResult[1][0] +'|User-Agent=' + UA + '&Referer=' + self._url
                
        if (api_call):
            return True, api_call

        return False, False