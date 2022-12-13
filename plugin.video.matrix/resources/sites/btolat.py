# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, siteManager

SITE_IDENTIFIER = 'btolat'
SITE_NAME = 'Btolat'
SITE_DESC = 'sport vod'

URL_MAIN = 'https://www.btolat.com/'

SPORT_FOOT = ('https://www.btolat.com/video', 'showMovies')

SPORT_SPORTS = ('http://', 'load')

def load():
    oGui = cGui() 

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_FOOT[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أهداف و ملخصات ', 'sport.png', oOutputParameterHandler)

    oGui.setEndOfDirectory() 
			
def showMovies(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
	 # .+? ([^<]+) 
    sPattern = '<h1 class="title">([^<]+)</h1>.+?<a href="([^<]+)">.+?data-original="([^<]+)" alt='
   
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
            sUrl = aEntry[1]
            sUrl = URL_MAIN+sUrl
            sTitle = aEntry[0]
            sDesc = ""
            sThumb = aEntry[2]
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, 'doc.png', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
            
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage != False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = ""
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        aResult = URL_MAIN+aResult[1][0]
        return aResult

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

    sPattern =  "'true' src='(.+?)'"
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0] is True:
        m3url = aResult[1][0] 
        oRequest = cRequestHandler(m3url)
        sHtmlContent2 = oRequest.request()
    
 
    sPattern = ",src:{hls:'(.+?)'}" 
    aResult = oParser.parse(sHtmlContent2, sPattern)
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