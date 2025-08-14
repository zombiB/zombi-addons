# -*- coding: utf-8 -*-

import re
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.multihost import cMegamax
from resources.lib import random_ua

UA = random_ua.get_ua()

SITE_IDENTIFIER = 'hwnaturkya'
SITE_NAME = 'HwnaTurkya'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

SERIE_TR = (f'{URL_MAIN}category/مسلسلات-تركية-مترجمة', 'showSeries')
SERIE_TR_AR = (f'{URL_MAIN}category/مسلسلات-تركية-مدبلجة', 'showSeries')
MOVIE_TURK = (f'{URL_MAIN}category/افلام-تركية-مترجمة', 'showMovies')
MOVIE_DUBBED = (f'{URL_MAIN}category/افلام-تركية-مدبلجة', 'showMovies')

URL_SEARCH = (f'{URL_MAIN}search/', 'showSeries')
URL_SEARCH_MOVIES = (f'{URL_MAIN}search/', 'showMovies')
URL_SEARCH_SERIES = (f'{URL_MAIN}search/', 'showSeries')
FUNCTION_SEARCH = 'showSeries'
 
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', addons.VSlang(30079), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية', '1/Turkish.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_DUBBED[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية مدبلجة', '1/Turkish.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', '1/Turkish.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية مدبلجة', '1/Turkish.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}search/{sSearchText}'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}search/{sSearchText}'
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
    sHtmlContent = oRequestHandler.request().replace('&rsaquo;', '>').replace('&raquo;', '>>').replace('&lsaquo;', '<')

    sPattern = '<article class="post">.+?<a href="([^"]+)" title="([^"]+)".+?data-original="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if "فيلم" not in aEntry[1]:
                continue
 
            sTitle = cUtil().CleanMovieName(aEntry[1])
            siteUrl = aEntry[0] .replace("/movies/","/watch_movies/")
            sThumb = aEntry[2]
            sYear = ''
            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch: 
        sPattern = '<li><a href="([^"]+)" data-ci-pagination-page="([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            total = len(aResult[1])
            progress_ = progress().VScreate(SITE_NAME)
            oOutputParameterHandler = cOutputParameterHandler() 
            for aEntry in aResult[1]:
                progress_.VSupdate(progress_, total)
                if progress_.iscanceled():
                    break
 
                sTitle =  f'[COLOR red]Page: {aEntry[1]}[/COLOR]'
                siteUrl = aEntry[0]
                sThumb = ""
                sDesc = ""

                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
			
                oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'next.png', oOutputParameterHandler)

            progress_.VSclose(progress_)
 
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
    sHtmlContent = oRequestHandler.request().replace('&rsaquo;', '>').replace('&raquo;', '>>').replace('&lsaquo;', '<')

    itemList = []	
    sPattern = '<article class="post">.+?<a href="([^"]+)" title="([^"]+)".+?data-original="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if "فيلم" in aEntry[1]:
                continue
 
            sTitle = (cUtil().CleanSeriesName(aEntry[1])).replace('- قصة عشق','')
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
            sDesc = ''
            sYear = ''
            sDesc = ""
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))

            if sTitle not in itemList:
                itemList.append(sTitle)	
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sYear', sYear)
			
                oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch: 
        sPattern = '<li><a href="([^"]+)" data-ci-pagination-page="([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)	
        if aResult[0]:
            total = len(aResult[1])
            progress_ = progress().VScreate(SITE_NAME)
            oOutputParameterHandler = cOutputParameterHandler() 
            for aEntry in aResult[1]:
                progress_.VSupdate(progress_, total)
                if progress_.iscanceled():
                    break
 
                sTitle =  f'[COLOR red]Page: {aEntry[1]}[/COLOR]'
                siteUrl = aEntry[0]
                sThumb = ""
                sDesc = ""

                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
			
                oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'next.png', oOutputParameterHandler)

            progress_.VSclose(progress_)

        oGui.setEndOfDirectory()
 
