#-*- coding: utf-8 -*-
#Venom.
#zombi.(@geekzombi)
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
 
SITE_IDENTIFIER = 'serieswatch'
SITE_NAME = 'series4watch'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'http://www.series4watch.tv/'


MOVIE_AR = ('http://www.series4watch.tv/category/%D8%A3%D9%81%D9%84%D8%A7%D9%85-%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9-%D8%A3%D9%88%D9%86-%D9%84%D8%A7%D9%8A%D9%86/', 'showMovies')
MOVIE_EN = ('http://www.series4watch.tv/category/%D8%A3%D9%81%D9%84%D8%A7%D9%85-%D8%A3%D8%AC%D9%86%D8%A8%D9%8A%D8%A9-%D8%A3%D9%88%D9%86-%D9%84%D8%A7%D9%8A%D9%86/', 'showMovies')
MOVIE_ANIME = ('http://www.series4watch.tv/category/%D8%A3%D9%81%D9%84%D8%A7%D9%85-%D8%A5%D9%86%D9%85%D9%8A-%D9%85%D8%AF%D8%A8%D9%84%D8%AC%D8%A9/', 'showMovies')
MOVIE_ASIAN = ('http://www.series4watch.tv/type/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%A7%D8%B3%D9%8A%D9%88%D9%8A%D8%A9/', 'showMovies')
MOVIE_HI = ('http://www.series4watch.tv/category/%D8%A3%D9%81%D9%84%D8%A7%D9%85-%D9%87%D9%86%D8%AF%D9%8A/', 'showMovies')
MOVIE_TURK = ('http://www.series4watch.tv/category/%D8%A3%D9%81%D9%84%D8%A7%D9%85-%D8%AA%D8%B1%D9%83%D9%8A-%D8%A7%D9%88%D9%86-%D9%84%D8%A7%D9%8A%D9%86/', 'showMovies')
SERIE_NEWS = ('http://www.series4watch.tv/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%A3%D8%AC%D9%86%D8%A8%D9%8A%D8%A9-%D9%85%D9%85%D9%8A%D8%B2%D8%A9/', 'showMovies')
SERIE_EN = ('http://www.series4watch.tv/%D8%A7%D9%84%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA/', 'showSeasons')
REPLAYTV_NEWS = ('http://www.series4watch.tv/category/%D8%A8%D8%B1%D8%A7%D9%85%D8%AC-%D8%AA%D9%84%D9%8A%D9%81%D8%B2%D9%8A%D9%88%D9%86%D9%8A%D8%A9/', 'showMovies')
SPORT_NEWS = ('http://www.series4watch.tv/category/%D9%85%D8%B5%D8%A7%D8%B1%D8%B9%D8%A9-%D8%A3%D9%88%D9%86-%D9%84%D8%A7%D9%8A%D9%86/', 'showMovies')
URL_SEARCH = ('http://www.series4watch.tv/?s=', 'showMovies')
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
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANIME[0])
    oGui.addDir(SITE_IDENTIFIER, 'showEps', 'افلام كارتون', 'news.png', oOutputParameterHandler)

    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'برامج ومنوعات', 'animesvostfr.png', oOutputParameterHandler)

            
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = 'http://www.series4watch.tv/?s='+sSearchText
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
 
#(.+?)([^<]+)
    sPattern = '<div class="block_loop">.+?<a href="([^<]+)" title="([^<]+)">.+?<img width=".+?" height=".+?" src="([^<]+)" class'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
 
            sTitle = aEntry[1]
            siteUrl = str(aEntry[0])


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[2]))

            oGui.addMisc(SITE_IDENTIFIER, 'showLinks', aEntry[1], '', aEntry[2], '', oOutputParameterHandler)
        
        cConfig().finishDialog(dialog)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
		
def showSeasons(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 
#(.+?)([^<]+)
    sPattern = '<div class="title-post"><a href="([^<]+)" title="([^<]+)"><img src="([^<]+)">'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
 
            sTitle = aEntry[1]
            siteUrl = str(aEntry[0])


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[2]))

            oGui.addMisc(SITE_IDENTIFIER, 'showSeries', aEntry[1], '', aEntry[2], '', oOutputParameterHandler)
        
        cConfig().finishDialog(dialog)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 

 
def __checkForNextPage(sHtmlContent):
    sPattern = 'rel="next" href="(.+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if (aResult[0] == True):
        #print aResult[1][0]
        return aResult[1][0]

    return False
	
def showSeries():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
   
    oParser = cParser()
    sPattern = '<h1 class="title-news">(.+?)</h1><div class="block_loop">'
    sPattern = sPattern + '|' + '<a href="(.+?)" title="(.+?)">'
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    Saison = '0'
   
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
       
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
                        
            if aEntry[0]:
                Saison = str(aEntry[0]).replace('<strong>','').replace('</strong>','')
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addMisc(SITE_IDENTIFIER, 'showSeries', '[COLOR red]'+ Saison + '[/COLOR]', 'series.png', sThumbnail, aEntry[2], oOutputParameterHandler)

            else:
                sTitle = aEntry[2]
                sUrl= str(aEntry[1])
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addTV(SITE_IDENTIFIER, 'showLinks', sTitle, '', aEntry[0], '', oOutputParameterHandler)
    #(.+?)
    
 
        cConfig().finishDialog(dialog)
       
    oGui.setEndOfDirectory()	
  
def showLinks():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = "rtl post-template-default single single-post postid-([^<]+) single-format-standard"

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent.replace('\n',''))
    #fh.close()

    #print aResult
   
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            

        for i in range(0,7):
            sUrl = 'http://www.series4watch.tv/wp-content/themes/series4watch/server1.php?server='+str(i)+'&p='+str(aEntry)
            sTitle = 'server '+str(i)
            #print sUrl
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            

 
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, '', oOutputParameterHandler)
 
        cConfig().finishDialog(dialog)
       
    oGui.setEndOfDirectory()
    



def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    #sHtmlContent = sHtmlContent
               
        
    sPattern = '<IFRAME.+?SRC="(.+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
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
				

        cConfig().finishDialog(dialog) 
                
    oGui.setEndOfDirectory()