# -*- coding: utf-8 -*-

import re
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.comaddon import progress, VSlog, siteManager
 
SITE_IDENTIFIER = 'alwanfilm'
SITE_NAME = 'Alwanfilm'
SITE_DESC = 'arabic vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_CLASSIC = (f'{URL_MAIN}movies/', 'showMovies')
REPLAYTV_PLAY = ('https://alwanzman.com/genre/%D9%83%D9%88%D9%85%D9%8A%D8%AF%D9%8A%D8%A7/', 'showMovies')
MOVIE_ANNEES = (True, 'showYears')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_CLASSIC[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كلاسيكية', '1/Classic.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_PLAY[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'مسرحيات', 'msrh.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()

def showYears():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(range(1932, 1975)):
        sYear = str(i)
        oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}release/' + sYear)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sYear, '1/Calendar.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()
	
def showMovies():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<article.+?src="([^"]+)".+?href="([^"]+)".+?class="title">(.+?)</'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            
            siteUrl = aEntry[1]
            sTitle = (cUtil().CleanMovieName(aEntry[2])).replace('</h4>',"").replace('<h4>',"").replace('"',"")
            if "movies/" not in siteUrl:
                siteUrl =  f'{URL_MAIN}movies/{siteUrl}'
            if '../../' in siteUrl:
                siteUrl =  f'https://alwanzman.com/{siteUrl}'

            sDesc = ''
            sYear = ''
            sThumb = aEntry[0]
            sDub = ''
            m = re.search('باﻷلوان', sTitle)
            if m:
                sDub = str(m.group(0))
                sTitle = sTitle.replace(sDub,'')
            m = re.search('Colorized', sTitle)
            if m:
                sDub = str(m.group(0))
                sTitle = sTitle.replace(sDub,'')
            sDisplayTitle = f'{sTitle} [{sDub}]'

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addMovie(SITE_IDENTIFIER, 'showServer', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent, sUrl)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent, sUrl):
    oParser = cParser()
    sPattern = '<link rel="next" href="([^<]+)" />'
    aResult = oParser.parse(sHtmlContent, sPattern) 
    if aResult[0]:
        return f'{sUrl}{aResult[1][0]}'

    sPattern = 'class="arrow_pag" href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern) 
    if aResult[0]:
        return f'{sUrl}{aResult[1][0]}'

    return False

def showServer():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
      	
    sPattern = '"embed_url":["\']([^"\']+)["\']'
    aResult = oParser.parse(sHtmlContent, sPattern)	
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

    sPattern = '<iframe.+?src=["\']([^"\']+)["\']'
    aResult = oParser.parse(sHtmlContent, sPattern)	
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