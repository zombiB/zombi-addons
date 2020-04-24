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
 
SITE_IDENTIFIER = 'zimabdko'
SITE_NAME = 'zimabdko'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'https://www.zimabdko.com'

ANIM_NEWS = ('https://www.zimabdko.com/series/', 'showSeries')

ANIM_MOVIES = ('https://www.zimabdko.com/anime/', 'showMovies')

URL_SEARCH = ('https://www.zimabdko.com/?s=', 'showSeries')
URL_SEARCH_MOVIES = ('https://www.zimabdko.com/?s=', 'showMovies')
URL_SEARCH_SERIES = ('https://www.zimabdko.com/?s=', 'showSeries')
FUNCTION_SEARCH = 'showSeries'
 
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
        sUrl = 'https://www.zimabdko.com/?s='+sSearchText
        showSeries(sUrl)
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
 # ([^<]+) .+?

    sPattern = '<a href="([^<]+)">.+?<img width=".+?" height=".+?" src="([^<]+)" class=".+?<h2>([^<]+)</h2>'

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
            sTitle = sTitle.replace("مشاهدة","").replace("مترجم","").replace("فيلم","")
            siteUrl = str(aEntry[0])
            sThumb = str(aEntry[1])
            sDesc = ""


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showServers', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

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
 # ([^<]+) .+?

    sPattern = '<a href="([^<]+)"><img width=".+?" height=".+?" src="(.+?)".+?<h2>([^<]+)</h2>.+?<span class="year">([^<]+)</span>'

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
            siteUrl = aEntry[0]
            sThumb = str(aEntry[1])
            sDesc = aEntry[3]


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()


def showEpisodes():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()
    
    #Recuperation infos
    sNote = ''

    sPattern = '<b>قصة الأنيمي : </b>.+?<p>([^<]+)</p>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        sNote = aResult[1][0]
     # (.+?) ([^<]+) .+?
    sPattern = '<div class="one-poster seasonsEx col-sm-2">.+?<div class="wrap-poster clearfix">.+?<a href="([^<]+)"><img width=".+?" height=".+?" src="([^<]+)" class.+?<h2>([^<]+)</h2>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[2]
            siteUrl = str(aEntry[0])
            sThumb = aEntry[1]
            sDesc = sNote
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
     # (.+?) ([^<]+) .+?
    sPattern = ' <div class="one-poster col-sm-2">.+?<div class="wrap-poster clearfix">.+?<a href="([^<]+)"><img width=".+?" height=".+?" src="([^<]+)".+?<h2>([^<]+)</h2>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[2]
            siteUrl = str(aEntry[0])
            sThumb = aEntry[1]
            sDesc = sNote
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showServers', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
	

  
def showServers():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    oParser = cParser()  
	    #Affichage du menu  
    oGui.addText(SITE_IDENTIFIER,'[COLOR olive]-------سيرفرات المشاهدة--------[/COLOR]')
   
    #Recuperation infos
    sId = ''
    serv = ''
    sUrl2 = ''

    sPattern = '<a class="buttosn"  data-serv="(.+?)" data-post="(.+?)"><i'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        for aEntry in aResult[1]:
			total = len(aResult[1])
			progress_ = progress().VScreate(SITE_NAME)
			serv = aEntry[0]
			sId = aEntry[1]
			sUrl2 = 'https://www.zimabdko.com/wp-admin/admin-ajax.php?action=codecanal_ajax_request&post='+sId+'&serv='+serv


			oRequestHandler = cRequestHandler(sUrl2)
			sHtmlContent2 = oRequestHandler.request()

    # (.+?) .+? ([^<]+)        	
			sPattern = 'src="([^<]+)" allowfullscreen>'
			oParser = cParser()
			aResult = oParser.parse(sHtmlContent2, sPattern)

	
			if (aResult[0] == True):
				total = len(aResult[1])
				progress_ = progress().VScreate(SITE_NAME)
				for aEntry in aResult[1]:
					progress_.VSupdate(progress_, total)
					if progress_.iscanceled():
						break
            
					url = str(aEntry)
					sTitle = sMovieTitle
					if url.startswith('//'):
						url = 'http:' + url
					
					
            
					sHosterUrl = url 
					oHoster = cHosterGui().checkHoster(sHosterUrl)
					if (oHoster != False):
						sDisplayTitle = sTitle
						oHoster.setDisplayName(sDisplayTitle)
						oHoster.setFileName(sMovieTitle)
						cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
				

				progress_.VSclose(progress_)
					
					
    oGui.addText(SITE_IDENTIFIER,'[COLOR olive]-------سيرفرات التحميل--------[/COLOR]')





    # (.+?) .+? ([^<]+)
               

    sPattern = '<a href="([^<]+)"><i'
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
        
				url = aEntry
				sTitle = ""

				if 'thevideo.me' in url:
					sTitle = " (thevideo.me)"
				if 'flashx' in url:
					sTitle = " (flashx)"
				if 'streamcherry' in url:
					sTitle = " (streamcherry)"
				if url.startswith('//'):
					url = 'https:' + url
				
					
            
				sHosterUrl = url 
				oHoster = cHosterGui().checkHoster(sHosterUrl)
				if (oHoster != False):
					sDisplayTitle = sMovieTitle+sTitle
					oHoster.setDisplayName(sDisplayTitle)
					oHoster.setFileName(sMovieTitle)
					cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
				

			progress_.VSclose(progress_)
 
      

               
       
    oGui.setEndOfDirectory()	
 
 
def __checkForNextPage(sHtmlContent):
    sPattern = "<a href='([^<]+)' class='inactive' >"
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if (aResult[0] == True):
        #print aResult[1][0]
        return aResult[1][0]

    return False