#-*- coding: utf-8 -*-
import requests
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import VSlog
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
import  xbmcgui
import urllib.request
from bs4 import BeautifulSoup
from  resources.lib.cloudscraper2 import CloudScraper
import time
import re
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'mp4Play', 'Mp4Play')

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        sReferer = self._url
      
        #  sReferer=sReferer.replace("bgwp","bigwarp",).replace("https","http")
        res=requests.get( sReferer)
        con=res.text
        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('user-agent',UA)
        oRequest.addHeaderEntry('Referer',sReferer)
        sHtmlContent = oRequest.request()
       
    #    xbmcgui.Dialog().ok("aResult",str (sReferer))
        
        oParser = cParser()
        play_Js=None
        
        if "mp4plus" in sReferer : # (.+?) .+?
         sPattern =r'jwplayer\s*\([^)]*\)\s*\.setup\s*\(\s*{.*?}\s*\)'
      #  aResult = re.findall(sPattern, sHtmlContent, re.DOTALL)
         play_Js = oParser.parse(con, sPattern)
      # xbmcgui.Dialog().ok("aResult",str (con))
       
          
      
        
        if play_Js:
       #     data = aResult[1][0]
          #  sHtmlContent = cPacker().unpack(data)

         
         
         #   xbmcgui.Dialog().ok("aResult", "No script found")
            sPattern = 'file:"(.+?)"'
            aResult = oParser.parse(play_Js, sPattern)
        #    xbmcgui.Dialog().ok("x",str (aResult))
        #
        
        api_call = False

        if (aResult[0] == True):
        #    xbmcgui.Dialog().ok("aResult",  aResult[1][0])
            api_call = aResult[1][0]
            VSlog(api_call)

            if (api_call):
                return True, api_call + '|User-Agent=' + UA
        return False, False
        
