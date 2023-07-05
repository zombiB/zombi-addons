# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser

ADDON = addon()
icons = ADDON.getSetting('defaultIcons')

SITE_IDENTIFIER = 'xsanime'
SITE_NAME = 'Xsanime'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

ANIM_MOVIES = (URL_MAIN + '/movies_list/', 'showMovies')
ANIM_NEWS = (URL_MAIN+'/episodes' , 'showSeries')

URL_SEARCH = (URL_MAIN + '/?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '/?s=', 'showSeries')

FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Search', icons + '/Search.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات إنمي', icons + '/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام إنمي', icons + '/Anime.png', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/?s='+sSearchText
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
 # ([^<]+) .+? (.+?)
    sPattern = '<div class="itemtype_anime"><a href="([^<]+)" title="(.+?)"><div class="itemtype_anime_poster">.+?src="(.+?)" alt='

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
 
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("برنامج","").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("بلوراي","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
            sDesc = ''
            sYear = ''

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            if '/anime/'  in siteUrl:			
                oGui.addTV(SITE_IDENTIFIER, 'ShowEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler) 
            else: 		
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', icons + '/next.png', oOutputParameterHandler)
 
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
    sPattern = 'div class="itemtype_episode"><a href="([^<]+)" title="([^<]+)"><div class="itemtype_episode_poster"><img src="([^<]+)" alt='


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
 
            sTitle = aEntry[1]
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
            sDesc = ''
            sYear = ''
            sTitle = sTitle.split('الحلقة')[0].split('الموسم')[0]
            sTitle = sTitle.replace("Season ","S")

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addTV(SITE_IDENTIFIER, 'ShowEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', icons + '/next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
def __checkForNextPage(sHtmlContent):
    sPattern = 'class="next page-numbers" href="([^<]+)">'
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0]:
        return URL_MAIN + aResult[1][0]

    return False

def ShowEps():
    oGui = cGui()   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request() 
				
    # (.+?) .+? ([^<]+)

    sPattern = 'href="([^<]+)">الحلقة<em>(.+?)</em></a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
   
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
 
            sTitle = "E"+aEntry[1]
            sTitle = sMovieTitle+sTitle
            siteUrl = aEntry[0]
            sDesc = ''
            sYear = ''
 
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler) 
       
    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request() 
    
    # (.+?) .+? ([^<]+)        	
    sPattern = 'href="([^<]+)" class="download--item">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
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