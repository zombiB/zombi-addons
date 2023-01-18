# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager
from resources.lib.parser import cParser
 
SITE_IDENTIFIER = 'alarabiya'
SITE_NAME = 'Alarabiya'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'https://www.alarabiya.net/'
 
DOC_NEWS = ('https://www.alarabiya.net/programs/documentaries', 'showMovies')

 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام وثائقية', 'doc.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()
    
def showMovies(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 
# ([^<]+) .+? (.+?)
    sPattern = '<a class="list-item-link" href="(.+?)" title="(.+?)">.+?<img src="(.+?)" width='

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1]
            sThumb = aEntry[2]
            siteUrl = URL_MAIN+aEntry[0]
            sDesc = ''
			
			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage != False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()
 
def __checkForNextPage(sHtmlContent):
    sPattern = ' <li >.+?<a href="(.+?)">'
	 # .+? ([^<]+) (.+?)
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0] is True:
        
        return URL_MAIN+aResult[1][0]


    return False

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
 
    sPattern = ',"contentUrl": "(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        for aEntry in aResult[1]:
            url = aEntry
            if url.startswith('//'):
                url = 'http:' + url
            sHosterUrl = url
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

                
    oGui.setEndOfDirectory() 