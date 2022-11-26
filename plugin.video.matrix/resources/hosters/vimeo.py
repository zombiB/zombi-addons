#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog
from resources.lib.comaddon import VSlog

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vimeo', 'Vimeo')

    def __getIdFromUrl(self, sUrl):
        sPattern = 'vimeo\.com\/(?:event\/)?([0-9]+)'
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if aResult[0] is True:
            return aResult[1][0]

        return ''

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        api_call = False
        oParser = cParser()
        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('Host', 'vimeo.com')
        oRequest.addHeaderEntry('Referer', 'https://arabicfile.blogspot.com/')
        oRequest.addHeaderEntry('User-Agent', 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1')
        sHtmlContent = oRequest.request()

        sPattern = ";document.cookie='vuid='(.+?)';"
        aResult = oParser.parse(sHtmlContent, sPattern)
        VSlog(aResult)
        scook = ''
    
        if (aResult[0]):
            scook = aResult[1][0]
            scook = scook.replace("+encodeURIComponent('","").replace("') +","")
        cook = 'vuid='+scook
        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('Host', 'vimeo.com')
        oRequest.addHeaderEntry('Referer', 'https://arabicfile.blogspot.com/')
        oRequest.addHeaderEntry('User-Agent', 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1')
        sHtmlContent = oRequest.request()

        sPattern = 'data-clip-id="(.+?)">'
        aResult = oParser.parse(sHtmlContent, sPattern)

    
        if (aResult[0]):
            sId = aResult[1][0]
        web_url = 'https://player.vimeo.com/video/' + sId+'/config?autopause=0&background=0&badge=0&byline=0&bypass_privacy=1&referrer=https%3A%2F%2Farabicfile.blogspot.com%2F'

        oRequest = cRequestHandler(web_url)
        cook = oRequest.GetCookies()
        oRequest.addHeaderEntry('Referer', 'https://vimeo.com/')
        oRequest.addHeaderEntry('User-Agent', 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1')
        sHtmlContent = oRequest.request()
        sPattern =  '"origin":"(.+?)","url":"(.+?)",'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        VSlog(aResult)

        if aResult[0] is True:
            #initialisation des tableaux
            url=[]
            qua=[]

            #Remplissage des tableaux
            for i in aResult[1]:
                url.append(str(i[1]))
                qua.append(str(i[0]))

            #tableau
            api_call = dialog().VSselectqual(qua, url)

            if api_call:
                return True, api_call+ '|Referer=https://arabicfile.blogspot.com/'

            return False, False
