#-*- coding: utf-8 -*-
#zombi.(@geekzombi)
import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress
from resources.lib.parser import cParser
 
SITE_IDENTIFIER = 'yallalive'
SITE_NAME = 'yallalive'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'http://www.yalla-shoot.com/mobile/'

SPORT_FOOT = ('http://www.yalla-shoot.com/mobile/index.php', 'showMovies')
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Search', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_FOOT[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'رياضة', 'sport.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
		
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 
      # (.+?) ([^<]+) .+?
    sPattern = '<a href="([^<]+)" class="matsh_live"><div.+?class="fc_name">([^<]+)</td>.+?class="fc_name">([^<]+)</td>.+?<span class="matsh.+?">([^<]+)</span> </td>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[2] +' vs ' + aEntry[1] 
            sThumbnail = ""
            siteUrl = URL_MAIN + aEntry[0]
            sInfo = aEntry[3]
            if 'جارية' in sInfo:
                sTitle = '[COLOR yellow]'+sTitle+' [/COLOR]'
			
		
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()
# ([^<]+) .+?
def __checkForNextPage(sHtmlContent):
    sPattern = '<td><a href="([^<]+)"><img src="https://www.yalla-shoot.com/img/yesterday.png"></a></td>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        aResult = aResult[1][0]
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
    sPattern = '<font color=.+?>([^<]+)</font>.+?src="(.+?)"' 
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            url = aEntry[1]
            sTitle = aEntry[0]
            if url.startswith('//'):
                url = 'https:' + url
            if 'ok.php' in url:
                url = url.split('ok.php?id=', 1)[1]
                url = 'http://ok.ru/videoembed/' + url
            
                
            sHosterUrl = url
            sHosterUrl = sHosterUrl.replace('https://www.yallashahed.com/youtube.php?ytid=','https://www.youtube.com/embed/')
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

                
    oGui.setEndOfDirectory()    
