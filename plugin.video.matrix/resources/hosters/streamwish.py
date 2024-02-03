#-*- coding: utf-8 -*-
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog, dialog
import re

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'streamwish', 'streamwish')
			
    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        api_call = ''

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        oParser = cParser()

        sPattern = 'file:"(https.+?)"'
        aResult = re.findall(sPattern, sHtmlContent)
        if aResult:
           api_call = aResult[0]  # fichier master valide pour la lecture
           oRequestHandler = cRequestHandler(api_call)
           sHtmlContent2 = oRequestHandler.request()
           list_url = []
           list_q = []
           oParser = cParser()
           sPattern = 'PROGRAM.*?BANDWIDTH.*?RESOLUTION=(\d+x\d+).*?(https.*?m3u8)'
           aResult = oParser.parse(sHtmlContent2, sPattern)
           if aResult[0]:
              for aEntry in aResult[1]:
                  list_url.append(aEntry[1])
                  list_q.append(aEntry[0])
              if list_url:
                 api_call = dialog().VSselectqual(list_q, list_url)
       

        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        from resources.lib.util import Quote
        import unicodedata

        if aResult[0]:
            data = aResult[1][0]
            data = unicodedata.normalize('NFD', data).encode('ascii', 'ignore').decode('unicode_escape')
            sHtmlContent2 = cPacker().unpack(data)
      # (.+?) ([^<]+) .+?

            sPattern = 'wurl="(.+?)";'
            aResult = oParser.parse(sHtmlContent2, sPattern)
            if aResult[0]:
                api_call = aResult[1][0] 
                if api_call.startswith('//'):
                   api_call = 'http:' + api_call

            sPattern = 'file:"(.+?)"'
            aResult = oParser.parse(sHtmlContent2, sPattern)
            if aResult[0]:
                api_call = aResult[1][0] 

        if api_call:
            return True, api_call

        return False, False