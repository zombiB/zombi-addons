#-*- coding: utf-8 -*-
#zombi https://github.com/zombiB/zombi-addons/
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress
import re

SITE_IDENTIFIER = 'btolat'
SITE_NAME = 'btolat'
SITE_DESC = 'sport vod'

URL_MAIN = 'https://www.btolat.com'
SPORT_FOOT = ('https://www.btolat.com/video', 'showMovies')

SPORT_SPORTS = ('http://', 'load')

FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)  
            
    oGui.setEndOfDirectory()
  
def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
            sUrl = ''  
            showMovies(sUrl)
            oGui.setEndOfDirectory()
            return  

 
def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.replace('&quot;', '"')
	 # .+? ([^<]+) 
    sPattern = '<h1 class="title">([^<]+)</h1>.+?<a href="([^<]+)">.+?data-original="([^<]+)" alt='
   
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            sUrl = str(aEntry[1])
            sUrl = URL_MAIN+sUrl
            sTitle = str(aEntry[0])
            sInfo = ""
            sThumbnail = aEntry[2]
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, 'doc.png', sThumbnail, sInfo, oOutputParameterHandler)

        progress_.VSclose(progress_)
            
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = ""
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        aResult = URL_MAIN+aResult[1][0]
        return aResult

    return False

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    oParser = cParser()

    sPattern =  "'true' src='(.+?)'"
    aResult = oParser.parse(sHtmlContent,sPattern)
    if (aResult[0] == True):
        m3url = aResult[1][0] 
        oRequest = cRequestHandler(m3url)
        sHtmlContent2 = oRequest.request()
    oParser = cParser()
    
 
    sPattern = ",src:{hls:'([^<]+)'}" 
    aResult = oParser.parse(sHtmlContent2, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            url = str(aEntry)
            if url.startswith('//'):
                url = 'http:' + url
            sHosterUrl = url
			
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

        progress_.VSclose(progress_) 


                
    oGui.setEndOfDirectory()    