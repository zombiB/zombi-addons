# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, siteManager, VSlog, addon
ADDON = addon()
icons = ADDON.getSetting('defaultIcons')

SITE_IDENTIFIER = 'btolat'
SITE_NAME = 'Btolat'
SITE_DESC = 'sport vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
SPORT_FOOT = (URL_MAIN + 'video', 'showMovies')
MOVIE_PACK = (URL_MAIN , 'showPack')
SPORT_SPORTS = ('http://', 'load')

def load():
    oGui = cGui() 

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_FOOT[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أهداف و ملخصات ',  icons + '/Sport.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_PACK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showPack', 'فيديوهات الموقع',  icons + '/Sport.png', oOutputParameterHandler)

    oGui.setEndOfDirectory() 


def showPack():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
     # (.+?) ([^<]+) .+?
    sStart = '/video">فيديوهات</a>'
    sEnd = 'matches">مباريات</a></li>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    sPattern = 'href="([^<]+)">([^<]+)</a>'


    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if '#' in aEntry[0]:
                continue 
            sTitle = aEntry[1]
            siteUrl = aEntry[0].split('"')[0]
            if siteUrl.startswith('/'):
                siteUrl = URL_MAIN + aEntry[0].split('"')[0]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
			
            oGui.addMisc(SITE_IDENTIFIER, 'showPackMovies', sTitle, 'sport.png', '', '', oOutputParameterHandler)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showPack', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()

def showPackMovies(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
	 # .+? ([^<]+) 

    sPattern = '<div class="categoryNewsCard">.+?<a href=([^<]+)>.+?data-original="([^<]+)" alt="([^<]+)" />'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            sUrl = aEntry[0].replace("'","")
            sUrl = URL_MAIN+sUrl
            sTitle = aEntry[2]
            sDesc = ""
            sThumb = aEntry[1]
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, 'doc.png', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
	 # .+? ([^<]+) 

    sPattern = '<div class="categoryNewsCard">.+?<a href=([^<]+)>.+?data-original="([^<]+)" alt="([^<]+)" />'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            sUrl = aEntry[0].replace("'","")
            sUrl = URL_MAIN+sUrl
            sTitle = aEntry[2]
            sDesc = ""
            sThumb = aEntry[1]
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, 'doc.png', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)


    sPattern = '<h1 class="title">([^<]+)</h1>.+?<a href="([^<]+)">.+?data-original="([^<]+)" alt='

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            sUrl = aEntry[1]
            sUrl = URL_MAIN+sUrl
            sTitle = aEntry[0]
            sDesc = ""
            sThumb = aEntry[2]
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, 'doc.png', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    sPattern = '<h1 class="title">([^<]+)</h1>.+?<a href="([^<]+)">.+?<img src="([^<]+)" alt='

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            sUrl = aEntry[1]
            sUrl = URL_MAIN+sUrl
            sTitle = aEntry[0]
            sDesc = ""
            sThumb = aEntry[2]
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, 'doc.png', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = 'data-val="(.+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if aResult[0]:
        nPage = URL_MAIN+'video/LoadMore?VideoID='+aResult[1][0]+'&cat='
        return nPage


    sPattern = '<li class="active"><a>.+?<a href="(.+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if aResult[0]:
        nPage = aResult[1][0]
        return nPage

    return False

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    sPattern =  "'true' src='(.+?)'"
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        m3url = aResult[1][0] 
        oRequest = cRequestHandler(m3url)
        sHtmlContent2 = oRequest.request()
    
 
    sPattern = ",src:{hls:'(.+?)'}" 
    aResult = oParser.parse(sHtmlContent2, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:

            url = aEntry
            if url.startswith('//'):
                url = 'http:' + url
            sHosterUrl = url
			
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

                
    oGui.setEndOfDirectory()    