def showSeasons():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oParser = cParser()    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request() 

    sPattern = '<div id="getSeasonsBySeries" class="(.+?)">'
    aResult = oParser.parse(sHtmlContent, sPattern)		
    if aResult[0]:

        sStart = '<a title="سلسلة مواسم">'
        sEnd = '<div class="container">'
        sHtmlContents = oParser.abParse(sHtmlContent, sStart, sEnd)

        sPattern = '<div class="seasonNum">(.+?)</div>.+?href="(.+?)" title="(.+?)">.+?src="([^"]+)'
        aResult = oParser.parse(sHtmlContents, sPattern)
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler()    
            for aEntry in aResult[1]:

                sTitle = (cUtil().CleanMovieName(aEntry[2]))
                sTitle = cUtil().ConvertSeasons(sTitle)
                if 'موسم' not in aEntry[2]:
                    sTitle = f'{sTitle} S01'
                siteUrl = aEntry[1]
                sThumb = aEntry[3]
                sDesc = ''
                if sThumb.startswith('//'):
                    sThumb = f'https:{aEntry[1]}'
			
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addSeason(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
                
    else:
        sPattern = '<a class href="([^"]+)" title="([^"]+)".+?class="numEp">([^<]+)</span>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler() 
            for aEntry in aResult[1]:
 
                sTitle = f'{sMovieTitle} E{aEntry[2]}'
                sThumb = sThumb
                siteUrl = aEntry[0].replace("/episodes/","/watch_episodes/")
                sDesc = ""

                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showEps():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oParser = cParser()    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request() 

    sStart = 'class="list-episodes"'
    sEnd = 'class="container"'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'href="([^"]+)" title="([^"]+)".+?class="numEp">([^<]+)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
 
            sTitle = f'{sMovieTitle.replace("مدبلج","").replace("مترجم","")} E{aEntry[2]}'
            sThumb = sThumb
            siteUrl = aEntry[0].replace("/episodes/","/watch_episodes/")
            sDesc = ""

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
    oGui.setEndOfDirectory() 

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern =  "baseUrl = '([^']+)" 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        URL_MAIN = aResult[1][0] 

    sPattern =  'postID = "([^"]+)' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        postID = aResult[1][0] 

    sPattern =  'onclick="([^"]+)' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
                    sServer = aEntry.replace("getPlayer('","").replace("')","")

                    oRequestHandler = cRequestHandler(f'{URL_MAIN}ajax/getPlayer')
                    oRequestHandler.addHeaderEntry('Accept', '*/*')
                    oRequestHandler.addHeaderEntry('User-Agent', UA)
                    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
                    oRequestHandler.addHeaderEntry('Origin', URL_MAIN)
                    oRequestHandler.addHeaderEntry('sec-fetch-dest', 'empty')
                    oRequestHandler.addHeaderEntry('sec-fetch-mode', 'cors')
                    oRequestHandler.addHeaderEntry('sec-fetch-site', 'same-origin')
                    oRequestHandler.addParameters('server', sServer)
                    oRequestHandler.addParameters('postID', postID)
                    oRequestHandler.addParameters('Ajax', '1')
                    oRequestHandler.setRequestType(1)
                    sHtmlContent1 = oRequestHandler.request()

                    sPattern = '<IFRAME.+?SRC=["\']([^"\']+)["\']'
                    aResult = oParser.parse(sHtmlContent1, sPattern)
                    if aResult[0]:
                        oOutputParameterHandler = cOutputParameterHandler()
                        for aEntry in (aResult[1]):
                            if 'قريبا' in aEntry:
                                continue
                            if 'leech' in aEntry:
                                continue

                            sHosterUrl = aEntry
                            if sHosterUrl.startswith('//'):
                                sHosterUrl = f'http:{sHosterUrl}'

                            if bool(re.search(r'mega.*max', sHosterUrl)):
                                data = cMegamax().GetUrls(sHosterUrl)
                                if data is not False:
                                    for item in data:
                                        sHosterUrl = item.split(',')[0].split('=')[1]
                                        sQual = item.split(',')[1].split('=')[1]
                                        sLabel = item.split(',')[2].split('=')[1]

                                        sDisplayTitle = f'{sMovieTitle} [COLOR coral] [{sQual}][/COLOR][COLOR orange] - {sLabel}[/COLOR]'  
                                        oOutputParameterHandler.addParameter('sHosterUrl', sHosterUrl)
                                        oOutputParameterHandler.addParameter('siteUrl', sUrl)
                                        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                                        oOutputParameterHandler.addParameter('sThumb', sThumb)

                                        oGui.addLink(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, sThumb, sDisplayTitle, oOutputParameterHandler)

                            oHoster = cHosterGui().checkHoster(sHosterUrl)
                            if oHoster:
                                oHoster.setDisplayName(sMovieTitle)
                                oHoster.setFileName(sMovieTitle)
                                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    sPattern = '<a target="_blank" href=["\']([^"\']+)["\'].+?<i class="icon-download">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:

            if 'megamax' in aEntry:
                continue
            
            url = aEntry
            sTitle = sMovieTitle
            if url.startswith('//'):
               url = f'http:{url}'
            
            sHosterUrl = url 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
               oHoster.setDisplayName(sTitle)
               oHoster.setFileName(sTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def showLinks():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sHosterUrl = oInputParameterHandler.getValue('sHosterUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
 
    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if oHoster:
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()