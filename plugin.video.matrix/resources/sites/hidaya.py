# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, siteManager
from resources.lib.parser import cParser
 
SITE_IDENTIFIER = 'hidaya'
SITE_NAME = 'hidaya'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

ISLAM_QURAN = ('https://hidaya.tn/tilawet/ajax_tilawet.php?search=&page=1', 'showMovies')

 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ISLAM_QURAN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'ISLAM_QURAN', 'search.png', oOutputParameterHandler)

            
    oGui.setEndOfDirectory()
  
def showMovies(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    b = sUrl.split('=')[2]
    b = int(b)
    for b in range(b,b+5):
        sUrl = "https://hidaya.tn/tilawet/ajax_tilawet.php?search=&page="+str(b)
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
 # ([^<]+) .+?

        sPattern = "<div class='card-header text-center text-body'>([^<]+)</div>.+?src='http://img.youtube.com/vi/([^<]+)/hqdefault.jpg' alt='Youtube Video' .+?<p class='card-text text-right'>([^<]+)</p></a>"

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
	
        if aResult[0] is True:
           for aEntry in aResult[1]:
        
               url = "https://www.youtube.com/watch?v="+aEntry[1]
               sTitle = aEntry[0]+' [COLOR yellow] '+aEntry[2]+' [/COLOR]'
               sThumb = "http://img.youtube.com/vi/"+aEntry[1]+"/hqdefault.jpg"
				
				

               if url.startswith('//'):
                  url = 'https:' + url
            
               sHosterUrl = url 
               oHoster = cHosterGui().checkHoster(sHosterUrl)
               if oHoster != False:
                  sDisplayTitle = sTitle
                  oHoster.setDisplayName(sDisplayTitle)
                  oHoster.setFileName(sTitle)
                  cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
				

 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage != False:
           oOutputParameterHandler = cOutputParameterHandler()
           oOutputParameterHandler.addParameter('siteUrl', sNextPage)
           oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = "<li class='page-item active'><a class='page-link' onclick=.+?</a></li><li class='page-item'><a class='page-link' onclick=.+?>([^<]+)</a></li>"
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0] is True:
        return "https://hidaya.tn/tilawet/ajax_tilawet.php?search=&page=" + aResult[1][0]

    return False

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    oParser = cParser()       
    sPattern =  '<a href="([^<]+)".+?class="download-link"' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0] is True:
        m3url =  aResult[1][0]
        oRequest = cRequestHandler(m3url)
        sHtmlContent = oRequest.request()

    # (.+?) .+? ([^<]+)
               
    sPattern = '<source.+?src="(.+?)".+?type="video/mp4".+?size="(.+?)".+?/>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if aResult[0] is True:
        for aEntry in aResult[1]:
        
            url = aEntry[0]
            sTitle = aEntry[1].replace('"',"")
				
            sTitle = '[COLOR yellow]'+sTitle+'p[/COLOR]'
            if url.startswith('//'):
               url = 'https:' + url
            
            sHosterUrl = url 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
               sDisplayTitle = sMovieTitle+sTitle
               oHoster.setDisplayName(sDisplayTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
				
                
    oGui.setEndOfDirectory()