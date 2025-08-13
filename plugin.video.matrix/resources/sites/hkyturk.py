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

SITE_IDENTIFIER = 'hkyturk'
SITE_NAME = 'HkyahTurkiya'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

SERIE_TR = (f'{URL_MAIN}category/مسلسلات-تركية-مترجمة/', 'showSeries')
SERIE_TR_AR = (f'{URL_MAIN}category/مسلسلات/مسلسلات-تركية-مدبلجة/', 'showSeries')
MOVIE_TURK = (f'{URL_MAIN}category/افلام-تركية/', 'showMovies')

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

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', '1/Turkish.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية مدبلجة', '1/Turkish.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}episodes/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries2', 'احدث الحلقات', '1/Turkish.png', oOutputParameterHandler)

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

    sPattern = 'class="block-post">.+?href="([^"]+)" title="([^"]+)".+?style="background-image:url([^<]+);"></div>'
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
            siteUrl = f'{aEntry[0]}?do=watch'
            sThumb = re.sub(r'-\d*x\d*.','.', aEntry[2].replace("(","").replace(")",""))
            sYear = ''
            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch: 
        sPattern = r"href=[\'\"]([^\'\"]+)[\'\"]\s*class=[\'\"].+?[\'\"]\s*>(\d+)</a>"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:

                sTitle = f'[COLOR red]Page: {aEntry[1]}[/COLOR]'
                siteUrl = aEntry[0]

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
			
                oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'next.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

