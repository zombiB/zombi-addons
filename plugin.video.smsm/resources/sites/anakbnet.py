#-*- coding: utf-8 -*-
#Venom.
#zombi(@zombigeek)
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
from resources.lib.util import cUtil
import urllib2,urllib,re
import unicodedata
 
SITE_IDENTIFIER = 'anakbnet'
SITE_NAME = 'anakbnet.com'
SITE_DESC = 'vod arab'
 
URL_MAIN = 'http://www.anakbnet.com/video/browse.php?c=3&p=1'


MOVIE_ANIME = ('http://www.anakbnet.com/video/browse.php?c=3&p=1', 'showMovies')
MOVIE_AR = ('http://www.anakbnet.com/video/browse.php?c=1&p=1', 'showMovies')
MOVIE_EN = ('http://www.anakbnet.com/video/browse.php?c=2&p=1', 'showMovies')


URL_SEARCH = ('http://www.anakbnet.com/aflam/search.php?t=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Films Recherche', 'search.png', oOutputParameterHandler)

 
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = 'http://www.anakbnet.com/aflam/search.php?t='+sSearchText
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

    #sPattern = '<a href="([^<]+)" title="([^<]+)" >.+?<img width=".+?" height=".+?" src="(.+?)"'
    sPattern = '<div class="icon">.+?<a href="([^<]+)"><img src="([^<]+)" width="85" height="110" title="([^<]+)" alt=".+?" border="0" /></a>.+?</div>.+?<div class="desc">.+?<p class="link"><a href=".+?">.+?</a></p>.+?<p>([^<]+)</p>'
	
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    #print aResult
		
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
 
            sTitle = unicode(aEntry[2], 'utf-8')#converti en unicode

            sTitle = sTitle.encode( "utf-8")
            
            #sTitle = cUtil().DecoTitle(sTitle)
           
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[1]))
		
           
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', aEntry[1], aEntry[3], oOutputParameterHandler)
 
        cConfig().finishDialog(dialog)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
 
 
def __checkForNextPage(sHtmlContent):
    sPattern = '<div class="pagination">.+?<b>.+?</b><a href="(.+?)".+?'

	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if (aResult[0] == True):
        sUrl = aResult[1][0]
        return sUrl
 
    return False
 
 
def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 
    sPattern = '<iframe rel="nofollow" src="(.+?)"[^<>]*><\/iframe>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
			
    #print aResult
 
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
				
            sHosterUrl = str(aEntry)
			
            #oHoster = __checkHoster(sHosterUrl)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
 
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
 
        cConfig().finishDialog(dialog)
 
    oGui.setEndOfDirectory()
