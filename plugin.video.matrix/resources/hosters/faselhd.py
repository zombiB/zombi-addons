#coding: utf-8
# https://github.com/MatrixFlix/Dist/blob/main/repo/plugin.video.matrixflix/resources/hosters/faselhd.py

import base64
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.sites.faselhd import decode_page
from resources.lib.comaddon import dialog, VSlog, addon, siteManager
from resources.lib import random_ua
import xbmcgui
UA = random_ua.get_phone_ua()

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'faselhd', 'FaselHD', 'gold')

    def isDownloadable(self):
        return True

    def _getMediaLinkForGuest(self, autoPlay = False):
        api_call = self._url
        VSlog(self._url)
        oParser = cParser()
     #   xbmcgui.Dialog().ok("sHtmlContent",str(self._url )) 
  
     #   xbmcgui.Dialog().ok("","") 
       


        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('user-agent',UA)
        sHtmlContent = oRequest.request()
        if 'adilbo' in sHtmlContent:
         sHtmlContent = decode_page(sHtmlContent)
     #    xbmcgui.Dialog().ok("sHtmlContent",str(sHtmlContent)) 


        sPattern = 'data-url="([^<]+)">([^<]+)</button>' 
        aResult = oParser.parse(sHtmlContent, sPattern)	
       
        if aResult[0]:
            sLink = []
            sQual = []
            for aEntry  in aResult[1]:
                sLink.append(str(aEntry [0]))
                sQual.append(str(aEntry [1].upper()))
            api_call = dialog().VSselectqual(sQual, sLink)
            pass
        sPattern =  'videoSrc = ["\']([^"\']+)["\']' 
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                api_call = aEntry


        if api_call:
            return True, api_call + '|User-Agent=' + UA

        return False, False