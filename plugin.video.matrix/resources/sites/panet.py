 #-*- coding: utf-8 -*-
#zombi https://github.com/zombiB/zombi-addons/
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, isMatrix
from resources.lib.parser import cParser
from resources.lib.player import cPlayer
import re
 
SITE_IDENTIFIER = 'panet'
SITE_NAME = 'panet'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'http://www.panet.co.il'


MOVIE_AR = ('http://www.panet.co.il/movies', 'showMovies')
MOVIE_TURK = ('http://www.panet.co.il/movies/genre/21/1', 'showMovies')
KID_MOVIES = ('http://www.panet.co.il/series/home/257/1', 'showEps')
SERIE_AR = ('http://www.panet.co.il/series/v1/category/19/1', 'showSeries')
SERIE_TR = ('http://www.panet.co.il/series/v1/category/17/1', 'showSeries')
SERIE_ASIA = ('http://www.panet.co.il/series/v1/category/20/1', 'showSeries')
SERIE_LATIN = ('https://www.panet.co.il/series/category/20/1', 'showSeries')
SERIE_GENRES = (True, 'showGenres')

RAMADAN_SERIES = ('http://www.panet.co.il/mosalsalat/category/81/1', 'showSeries')
REPLAYTV_NEWS = ('http://www.panet.co.il/series/category/27/1', 'showSeries')
NETS_NEWS = ('http://www.panet.co.il/series/category/2/1', 'showEps')
KID_CARTOON = ('http://www.panet.co.il/mosalsalat/category/15/1', 'showSeries')
URL_SEARCH = ('http://www.panet.co.il/search/result/', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'افلام عربي', 'news.png', oOutputParameterHandler)

    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showEps', 'افلام كارتون', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات رمضان 2016', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://www.panet.co.il/series/v1/category/19/1')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries' ,'مسلسلات مصرية', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://www.panet.co.il/series/v1/category/18/1')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries' ,'مسلسلات سورية - لبنانية', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://www.panet.co.il/series/v1/category/21/1')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries' ,'مسلسلات خليجية', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات مكسيكية وعالمية', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', 'series.png', oOutputParameterHandler)
    
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', NETS_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showEps', 'كليبات مضحكة', 'animesvostfr.png', oOutputParameterHandler)
    
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', KID_CARTOON[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'رسوم متحركة , برامج اطفال', 'animesvostfr.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'برامج ومنوعات', 'animesvostfr.png', oOutputParameterHandler)

            
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = 'http://www.panet.co.il/search/result/'+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
   
def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
	
    liste.append( ['مسلسلات سورية - لبنانية','http://www.panet.co.il/series/v1/category/18/1'] )

 
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
 

    sPattern = '<div class="panet-thumbnail"><a href="([^<]+)"><img src="([^<]+)" alt="([^<]+)"></a>.+?class="panet-genre"><a href=".+?">(.+?)</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = str(aEntry[2])
            siteUrl = URL_MAIN+str(aEntry[0])


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[1]))

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', aEntry[2], '', aEntry[1], aEntry[3], oOutputParameterHandler)
        
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
    sHtmlContent = oRequestHandler.request()
 
    sPattern = '<a class="panet-thumbnail" title="([^<]+)" href="([^<]+)""><img src="([^<]+)" alt="([^<]+)"><div class="panet-title"><h2>                                ([^<]+)                            </h2></div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[4]
            siteUrl = URL_MAIN+str(aEntry[1])
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[4]))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[2]))

            oGui.addTV(SITE_IDENTIFIER, 'showEps', aEntry[4], '', aEntry[2], aEntry[3], oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
def __checkForNextPage(sHtmlContent):
    sPattern = 'class="active"><a href=".+?">.+?</a></li><li><a href="(.+?)">'
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if (aResult[0] == True):
        aResult = URL_MAIN+aResult[1][0]
        #print aResult[1][0]
        return aResult

    return False
  
def showEps():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'href="/mosalsalat/home/(.+?)"><img src="(.+?)" alt="(.+?)"><div class="panet-title">(.+?)</div><div class="panet-info">(.+?)</'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            siteUrl = URL_MAIN+'/mosalsalat/home/'+str(aEntry[0])
            sTitle = sMovieTitle+str(aEntry[2]).replace("الحلقة "," E").replace("حلقة "," E")

 
            #print sUrl
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[1]))

            

 
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', aEntry[1], '', oOutputParameterHandler)
 
        progress_.VSclose(progress_)
       
    oGui.setEndOfDirectory()
    	
def showHosters():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    #recup du lien mp4
    sPattern = 'meta itemprop="contentURL" content="([^<]+)" />'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        
        sUrl = str(aResult[1][0])
                 
        #on lance video directement
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setTitle(sMovieTitle)
        oGuiElement.setMediaUrl(sUrl)
        oGuiElement.setThumbnail(sThumbnail)

        oPlayer = cPlayer()
        oPlayer.clearPlayList()
        oPlayer.addItemToPlaylist(oGuiElement)
        oPlayer.startPlayer()
        return
    
    else:
        return

    oGui.setEndOfDirectory()
