#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog, VSlog
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker



UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'govid', 'CimaClub', 'gold')
			
    def setUrl(self, sUrl):
        self._url = str(sUrl)

    def _getMediaLinkForGuest(self):
        sReferer = ""
        if '|Referer=' in self._url:
            surl = self._url.split('|Referer=')[0]
        else:
            surl = self._url
        if '|Referer=' in self._url:
            sReferer = self._url.split('|Referer=')[1]
        else:
            sReferer = self._url

        oRequest = cRequestHandler(surl)
        oRequest.addHeaderEntry('Referer', sReferer)
        oRequest.addHeaderEntry('User-Agent', UA)
        sHtmlContent = oRequest.request()
        oParser = cParser()

       # (.+?) .+? ([^<]+)
        sPattern =  '"playbackUrl": "(.+?)"' 
        aResult = oParser.parse(sHtmlContent,sPattern)
        if aResult[0]:
            url2 = aResult[1][0].replace("hhttps","https").replace('api.govid.co/api','go.telvod.site/api')

            oRequest = cRequestHandler(url2)
            oRequest.addHeaderEntry('Referer', surl)
            oRequest.addHeaderEntry('User-Agent', UA)
            sHtmlContent2 = oRequest.request()
            sPattern = ',NAME="(.+?)",.+?(https.+?m3u8)'
            aResult = oParser.parse(sHtmlContent2, sPattern)
            list_url=[]
            list_q=[]
            for aEntry in aResult[1]:
                list_q.append(aEntry[0]) 
                list_url.append(aEntry[1]) 
				
            api_call = dialog().VSselectqual(list_q,list_url)


            if api_call:
                return True, api_call+ '|User-Agent=' + UA+'&AUTH=TLS&verifypeer=false' + '&Referer=' + surl

        sPattern =  '<a target="_blank".+?href="([^"]+)' 
        aResult = oParser.parse(sHtmlContent,sPattern)
        VSlog(aResult)
        if aResult[0]:
            for aEntry in aResult[1]:            
                api_call = aEntry

                if api_call:
                   return True, api_call+ '|User-Agent=' + UA+'&AUTH=TLS&verifypeer=false' + '&Referer=' + surl

        sPattern =  'file:"(.+?)",label' 
        aResult = oParser.parse(sHtmlContent,sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
            
                api_call = aEntry.replace('["','').replace('"]','')


                if api_call:
                   return True, api_call+ '|User-Agent=' + UA+'&AUTH=TLS&verifypeer=false' + '&Referer=' + surl

        sPattern =  'sources: (.+?),' 
        aResult = oParser.parse(sHtmlContent,sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
            
                api_call = aEntry.replace('["','').replace('"]','')


                if api_call:
                   return True, api_call+ '|User-Agent=' + UA+'&AUTH=TLS&verifypeer=false' + '&Referer=' + surl

        return False, False