#-*- coding: utf-8 -*-

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'anonfile', 'Generic')

    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self):
        
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        VSlog(self._url)

        
        oParser = cParser()
        
            # (.+?) .+?
        sPattern = 'class="btn btn-primary btn-block btn-download-quality" href="(.+?)">(.+?)</a>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        api_call = False

        if aResult[0] is True:
            
            #initialisation des tableaux
            url=[]
            qua=[]
            
            #Replissage des tableaux
            for i in aResult[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))

            api_call = dialog().VSselectqual(qua, url)

            if api_call:
                return True, api_call
        
            # (.+?) .+?
        sPattern = 'class="btn btn-.+?".+?href="([^<]+)">'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        api_call = False

        if aResult[0] is True:
            api_call = aResult[1][0]

            if api_call:
                return True, api_call + '|User-Agent=' + UA
        
            # (.+?) .+?
        sPattern = "class='btn btn-.+?' href='(.+?)'>"
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        api_call = False

        if aResult[0] is True:
            api_call = aResult[1][0]

            if api_call:
                return True, api_call + '|User-Agent=' + UA
        
            # (.+?) .+?
        sPattern = 'href="([^<]+)"><img'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        api_call = False

        if aResult[0] is True:
            api_call = aResult[1][0]

            if api_call:
                return True, api_call + '&Referer=' + self._url
        
            # (.+?) .+?
        sPattern = '<meta property="og:video" content="(.+?)">'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        api_call = False

        if aResult[0] is True:
            api_call = aResult[1][0]

            if api_call:
                return True, api_call + '&Referer=' + self._url
        sPattern = 'file:"(.+?)",label:"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        api_call = False

        if aResult[0] is True:
            api_call = aResult[1][0]

            if api_call:
                return True, api_call + '&Referer=' + self._url
        sPattern = 'src: "(.+?)", type: "application/x-mpegURL'
        aResult = oParser.parse(sHtmlContent, sPattern)
        VSlog(aResult)
        
        api_call = False

        if aResult[0] is True:
            api_call = aResult[1][0]

            if api_call:
                return True, api_call 

        return False, False
        