def showSeries2():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request().replace('&rsaquo;', '>').replace('&raquo;', '>>').replace('&lsaquo;', '<')

    sPattern = 'class="block-post">.+?href="([^"]+)" title="([^"]+)".+?(data-img|style)="([^"]+)'
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
 
            sTitle = (cUtil().CleanMovieName(aEntry[1])).replace('الحلقة ','E').replace('حلقة ','E')
            sTitle = cUtil().ConvertSeasons(sTitle)
            siteUrl = f'{aEntry[0]}?do=watch'
            sThumb = aEntry[3]
            if 'background-image' in sThumb:
                match = re.search(r"(?<=url\()([^)]+)(?=\))", sThumb)
                if match:
                    sThumb = match.group(1)
            sDesc = ""

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
    sPattern = r"href=[\'\"]([^\'\"]+)[\'\"]\s*class=[\'\"].+?[\'\"]\s*>(\d+)</a>"
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:

            sTitle = f'[COLOR red]Page: {aEntry[1]}[/COLOR]'
            siteUrl = aEntry[0]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        
            oGui.addDir(SITE_IDENTIFIER, 'showSeries2', sTitle, 'next.png', oOutputParameterHandler)

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
    sPattern = 'class="block-post">.+?href="([^"]+)" title="([^"]+)".+?(data-img|style)="([^"]+)'
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
            sTitle = re.sub(r"S\d{2}|S\d", "", sTitle)
            siteUrl = aEntry[0]
            sThumb = aEntry[3]
            if 'background-image' in sThumb:
                match = re.search(r"(?<=url\()([^)]+)(?=\))", sThumb)
                if match:
                    sThumb = match.group(1)
            sDesc = ""

            if sTitle not in itemList:
                itemList.append(sTitle)	
                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
			
                oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch: 
        sPattern = r"href=[\'\"]([^\'\"]+)[\'\"]\s*class=[\'\"].+?[\'\"]\s*>(\d+)</a>"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:

                sTitle = f'[COLOR red]Page: {aEntry[1]}[/COLOR]'
                siteUrl = aEntry[0]

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
			
                oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'next.png', oOutputParameterHandler)

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
    
    sPattern = 'data-season="(.+?)">(.+?)</li>'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            sSeason = (cUtil().ConvertSeasons(aEntry[1]).split("الحلقة")[0])
            if bool(re.search(r'\d', sSeason)) is False:
                sSeason = "S1"
            siteUrl = f'{URL_MAIN}wp-content/themes/vo2023/temp/ajax/seasons.php?seriesID={aEntry[0]}'
            sMovieTitle = re.sub(r"\s+([0-9]+)\s+", "", sMovieTitle)
            sTitle = f'{sMovieTitle} {sSeason}' 
            sThumb = sThumb
            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('siteUrl0',sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addSeason(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)	

    else:
        sPattern = '<a class="epNum" href="([^"]+)".+?<span>(.+?)</span>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler()    
            for aEntry in aResult[1]:
 
                sTitle =  f'{sMovieTitle} E{aEntry[1]}'
                siteUrl = f'{aEntry[0]}?do=watch'
                sThumb = sThumb
                sDesc = ''

                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        sPattern = '<a class="epNum.+?" href="([^"]+)".+?<span>(.+?)</span>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler()    
            for aEntry in aResult[1]:
 
                sTitle = f'{sMovieTitle} E{aEntry[1]}'
                siteUrl = f'{aEntry[0]}?do=watch'
                sThumb = sThumb
                sDesc = ''

                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showEps():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sUrl0 = oInputParameterHandler.getValue('siteUrl0')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl0)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    siteUrl = str(sUrl).split('?')[0]

    sCode = sUrl.split('seriesID=')[1]
    cook = oRequestHandler.GetCookies()
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Accept', '*/*')
    oRequestHandler.addHeaderEntry('x-requested-with', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', sUrl0.encode('utf-8'))
    oRequestHandler.addHeaderEntry('Cookie', cook)
    oRequestHandler.addParameters('seriesID', sCode)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'href="([^"]+)".+?<span>(.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)  
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
 
            sTitle = f'{sMovieTitle} E{aEntry[1].replace("الحلقة "," E").replace("حلقة "," E")}'
            siteUrl = f'{aEntry[0]}?do=watch'
            sThumb = sThumb
            sDesc = ''
 
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
 
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
    oGui.setEndOfDirectory() 

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    Referer = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern =  '<link rel=["\']shortlink["\'] href=["\']([^"\']+)["\']' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        sPage = aResult[1][0].split('?p=')[1]

    sPattern = 'id="s_.+?onClick=".*?getServer2([^"]+)"'
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            ServerIDs = aEntry.replace('(this.id,','').replace(');','') 
            sHosterID = ServerIDs.split(',')[0]
            serverId = ServerIDs.split(',')[1]
      
            url = f'{URL_MAIN}wp-content/themes/vo2023/temp/ajax/iframe2.php?id={sPage}&video={sHosterID}&serverId={serverId}'

            oRequestHandler = cRequestHandler(url)
            cook = oRequestHandler.GetCookies()
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Referer', Referer.encode('utf-8'))
            oRequestHandler.addHeaderEntry('Cookie', cook.encode('utf-8'))
            oRequestHandler.addHeaderEntry('sec-fetch-dest', 'empty'.encode('utf-8'))
            oRequestHandler.addHeaderEntry('sec-fetch-mode', 'cors'.encode('utf-8'))
            oRequestHandler.addHeaderEntry('x-requested-with', 'XMLHttpRequest')
            sHtmlContent2 = oRequestHandler.request()
    
            sPattern = 'iframe.+?src=["\']([^"\']+)["\']'
            aResult = oParser.parse(sHtmlContent2, sPattern)
            if aResult[0]:
                oOutputParameterHandler = cOutputParameterHandler()
                sHosterUrl = aResult[1][0]

                if bool(re.search(r'mega.*max', sHosterUrl)) or '/iframe/' in sHosterUrl:
                    data = cMegamax().GetUrls(sHosterUrl)
                    if data is not False:
                        for item in data:
                            sHosterUrl = item.split(',')[0].split('=')[1]
                            sQual = item.split(',')[1].split('=')[1]
                            sLabel = item.split(',')[2].split('=')[1]

                            sDisplayTitle = f'{sMovieTitle} [COLOR coral] [{sQual}][/COLOR][COLOR orange] - {sLabel}[/COLOR]'
                            oOutputParameterHandler.addParameter('sHosterUrl', sHosterUrl)
                            oOutputParameterHandler.addParameter('siteUrl', sUrl)
                            oOutputParameterHandler.addParameter('sQual', sQual)
                            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                            oOutputParameterHandler.addParameter('sThumb', sThumb)

                            oGui.addLink(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, sThumb, sDisplayTitle, oOutputParameterHandler)

                if 'mystream' in sHosterUrl:
                    sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN    
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    else:
        sPattern = 'id="s_.+?onClick=".*?getServer([^"]+)"'
        aResult = oParser.parse(sHtmlContent,sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                sHosterID = aEntry.replace('(this.id,','').replace(');','') 

                url = f'{URL_MAIN}wp-content/themes/vo2023/temp/ajax/iframe.php?id={sPage}&video={sHosterID}'

                oRequestHandler = cRequestHandler(url)
                cook = oRequestHandler.GetCookies()
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Referer', Referer.encode('utf-8'))
                oRequestHandler.addHeaderEntry('Cookie', cook.encode('utf-8'))
                oRequestHandler.addHeaderEntry('sec-fetch-dest', 'empty'.encode('utf-8'))
                oRequestHandler.addHeaderEntry('sec-fetch-mode', 'cors'.encode('utf-8'))
                oRequestHandler.addHeaderEntry('x-requested-with', 'XMLHttpRequest')
                sHtmlContent2 = oRequestHandler.request()
    
                sPattern = 'iframe.+?src=["\']([^"\']+)["\']'
                aResult = oParser.parse(sHtmlContent2, sPattern)
                if aResult[0]:
                    oOutputParameterHandler = cOutputParameterHandler()
                    sHosterUrl = aResult[1][0]

                    if bool(re.search(r'mega.*max', sHosterUrl)) or '/iframe/' in sHosterUrl:
                        data = cMegamax().GetUrls(sHosterUrl)
                        if data is not False:
                            for item in data:
                                sHosterUrl = item.split(',')[0].split('=')[1]
                                sQual = item.split(',')[1].split('=')[1]
                                sLabel = item.split(',')[2].split('=')[1]

                                sDisplayTitle = f'{sMovieTitle} [COLOR coral] [{sQual}][/COLOR][COLOR orange] - {sLabel}[/COLOR]'     
                                oOutputParameterHandler.addParameter('sHosterUrl', sHosterUrl)
                                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                                oOutputParameterHandler.addParameter('sQual', sQual)
                                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                                oOutputParameterHandler.addParameter('sThumb', sThumb)

                                oGui.addLink(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, sThumb, sDisplayTitle, oOutputParameterHandler)
  
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if oHoster:
                        oHoster.setDisplayName(sMovieTitle)
                        oHoster.setFileName(sMovieTitle)
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