# -*- coding: utf-8 -*-

import base64
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser
from resources.lib.util import cUtil
 
SITE_IDENTIFIER = 'animeblkom'
SITE_NAME = 'Animeblkom'
SITE_DESC = 'arabic vod'

sHost = base64.b64decode(siteManager().getUrlMain2(SITE_IDENTIFIER)).decode("utf-8")
sHost = sHost[::-1]

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
if addon().getSetting('Use_alternative') == "true":
    URL_MAIN = sHost
    
ANIM_NEWS = (f'{URL_MAIN}series-list', 'showSeries')
ANIM_MOVIES = (f'{URL_MAIN}movie-list', 'showMovies')

URL_SEARCH_ANIMS = (f'{URL_MAIN}search?query=', 'showSeries')
FUNCTION_SEARCH = 'showSeries'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30118), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات انمي', '1/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام انمي', '1/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}/special-list')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'قائمة الحلقات خاصة', '1/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}/ova-list')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'قائمة الأوفا', '1/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}/ona-list')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'قائمة الأونا', '1/Anime.png', oOutputParameterHandler)
            
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}search?query={sSearchText}'
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

    if addon().getSetting('Use_alternative') == "true":
        sUrl = sHost + "/".join(sUrl.split("/")[3:]) if sUrl.startswith("https://") else sUrl

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<img class="lazy" data-original="([^"]+)".+?<a href="([^"]+)">(.+?)<.+?story-text">.+?p>(.*?)</'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = (cUtil().CleanMovieName(aEntry[2])).replace("poster","")
            siteUrl = aEntry[1]
            sThumb = URL_MAIN.rstrip('/') + aEntry[0]
            sDesc = f'[COLOR yellow]{aEntry[3]}[/COLOR]'
            sYear = ''
			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)
            if '/watch/' in siteUrl:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler) 
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

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

    if addon().getSetting('Use_alternative') == "true":
        sUrl = sHost + "/".join(sUrl.split("/")[3:]) if sUrl.startswith("https://") else sUrl

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<img class="lazy" data-original="([^"]+)".+?<a href="([^"]+)">(.+?)<.+?story-text">.+?p>(.*?)</'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = cUtil().CleanSeriesName(aEntry[2])
            siteUrl = aEntry[1]
            sThumb = URL_MAIN.rstrip('/') + aEntry[0]
            sDesc = aEntry[3]
            sYear = ''

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle',sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)
            if '/watch/' in siteUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler) 
            else:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
def showEpisodes():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    if addon().getSetting('Use_alternative') == "true":
        sUrl = sHost + "/".join(sUrl.split("/")[3:]) if sUrl.startswith("https://") else sUrl

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.replace('<span class="badge pull-left">الأخيرة</span> ', '')
	
    sDesc = ''
    if '<a>لم يتم رفع أي حلقات حتى الآن</a>' in sHtmlContent:
        oOutputParameterHandler = cOutputParameterHandler() 
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]لم يتم رفع أي حلقات حتى الآن[/COLOR]')

    sPattern = '<li class="episode-link.+?<a href="([^"]+)">.+?<span class="separator">.+?<span>([^<]+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
 
            sTitle = f'{sMovieTitle.replace("Season ", "S")} E{aEntry[1]}'
            siteUrl = aEntry[0]
            sThumb = sThumb
            sDesc = sDesc
 
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
 
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
   
    oGui.setEndOfDirectory() 

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<a class="page-link" href="([^<]+)" rel="next" '	
    aResult = oParser.parse(sHtmlContent, sPattern) 
    if aResult[0]:        
        return aResult[1][0]
    
    return False

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    if addon().getSetting('Use_alternative') == "true":
        sUrl = sHost + "/".join(sUrl.split("/")[3:]) if sUrl.startswith("https://") else sUrl

    oParser = cParser()    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="item"> <span class="([^<]+)">'
    sPattern = f'{sPattern}|<a data-src="([^<]+)">([^<]+)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            if 'brmj' in aEntry[1]:
                continue
            sSub = f'{aEntry[0].replace("active","")} ترجمة'

            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, f'[COLOR coral]{sSub}[/COLOR]') 

            if aEntry[1]:
                url = aEntry[1]
                if url.startswith('//'):
                    url = f'https:{url}'
            
                sHosterUrl = url 
                if 'userload' in sHosterUrl:
                    sHosterUrl = f'{sHosterUrl}|Referer={URL_MAIN}' 
                if 'mystream' in sHosterUrl:
                    sHosterUrl = f'{sHosterUrl}|Referer={URL_MAIN}'  
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    sPattern = '<div class="col-xs-12 col-md-2 quality-icon ([^<]+)"'
    sPattern = f'{sPattern}|<a href="([^<]+)" target="_blank"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            if 'brmj' in aEntry[1]:
                continue
            sSub = aEntry[0]    

            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, f'[COLOR coral]{sSub}[/COLOR]')  

            if aEntry[1]:
                url = aEntry[1]
                if url.startswith('//'):
                    url = f'https:{url}'

                sHosterUrl = url 
                if 'userload' in sHosterUrl:
                    sHosterUrl = f'{sHosterUrl}|Referer={URL_MAIN}'
 
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
				
    oGui.setEndOfDirectory()
