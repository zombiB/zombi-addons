#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog, VSlog
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker



UA = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36 Edg/114.0.1823.67'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'cimanow', 'CimaNow', 'gold')
			
    def setUrl(self, sUrl):
        self._url = str(sUrl).replace('rrsrrs','cimanow')
        VSlog(self._url)
    def _getMediaLinkForGuest(self):
        
        sReferer = "https://cimanow.cc/"
        host = self._url.split('/e')[0]
        surl = self._url

        oRequest = cRequestHandler(surl)
        oRequest.addHeaderEntry('Referer', sReferer)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.disableSSL()
        sHtmlContent = oRequest.request()
        oParser = cParser()
        #VSlog(sHtmlContent)
       # (.+?) .+? ([^<]+)

        sPattern =  '<source src="(.+?)" type="video/mp4" size="(.+?)">' 
        aResult = oParser.parse(sHtmlContent,sPattern)
        list_url=[]
        list_q=[]
        for aEntry in aResult[1]:
                list_q.append(aEntry[1]) 
                list_url.append(aEntry[0]) 
				
        api_call = dialog().VSselectqual(list_q,list_url)
        api_call = host + api_call.replace(' ', '%20') +'|AUTH=TLS&verifypeer=false' + '&Referer=' + host

        if api_call:
                    return True, api_call

        return False, False