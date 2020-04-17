#-*- coding: utf-8 -*-
#zombi
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress
from resources.lib.parser import cParser
from resources.lib.util import cUtil
import urllib2,urllib,re
import unicodedata
 
SITE_IDENTIFIER = 'animeblkom'
SITE_NAME = 'animeblkom'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'https://animeblkom.net'
ANIM_NEWS = ('https://animeblkom.net/', 'showSeries')

ANIM_MOVIES = ('https://animeblkom.net/movie-list', 'showSerieSearch')
URL_SEARCH_SERIES = ('https://animeblkom.net/search?query=', 'showSerieSearch')
FUNCTION_SEARCH = 'showSerieSearch'
 
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
        sUrl = 'https://animeblkom.net/search?query='+sSearchText
        showSerieSearch(sUrl)
        oGui.setEndOfDirectory()
        return

 
def showSerieSearch(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    #print sHtmlContent
     # (.+?) ([^<]+) .+?
    sPattern = '<div class="poster"> <a href="([^<]+)"> <img class="lazy" data-original="([^<]+)" alt=".+?"> </a> </div> <div class="info"> <div class="name"> <a href=".+?">([^<]+)</a> </div> <div class="overlay">.+?</div> <div class="story"> <div class="story-text"> <p>([^<]+)</p>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = str(aEntry[2]).decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            siteUrl = URL_MAIN+str(aEntry[0])
            sThumbnail = URL_MAIN+str(aEntry[1])
            sInfo = aEntry[3].decode("utf8")
            sInfo = cUtil().unescape(sInfo).encode("utf8")



            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', aEntry[3])
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
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
     # (.+?) ([^<]+) .+?

    sPattern = '<div class="content-inner"> <div class="poster"> <a href="([^<]+)"> <img class="lazy" data-original="(.+?)" alt="(.+?)"> </a> </div> <div class="info">.+?<div class="story"> <div class="story-text"> <p>(.+?)</p>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = str(aEntry[2]).decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            sTitle = sTitle.replace("poster","")
            siteUrl = URL_MAIN+str(aEntry[0])
            sThumbnail = URL_MAIN+str(aEntry[1])
            sInfo = aEntry[3].decode("utf8")
            sInfo = cUtil().unescape(sInfo).encode("utf8")
            sInfo = '[COLOR yellow]'+aEntry[3]+'[/COLOR]'


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
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
    sHtmlContent = oRequestHandler.request()
     # (.+?) ([^<]+) .+?
    sPattern = '<div class="recent-episode episode animated-episode fadeInUp"> <a href="([^<]+)"> <div class="poster"> <img class="lazy" data-original="([^<]+)" alt=".+?"> <div class="overlay"><i class="fa fa-play"></i></div> </div> <div class="text"> <div class="name">([^<]+)</div> <hr> <div class="episode-number">([^<]+)</div>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = str(aEntry[2]).decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            siteUrl = URL_MAIN+str(aEntry[0])
            sThumbnail = URL_MAIN+str(aEntry[1])
            sInfo = '[COLOR yellow]'+aEntry[3]+'[/COLOR]'


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', aEntry[3])
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
def showEps():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    # (.+?) .+?
    sPattern = '<td>(.+?)</td><td><a href="(.+?)"><i class="fa fa-play"></i> ?????? ????</a>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent.replace('\n',''))
    #fh.close()

    #print aResult
   
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = " "+aEntry[0]
            siteUrl = str(aEntry[1])
            sThumbnail = str(sThumbnail)
            sInfo = ""
 
            #print sUrl
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            

 
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
 
        progress_.VSclose(progress_)
       
    oGui.setEndOfDirectory() 

 
def __checkForNextPage(sHtmlContent):
    sPattern = '<a class="page-link" href="([^<]+)" rel="next" '
	
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
    sHtmlContent = oRequestHandler.request()

    # (.+?) .+? ([^<]+)
               

    sPattern = '<a>([^<]+)</a>'
    sPattern = sPattern + '|' + '<div class="item"> <span class="([^<]+)"> <a data-src="([^<]+)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)


    #print aResult

	
    if (aResult[0] == True):
			total = len(aResult[1])
			progress_ = progress().VScreate(SITE_NAME)
			for aEntry in aResult[1]:
				progress_.VSupdate(progress_, total)
				if progress_.iscanceled():
					break


 


				sSub = aEntry[0]
            
				if aEntry[0]:
					oGui.addText(SITE_IDENTIFIER,'[COLOR coral]'+sSub+'[/COLOR]')
                   
        
				if aEntry[1]:
					url = str(aEntry[2])
					sTitle = str(aEntry[1]).decode("utf8").replace('"',"")
					sTitle = cUtil().unescape(sTitle).encode("utf8")
					sTitle = '[COLOR yellow]'+sTitle+'[/COLOR]'
					if url.startswith('//'):
						url = 'https:' + url
            
					sHosterUrl = url 
					oHoster = cHosterGui().checkHoster(sHosterUrl)
					if (oHoster != False):
						sDisplayTitle = sMovieTitle+sTitle
						oHoster.setDisplayName(sDisplayTitle)
						oHoster.setFileName(sMovieTitle)
						cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				

			progress_.VSclose(progress_)
	    #Affichage du menu  
    oGui.addText(SITE_IDENTIFIER,'[COLOR olive]---------------[/COLOR]')
    # (.+?) .+?
    sPattern = '<li class="episode-link"> <a href="(.+?)"> <span>الحلقة</span> <span class="separator">:</span> <span>(.+?)</span> </a> </li>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent.replace('\n',''))
    #fh.close()

    #print aResult
   
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = " الحلقة"+aEntry[1]
            siteUrl = URL_MAIN+str(aEntry[0])
            sThumbnail = str(sThumbnail)
            sInfo = ""
 
            #print sUrl
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            

 
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
 
        progress_.VSclose(progress_)
                
    oGui.setEndOfDirectory()