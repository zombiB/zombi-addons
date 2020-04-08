#-*- coding: utf-8 -*-

#Zombi.

from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress
from resources.lib.util import cUtil

import re,urllib,urllib2,xbmc

SITE_IDENTIFIER = 'jaewinter_com'
SITE_NAME = 'jaewinter'
SITE_DESC = 'vod'

URL_MAIN = 'https://www.jaewinter.co'
MOVIE_ASIAN = ('https://www.jaewinter.co/category/%d8%af%d8%b1%d8%a7%d9%85%d8%a7%d8%aa-%d9%85%d8%aa%d8%b1%d8%ac%d9%85/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d9%85%d8%aa%d8%b1%d8%ac%d9%85%d8%a9/', 'showMovies')
SERIE_ASIA = ('https://www.jaewinter.co/category/%d8%af%d8%b1%d8%a7%d9%85%d8%a7%d8%aa-%d9%85%d8%aa%d8%b1%d8%ac%d9%85/', 'showMovies')
SERIE_GENRES = (True, 'showGenres')

REPLAYTV_NEWS = ('http://www.jaewinter.com/category/showtv/', 'showMovies')


URL_SEARCH = ('http://www.jaewinter.com/?s=', 'showMovies')
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
        sUrl = 'http://www.jaewinter.com/?s='+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return 
   
def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ["chinese series","http://www.jaewinter.com/category/%D9%82%D8%A7%D8%A6%D9%85%D8%A9-%D8%A7%D9%84%D8%AF%D8%B1%D8%A7%D9%85%D8%A7/%D8%AF%D8%B1%D8%A7%D9%85%D8%A7-%D8%B5%D9%8A%D9%86%D9%8A%D8%A9-%D9%88%D8%AA%D8%A7%D9%8A%D9%88%D8%A7%D9%86%D9%8A%D8%A9/"] )
    liste.append( ["korean series","https://www.jaewinter.co/category/%D9%82%D8%A7%D8%A6%D9%85%D8%A9-%D8%A7%D9%84%D8%AF%D8%B1%D8%A7%D9%85%D8%A7/%D8%AF%D8%B1%D8%A7%D9%85%D8%A7-%D9%83%D9%88%D8%B1%D9%8A%D8%A9/"] )
    liste.append( ["japanese series","http://www.jaewinter.com/category/%D9%82%D8%A7%D8%A6%D9%85%D8%A9-%D8%A7%D9%84%D8%AF%D8%B1%D8%A7%D9%85%D8%A7/%D8%AF%D8%B1%D8%A7%D9%85%D8%A7-%D9%8A%D8%A7%D8%A8%D8%A7%D9%86%D9%8A%D8%A9/"] )
    liste.append( ["thai series","http://www.jaewinter.com/category/%D9%82%D8%A7%D8%A6%D9%85%D8%A9-%D8%A7%D9%84%D8%AF%D8%B1%D8%A7%D9%85%D8%A7/%D8%AF%D8%B1%D8%A7%D9%85%D8%A7-%D8%AA%D8%A7%D9%8A%D9%84%D8%A7%D9%86%D8%AF%D9%8A%D8%A9/"] )

    
	            
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 
    



def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

# ([^<]+) .+?
    sPattern = '<div style="background-image: url([^<]+)" class.+?<a href="([^<]+)" class="all-over-thumb-link"><span class="screen-reader-text">([^<]+)</span></a>.+?desc">([^<]+)</div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = aEntry[2].decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            sThumbnail = str(aEntry[0]).replace('(','').replace(')','')
 
            siteUrl = aEntry[1]
            sInfo = str(aEntry[3]).decode("utf8")
            sInfo = cUtil().unescape(sInfo).encode("utf8")
            sInfo = '[COLOR yellow]'+sInfo+'[/COLOR]'
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)

        progress_.VSclose(progress_)
            
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def showSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('<span class="likeThis">', '').replace('</span>','')


    sPattern = '<h2 class="post-box-title"><a href="(.+?)">(.+?)</a>.+?<img width=".+?" height=".+?" src="(.+?)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            sUrl = str(aEntry[0])
            if not 'http' in sUrl:
                sUrl = str(URL_MAIN) + sUrl
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[2]))
            oGui.addMovie(SITE_IDENTIFIER, 'showEpisodes', aEntry[1], '', aEntry[2], '', oOutputParameterHandler)

        progress_.VSclose(progress_)
            
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()
		
def showEpisodes():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()


 
    sPattern = '<h4 class="entry-title">.+?<a href="([^<]+)" rel="bookmark">([^<]+)</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1]
            siteUrl = aEntry[0]
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, '', oOutputParameterHandler)
        
        progress_.VSclose(progress_)
       
    oGui.setEndOfDirectory()
	    # ([^<]+) .+?
def __checkForNextPage(sHtmlContent):
    sPattern = 'class="pages-nav-item" href="([^<]+)" title'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        #print aResult[1][0]
        return aResult[1][0]

    return False
    

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();


    #sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/plugins/like.php','').replace('<iframe src="http://www.facebook.com/plugins/likebox.php','')
               
    # ([^<]+) .+?    
    sPattern = 'data-lazy-src="([^<]+)"></iframe>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
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
    
