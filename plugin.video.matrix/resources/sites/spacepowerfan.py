# -*- coding: utf-8 -*-

import base64
import urllib.parse, re
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser
from resources.lib.util import cUtil
 
SITE_IDENTIFIER = 'spacepowerfan'
SITE_NAME = 'Spacepowerfan'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

ANIM_MOVIES = (f'{URL_MAIN}anime-type/movie/', 'showMovies')
ANIM_NEWS = (f'{URL_MAIN}anime-type/tv/', 'showSeries')
KID_CARTOON = (f'{URL_MAIN}anime-type/كرتون/', 'showSeries')


URL_SEARCH = (f'{URL_MAIN}search/?s_keyword=', 'showMovies')
URL_SEARCH_ANIMS = (f'{URL_MAIN}search/?s_keyword=', 'showSeries')
FUNCTION_SEARCH = 'showSeries'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30118), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انمي', '1/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', KID_CARTOON[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات كرتون', '1/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام انمي', '1/Anime.png', oOutputParameterHandler)  
 
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}search/?s_keyword={sSearchText}'
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

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="status_show".+?src=\'([^\']+)\'.+?href="([^"]+)".+?<span data-en-title>(.+?)</span>.+?class="show">(.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()   
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = cUtil().CleanMovieName(aEntry[2])
            sDisplayTitle = f'{sTitle} ({cUtil().CleanMovieName(aEntry[3])})'
            siteUrl = aEntry[1]
            sThumb = urllib.parse.quote(aEntry[0], safe=":/")
            sDesc = ''
            sYear = ''

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showSeasons', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
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

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="status_show".+?src=\'([^\']+)\'.+?<a href="([^"]+)" class=".*?">(.+?)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()   
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            if 'data-en' in aEntry[2]:
                sPattern2 = '<span data-en-title>(.+?)</span>.+?class="show">(.+?)</span>'
                if aResult[0]:
                    tResult = oParser.parse(aEntry[2], sPattern2)
                    for nTitle in tResult[1]:
                        sTitle = cUtil().CleanSeriesName(nTitle[0])
                        sTitle = re.sub(r"S\d{2}|S\d", "", sTitle)
                        aTitle = cUtil().CleanSeriesName(nTitle[1])
                        aTitle = re.sub(r"S\d{2}|S\d", "", aTitle)
                        sDisplayTitle = f'{sTitle} ({aTitle})'
            else:
                sTitle = sDisplayTitle = aEntry[2]
            siteUrl = aEntry[1]
            sThumb = urllib.parse.quote(aEntry[0], safe=":/")
            sDesc = ''
            sYear = ''

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
  
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()

def showSeasons():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    sPattern = 'swiper-season(.+?)</section>'
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        sHtmlContent1 = aResult[1][0] 

        sPattern = 'href="([^"]+)".+?title="([^"]+)".+?<div class=".*?">(.+?)</div>.+?style="background-image:.+?["\']([^"\']+)["\']'
        aResult = oParser.parse(sHtmlContent1, sPattern)
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler()  
            for aEntry in aResult[1]:
                
                sSeason = cUtil().ConvertSeasons(aEntry[2])
                sTitle = f'{sMovieTitle} {sSeason}'
                siteUrl = aEntry[0]
                sThumb = urllib.parse.quote(aEntry[2], safe=":/")
                sDesc = ""
    
                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                
                oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
    else:
        sPattern = '<div class="swiper-slide">.+?href="([^"]+)".+?src=\'([^\']+)\'.+?<span class=".*?">(.+?)</span>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler()  
            for aEntry in aResult[1]:
                
                sEpisode = aEntry[2].replace('-EP', 'E').strip()
                sTitle = f'{sMovieTitle} {sEpisode}'
                siteUrl = aEntry[0]
                sThumb = urllib.parse.quote(aEntry[1], safe=":/")
                sDesc = ""
    
                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                
                oGui.addEpisode(SITE_IDENTIFIER, 'showServers', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory() 

def showEpisodes():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    sPattern = '<div class="swiper-slide">.+?href="([^"]+)".+?src=\'([^\']+)\'.+?<span class=".*?">(.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            
            sEpisode = aEntry[2].replace('-EP', 'E').strip()
            sTitle = f'{sMovieTitle} {sEpisode}'
            siteUrl = aEntry[0]
            sThumb = urllib.parse.quote(aEntry[1], safe=":/")
            sDesc = ""

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            
            oGui.addEpisode(SITE_IDENTIFIER, 'showServers', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
	
def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<link rel="next" href="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False
	 
def showServers():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
   
    sPattern = 'data-embed-id="([^"]+)"\s*class'
    aResult = oParser.parse(sHtmlContent, sPattern)  
    if aResult[0]:
        for aEntry in aResult[1]:

            url = base64.b64decode(aEntry.split(':')[1]).decode('utf8',errors='ignore')

            if 'iframe' in url:
                sPattern = 'src="([^"]+)"'
                aResult = oParser.parse(url, sPattern)  
                if aResult[0]:
                    for aEntry in aResult[1]:
                        oRequestHandler = cRequestHandler(aEntry)
                        data = oRequestHandler.request()       

                        sPattern = 'source src="([^"]+)"'
                        aResult = oParser.parse(data, sPattern)
                        if aResult[0]:
                            for aEntry in aResult[1]:
                                url = aEntry
                                if url.startswith('//'):
                                    url = f'http:{url}'
                    
            sHosterUrl = url 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
				       
    oGui.setEndOfDirectory()