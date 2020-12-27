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
 
SITE_IDENTIFIER = 'xsanime'
SITE_NAME = 'xsanime'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'https://ww.xsanime.com'
ANIM_NEWS = ('https://ww.xsanime.com/', 'showSeries')


URL_SEARCH = ('https://ww.xsanime.com/?s=', 'showSeries')
URL_SEARCH_MOVIES = ('https://ww.xsanime.com/?s=', 'showSeries')
URL_SEARCH_SERIES = ('https://ww.xsanime.com/?s=', 'showSeries')
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
        sUrl = 'https://ww.xsanime.com/?s='+sSearchText
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
 # ([^<]+) .+?
    sPattern = '<span class="label quality">([^<]+)</span>.+?<a href="([^<]+)" class="box">.+?data-src="([^<]+)" class="img-fluid w-100 lazy" alt="([^<]+)"/>.+?<span class="badge badge-pill badge-secondary ml-1">([^<]+)</span>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = str(aEntry[3]).decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            sTitle = sTitle.replace("مشاهدة","").replace("مترجم","").replace("فيلم","")
            siteUrl = str(aEntry[1])
            sThumb = str(aEntry[2])
            sDesc = ''
            sQua = aEntry[0]
            sYear = aEntry[4]
            sDisplayTitle = ('%s (%s) [%s] ') % (sTitle, sYear, sQua)


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

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
    sPattern = '<div class="MovieItem"><a title="([^<]+)" href="([^<]+)">.+?<div class="BGMovieItem" style="background-image: url([^<]+);">'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = str(aEntry[0]).decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            sTitle = sTitle.replace("مشاهدة","").replace("مترجم","").replace("فيلم","")
            siteUrl = str(aEntry[1])
            sThumb = str(aEntry[2]).replace("(","").replace(")","")
            sDesc = ''


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()


 
 
def __checkForNextPage(sHtmlContent):
    sPattern = '<li><a class="next page-numbers" href="([^<]+)">'
	
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
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    oParser = cParser()       


    # (.+?) .+? ([^<]+)
               

    sPattern = '<a href="([^<]+)" target="_blank">'
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
				sTitle = ''

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

    sPattern = 'data-server="([^<]+)" data-i='
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
				sTitle = ''

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
				

    oGui.addText(SITE_IDENTIFIER,'[COLOR olive]-------قائمه الحلقات --------[/COLOR]')
    # (.+?) .+? ([^<]+)
    sPattern = '<a href="([^<]+)">.+?<span class="number">([^<]+)</span>'

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
 
            sTitle =   ' الحلقة'+aEntry[1]
            siteUrl = aEntry[0]
            sThumbnail = ""
            sInfo = ""
 
            #print sUrl
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)        
           
                
    oGui.setEndOfDirectory()	