# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re
import requests	

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog, siteManager, addon

SITE_IDENTIFIER = 'asia2tv'
SITE_NAME = 'Asia2TV'
SITE_DESC = 'Asian Movies and TV Shows'
 
ADDON = addon()
icons = ADDON.getSetting('defaultIcons')

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_ASIAN = (URL_MAIN + 'category/asian-movies/', 'showMovies')
SERIE_ASIAN = (URL_MAIN + 'category/asian-drama/', 'showSeries')
SERIE_KR = (URL_MAIN + 'category/asian-drama/korean/', 'showSeries')
SERIE_CN = (URL_MAIN + 'category/asian-drama/chinese-taiwanese/', 'showSeries')
SERIE_JP = (URL_MAIN + 'category/asian-drama/japanese/', 'showSeries')
SERIE_THAI = (URL_MAIN + 'category/asian-drama/thai/', 'showSeries')
REPLAYTV_PLAY = (URL_MAIN + 'category/asian-drama/kshow/', 'showSeries')


URL_SEARCH = (URL_MAIN + '?s=', 'showSeries')
FUNCTION_SEARCH = 'showSeries'

WhiteList = ('افلام','مسلسلات','برامج','اطفال','رمضان','انمي','كرتون','كارتون','دراما', 'الدراما')
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', addons.VSlang(30079), icons + '/Search.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ASIAN[1], 'أفلام آسيوية', icons + '/Asian.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_ASIAN[1], 'مسلسلات آسيوية', icons + '/Asian.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_KR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_KR[1], 'مسلسلات كورية', icons + '/Asian.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_CN[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_CN[1], 'مسلسلات صينية', icons + '/Asian.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_JP[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_JP[1], 'مسلسلات يابانية', icons + '/Asian.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_THAI[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_THAI[1], 'مسلسلات تايلاندية', icons + '/Asian.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_PLAY[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_PLAY[1], 'برامج ترفيهية', icons + '/Asian.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui() 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '?s='+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSearchSeries():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '?s='+sSearchText
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
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    

    sPattern = '<div class="box-item">.+?href="([^"]+)" title="([^"]+)'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:

            siteUrl = aEntry[0]
            sTitle = aEntry[1].replace("فيلم","").replace("مترجم ","").replace("مترجم","").replace("مدبلج ","").replace("مدبلج","").strip()
            sTitle = re.sub('[^a-zA-Z]', ' ', sTitle)
            sYear = ''
        
            sThumb = ''
        
            if sThumb.startswith('//'):
                sThumb = 'https:' + sThumb
           
            sDesc = ''

            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('siteUrl',  siteUrl) 
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear',sYear)
        
            oGui.addMovie(SITE_IDENTIFIER, 'showEpisodes' , sTitle, sYear, sThumb, sDesc, oOutputParameterHandler) 
    
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
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
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    
    sPattern = '<div class="box-item">.+?href="([^"]+)" title="([^"]+)".+?src="([^"]+)'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            siteUrl = aEntry[0]
            sTitle = aEntry[1].replace("فيلم","").replace("مترجم ","").replace("مترجم","").replace("مدبلج ","").replace("مدبلج","").strip()
            sYear = ''

            sThumb = aEntry[2]

            if sThumb.startswith('//'):
                sThumb = 'https:' + sThumb
           
            sDesc = ''

            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('siteUrl',  siteUrl) 
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear',sYear)
        
            oGui.addMovie(SITE_IDENTIFIER, 'showEpisodes' , sTitle, sYear, sThumb, sDesc, oOutputParameterHandler)


        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'Next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

 
def showEpisodes():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    oInputParameterHandler = cInputParameterHandler()
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sYear = oInputParameterHandler.getValue('sYear')
    
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()
    sStart = 'id="episode-list"'
    sEnd = '<div class="heading">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="([^"]+)".+?class="titlepisode">(.+?)</div>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:

            siteUrl = aEntry[0]
            if 'الحلقة' in aEntry[1]:
                sTitle = 'E' + aEntry[1].split("الحلقة")[1].strip()
            else:
                sTitle = aEntry[1]
            sTitle = sTitle + ' '+ sMovieTitle
            sThumb = sThumb
            sDesc = ''

            oOutputParameterHandler.addParameter('sMovieTitle', sTitle )
            oOutputParameterHandler.addParameter('siteUrl',  siteUrl) 
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear',sYear)
            oOutputParameterHandler.addParameter('sDesc',sDesc)
            oGui.addTV(SITE_IDENTIFIER, 'showHosters' , sTitle, sYear, sThumb, sDesc, oOutputParameterHandler)
  
    oGui.setEndOfDirectory()	
    
def __checkForNextPage(sHtmlContent):
    sPattern = '<a class="next page-numbers" href="([^"]+)'
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0]:
        return aResult[1][0]

    return False

def showHosters(oInputParameterHandler = False):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    ## Watch Servers
    sPattern = 'data-server="([^"]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            
            url = aEntry
            sTitle = sMovieTitle
            if url.startswith('//'):
                url = 'http:' + url
				            
            sHosterUrl = url 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                sDisplayTitle = sTitle
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    else:
        if 'قريباً' in sHtmlContent:
            oGui.addText('', 'Soon on Asia2TV - No Links Yet','None.png')
        else:
            oGui.addText('', 'Error - No Links Founds','None.png')
        
    oGui.setEndOfDirectory()
