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


SITE_IDENTIFIER = 'rotana'
SITE_NAME = 'Rotana'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_AR = (URL_MAIN +'/vod-movies', 'showMovies')
URL_SEARCH = (URL_MAIN +'/?s=', 'showSeries')
URL_SEARCH_MOVIES = (URL_MAIN +'/?s=', 'showMoviesSearch')
FUNCTION_SEARCH = 'showSeries'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Search', 'search.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عربية', 'film.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', "https://rotana.net/movies-genres/%d8%a3%d9%83%d8%b4%d9%86/")
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أكشن', 'film.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', "https://rotana.net/movies-genres/%d8%af%d8%b1%d8%a7%d9%85%d8%a7/")
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'دراما', 'film.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', "https://rotana.net/movies-genres/%d8%b1%d9%88%d9%85%d8%a7%d9%86%d8%b3%d9%8a/")
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'رومانسي', 'film.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', "https://rotana.net/movies-genres/%d9%83%d9%88%d9%85%d9%8a%d8%af%d9%8a%d8%a7/")
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'كوميديا', 'film.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', "https://rotana.net/vod-short-movies")
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام قصيرة', 'film.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', "https://rotana.net/vod-series-2")
    oGui.addDir(SITE_IDENTIFIER, 'showSerie', 'مسلسلات عربية', 'mslsl.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', "https://rotana.net/theatrical-plays")
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'مسرحيات', 'msrh.png', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText != False:
        sUrl = URL_MAIN +'/?s='+sSearchText
        showMoviesSearch(sUrl)
        oGui.setEndOfDirectory()
        return
		
def showMoviesSearch(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 # .+? ([^<]+)

    sPattern = '<img width=".+?" height=".+?" src="([^<]+)" class.+?<h2 class="elementor-heading-title elementor-size-default"><a href="([^<]+)">([^<]+)</a></h2>.+?<div class="elementor-widget-container">([^<]+)</div>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0] :
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if "vod" not in aEntry[1]:
                continue
 
            sTitle = aEntry[2]
            siteUrl = aEntry[1]
            sThumb = aEntry[0]
            sDesc = aEntry[3]
            sYear = ''

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
    if not sSearch:
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
 # .+? ([^<]+)

    sPattern = '<a href=(.+?)>.+?class="main_eps_img" src="([^<]+)" alt="([^<]+)" title='


    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0] :
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[2]
            siteUrl = aEntry[0].replace("'","")
            sThumb = aEntry[1]
            sDesc = ''
            sYear = ''

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage != False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
  
 
def __checkForNextPage(sHtmlContent):
    sPattern = '<li><a href="([^<]+)" rel="next">&raquo;</a></li></ul></div>'
	 #.+?([^<]+)
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0] :
        
        return aResult[1][0]

    return False

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    #.+? ([^<]+)
                     
    sPattern = "video([^<]+).player"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if aResult[0] :
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            
            sId = aEntry.replace("')","").replace("('","")              
            url = 'https://embed.hibridvod.app/video/'+sId
            sTitle = sMovieTitle  
            if url.startswith('//'):
                url = 'http:' + url
            
            sHosterUrl = url
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
				

        progress_.VSclose(progress_) 
    oGui.setEndOfDirectory()                