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

SITE_IDENTIFIER = 'watanflix'
SITE_NAME = 'Watanflix'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'http://watanflix.com/'

RAMADAN_SERIES = (URL_MAIN + '/ar/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA', 'showSeries')
SERIE_AR = (URL_MAIN + '/ar/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA', 'showSeries')
KID_CARTOON = (URL_MAIN + '/ar/category/%D8%A3%D8%B7%D9%81%D8%A7%D9%84', 'showSerie')

SERIE_GENRES = (True, 'showGenres')

URL_SEARCH = (URL_MAIN + '/ar/search?q=', 'showSeries')
URL_SEARCH_SERIES = (URL_MAIN + '/ar/search?q=', 'showSeriesSearch')
FUNCTION_SEARCH = 'showSeries'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Search', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات عربية', 'mslsl.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', KID_CARTOON[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات كرتون', 'crtoon.png', oOutputParameterHandler) 
    
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText is not False:
        sUrl = URL_MAIN + '/ar/search?q='+sSearchText
        showSeriesSearch(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSeriesSearch(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    if "title" in sHtmlContent:
        sHtmlContent = sHtmlContent.encode("utf8",errors='ignore').decode("unicode_escape")
 # .+? ([^<]+)

    sPattern = ',"title":"(.+?)",.+?,"url":"(.+?)","class'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[0]
            siteUrl = aEntry[1]
            sThumb = ""
            sYear = ""
            sDesc = ""


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
            oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
   

def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ["كوميدي","https://watanflix.com/ar/type/%D9%83%D9%88%D9%85%D9%8A%D8%AF%D9%8A"] )
    liste.append( ["دراما","https://watanflix.com/ar/type/%D8%AF%D8%B1%D8%A7%D9%85%D8%A7"] )
    liste.append( ["حارة-شامية","https://watanflix.com/ar/type/%D8%AD%D8%A7%D8%B1%D8%A9-%D8%B4%D8%A7%D9%85%D9%8A%D8%A9"] )
    liste.append( ["تاريخي-سيرة-ذاتيه-وثائقي","https://watanflix.com/ar/type/%D8%AA%D8%A7%D8%B1%D9%8A%D8%AE%D9%8A-%D8%B3%D9%8A%D8%B1%D8%A9-%D8%B0%D8%A7%D8%AA%D9%8A%D9%87-%D9%88%D8%AB%D8%A7%D8%A6%D9%82%D9%8A"] )
    liste.append( ["غموض-تشويق","https://watanflix.com/ar/type/%D8%BA%D9%85%D9%88%D8%B6-%D8%AA%D8%B4%D9%88%D9%8A%D9%82"] )
    
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'genres.png', oOutputParameterHandler)
       
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
 # .+? ([^<]+)

    sPattern = 'title="<h4>.+?</h4><br> <span>([^<]+)</span>".+?data-content=" <div>(.+?)<br/>.+?<a href="([^<]+)" class="v-link" >.+?<div  class="video_img"><img alt="([^<]+)"  class="" src="([^<]+)"></div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[3]
            siteUrl = aEntry[2]
            sThumb = aEntry[4]
            sDesc = aEntry[1]
            sYear = aEntry[0]
            sDisplayTitle = ('%s (%s)') % (sTitle, sYear)

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage != False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
def showSerie(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 #.+?([^<]+)

    sPattern = 'data-content=" <div>(.+?)<br/>.+?<a href="([^<]+)" class="v-link" >.+?<div  class="video_img"><img alt="([^<]+)"  class="" src="([^<]+)"></div'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
				
            sTitle = aEntry[2]      
            siteUrl = aEntry[1]
            sThumb = aEntry[3]
            sDesc = aEntry[0]
            sYear = ""

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
            oGui.addDir(SITE_IDENTIFIER, 'showSerie', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
  
 
def __checkForNextPage(sHtmlContent):
    sPattern = 'href="([^<]+)" rel="next">'
	 # .+? ([^<]+)
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0] is True:
        
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
                     
    sPattern = '<div style="overflow: hidden">.+?<a href="([^<]+)" target="_blank" class="linkPlay">.+?<img src="([^<]+)"  style=" margin: -13% 0 -10% 0; width: 100%;">.+?<i class="play-icon"></i>.+?</a>.+?</div>.+?<div><p><b>.+?</b><br/>([^<]+)</p></div>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if aResult[0] is True:
        for aEntry in aResult[1]:
            
            sTitle = sMovieTitle+aEntry[2].replace("الحلقة "," E")                
            sThumb = aEntry[1]
            url = str(aEntry[0])
            if url.startswith('//'):
                url = 'http:' + url
            
            sHosterUrl = url
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
				

    oGui.setEndOfDirectory()                