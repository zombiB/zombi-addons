#-*- coding: utf8 -*-
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import VSlog, xbmcgui
from resources.lib.gui.gui import cGui
from resources.hosters.hoster import iHoster
import  re

from resources.lib.packer import cPacker

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'thevid', 'Thevid')

    def _getMediaLinkForGuest(self): 
        VSlog(self._url)
                    
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        if 'Not Found' in sHtmlContent:
        	dialog().VSinfo("404 Not Found")
        
        oParser = cParser()
              
        #Dean Edwards Packer
        sPattern = "(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            sUnpacked = cPacker().unpack(aResult[1][0])
        
        #fh = open('c:\\test.txt', "w")
        #sfilea="http://s005.thevid.net/v/892925a1c517aa9b70944ec53ec94aa3.mp4?e=1533859029&sa=CgOo0MoVWKjHhnVBzRFrAw&st=kW53T1epyxSYivAYzfvSxg";
        
        if (sUnpacked):

            sPattern ='var vldAb="(.+?)";'
            aResult = oParser.parse(sUnpacked, sPattern)
            
            #print aResult
            
            if aResult[0] is True:
                return True , aResult[1][0]
        
        
        return False, False
        
        
