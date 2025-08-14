# -*- coding: utf-8 -*-

import re
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.comaddon import progress, VSlog, siteManager, addon
	
SITE_IDENTIFIER = 'fushaar'
SITE_NAME = 'Fushaar'
SITE_DESC = 'arabic vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_FAM = (f'{URL_MAIN}gerne/family/', 'showMovies')
MOVIE_EN = (URL_MAIN, 'showMovies')
KID_MOVIES = (f'{URL_MAIN}gerne/animation/', 'showMovies')
MOVIE_TOP = (f'{URL_MAIN}newest/', 'showMovies')

URL_SEARCH = (f'{URL_MAIN}?s=', 'showMovies')
URL_SEARCH_MOVIES = (f'{URL_MAIN}?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', '1/Movies.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', '1/1/Anime.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearchAll():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText != False:
        sUrl = f'{URL_MAIN}/?s={sSearchText}'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  

def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}/?s={sSearchText}'
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

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 
    sPattern = '<article class="poster">.+?href="([^<]+)">.+?title="([^<]+)" data-lazy-src="([^<]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = cUtil().CleanMovieName(aEntry[1])
            siteUrl = aEntry[0]
            sThumb = f'{aEntry[2]}|verifypeer=false'
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)            

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'rel="next" href="([^<]+)"'
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

    oParser = cParser()    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
                      
    sPattern =  '<a class="watch-hd" href="([^<]+)" target="_blank" download>(.+?)</a>'                                                             
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            
            url = aEntry[0] 
            sHost = re.sub(r"\D", "", aEntry[1])
            sTitle = f'{sMovieTitle} [COLOR coral]({sHost}p)[/COLOR]'
            sThumb = sThumb
            if url.startswith('//'):
               url = f'http:{url}'
								            
            sHosterUrl = url 
            if 'uptobox' in sHosterUrl:
                sHosterUrl = f'{sHosterUrl}|Referer={URL_MAIN}'
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
               oHoster.setDisplayName(sTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, f'{sHosterUrl}|verifypeer=false', sThumb)           
         
    sPattern =  'file: "(.+?)",.+?label: "(.+?)"'                                                            
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            
            url = aEntry[0] 
            sHost = aEntry[1]  
            sTitle = f'{sMovieTitle} [COLOR coral]({sHost})[/COLOR]' 
            sThumb = sThumb
            if url.startswith('//'):
               url = f'http:{url}'				
				            
            sHosterUrl = url 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
               oHoster.setDisplayName(sTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl , sThumb)
          
    sPattern =  '<IFRAME sandbox.+?data-lazy-src="([^"]+)'                                                                
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            if 'imgur' in aEntry:
                continue
            url = aEntry
  
            sTitle = sMovieTitle
            sThumb = sThumb
            if url.startswith('//'):
               url = f'http:{url}'
								            
            sHosterUrl = url 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
               oHoster.setDisplayName(sTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl , sThumb)
          
    sPattern =  '</span><a href=.+?data-lazy-src="([^"]+)'                                                                 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
             
        sThumb = aResult[1][0]
        oGui.addText(SITE_IDENTIFIER, '[COLOR red] الفلم للأعضاء فقط [/COLOR]', 'none.png')

    oGui.setEndOfDirectory()