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
from resources.lib import random_ua

UA = random_ua.get_ua()

SITE_IDENTIFIER = 'nabdhlb'
SITE_NAME = 'Nabd8lb'
SITE_DESC = 'Online Movies and TV Shows'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (f'{URL_MAIN}category/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%a7%d8%ac%d9%86%d8%a8%d9%8a%d8%a9/', 'showMovies')
MOVIE_TURK = (f'{URL_MAIN}category/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d8%aa%d8%b1%d9%83%d9%8a%d8%a9/', 'showMovies')
MOVIE_HI = (f'{URL_MAIN}category/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d9%87%d9%86%d8%af%d9%8a%d8%a9/', 'showMovies')
MOVIE_PAK = (f'{URL_MAIN}category/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d8%a8%d8%a7%d9%83%d8%b3%d8%aa%d8%a7%d9%86%d9%8a%d8%a9/', 'showMovies')
MOVIE_ASIAN = (f'{URL_MAIN}category/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d8%a7%d8%b3%d9%8a%d9%88%d9%8a%d8%a9/', 'showMovies')
MOVIE_VIET = (f'{URL_MAIN}category/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d9%81%d9%84%d8%a8%d9%8a%d9%86%d9%8a%d8%a9/', 'showMovies')
KID_MOVIES = (f'{URL_MAIN}category/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d8%a3%d9%86%d9%85%d9%8a-%d9%83%d8%b1%d8%aa%d9%88%d9%86/', 'showMovies')

SERIE_TR = (f'{URL_MAIN}category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%aa%d8%b1%d9%83%d9%8a%d8%a9-%d9%85%d8%aa%d8%b1%d8%ac%d9%85%d8%a9/', 'showSeries')
SERIE_TR_AR = (f'{URL_MAIN}category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%aa%d8%b1%d9%83%d9%8a%d8%a9-%d9%85%d8%af%d8%a8%d9%84%d8%ac%d8%a9/', 'showSeries')
SERIE_EN = (f'{URL_MAIN}category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%a7%d8%ac%d9%86%d8%a8%d9%8a%d8%a9/', 'showSeries')
SERIE_AR = (f'{URL_MAIN}category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%b9%d8%b1%d8%a8%d9%8a%d8%a9-%d8%ad%d8%b5%d8%b1%d9%8a%d8%a9/', 'showSeries')
SERIE_ASIA = (f'{URL_MAIN}category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%a7%d8%b3%d9%8a%d9%88%d9%8a%d8%a9/', 'showSeries')
SERIE_THAI = (f'{URL_MAIN}category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%aa%d8%a7%d9%8a%d9%84%d9%86%d8%af%d9%8a%d8%a9-%d9%88-%d8%a7%d9%84%d8%aa%d8%a7%d9%8a%d9%88%d8%a7%d9%86%d9%8a%d8%a9/', 'showSeries')
SERIE_FI = (f'{URL_MAIN}category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d9%81%d9%84%d8%a8%d9%8a%d9%86%d9%8a%d8%a9/', 'showSeries')
SERIE_MAL = (f'{URL_MAIN}category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d9%85%d8%a7%d9%84%d9%8a%d8%b2%d9%8a%d8%a9/', 'showSeries')
SERIE_HEND = (f'{URL_MAIN}category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d9%87%d9%86%d8%af%d9%8a%d8%a9-%d9%85%d8%aa%d8%b1%d8%ac%d9%85%d8%a9/', 'showSeries')
SERIE_HEND_AR = (f'{URL_MAIN}category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d9%87%d9%86%d8%af%d9%8a%d8%a9-%d9%85%d8%af%d8%a8%d9%84%d8%ac%d8%a9/', 'showSeries')
SERIE_PAK = (f'{URL_MAIN}category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%a8%d8%a7%d9%83%d8%b3%d8%aa%d8%a7%d9%86%d9%8a%d8%a9/', 'showSeries')
SERIE_LATIN = (f'{URL_MAIN}category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d9%84%d8%a7%d8%aa%d9%8a%d9%86%d9%8a%d8%a9-%d9%88-%d9%85%d9%83%d8%b3%d9%8a%d9%83%d9%8a%d8%a9/', 'showSeries')
RAMDAN_SERIES = (URL_MAIN +'category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%b1%d9%85%d8%b6%d8%a7%d9%86-2022/', 'showSeries')

URL_SEARCH = (f'{URL_MAIN}?s=', 'showMovies')
URL_SEARCH_MOVIES = (f'{URL_MAIN}?s=', 'showMovies')
URL_SEARCH_SERIES = (f'{URL_MAIN}?s=', 'showSeries')
FUNCTION_SEARCH = 'showMovies'

sitemsList = []
def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', addons.VSlang(30079), '1/Search.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_EN[1], 'أفلام اجنبية', '1/Movies.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TURK[1], 'أفلام تركية', '1/Turkish.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ASIAN[1], 'أفلام آسيوية', '1/Asian.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIET[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIET[1], 'أفلام فيتنامية', '1/Vietnamese.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HI[1], 'أفلام هندية', '1/Hindi.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_PAK[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_PAK[1], 'أفلام باكستانية', 'paki.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, KID_MOVIES[1], 'أفلام اطفال', 'crtoon.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_EN[1], 'مسلسلات اجنبية', '1/Movies.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_AR[1], 'مسلسلات عربية', '1/Arabic.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_TR[1], 'مسلسلات تركية', '1/Turkish.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR_AR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_TR_AR[1], 'مسلسلات تركية مدبلجة', '1/Turkish.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_ASIA[1], 'مسلسلات آسيوية', '1/Asian.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_THAI[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_THAI[1], 'مسلسلات تايلاندية', '1/Thai.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_FI[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_FI[1], 'مسلسلات فلبينية', '1/Asian.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_MAL[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_MAL[1], 'مسلسلات ماليزية', '1/Asian.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_HEND[1], 'مسلسلات هندية', '1/Hindi.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND_AR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_HEND_AR[1], 'مسلسلات هندية مدبلج', '1/Hindi.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_PAK[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_PAK[1], 'مسلسلات باكستانية', 'paki.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_LATIN[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_LATIN[1], 'مسلسلات لاتينية', 'latin.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}?s={sSearchText}'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return 

def showSearchSeries():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = f'{URL_MAIN}?s={sSearchText}'
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
    cook = oRequestHandler.GetCookies()
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', sUrl.encode('utf-8'))
    oRequestHandler.addHeaderEntry('Cookie', cook.encode('utf-8'))
    oRequestHandler.addHeaderEntry('authority', 'nabd8lb.net'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('upgrade-insecure-requests', '1')
    oRequestHandler.addHeaderEntry('sec-fetch-dest', 'document'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('sec-fetch-mode', 'navigate'.encode('utf-8'))   
    sHtmlContent = oRequestHandler.request()
    
    sPattern = '<div class="block-post">.+?href="([^"]+)" title="([^"]+)".+?src=(.+?) class='
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if not '/movie' in aEntry[0]:
                continue 

            siteUrl = f'{aEntry[0]}?do=views'
            sTitle = cUtil().CleanMovieName(aEntry[1])
            sThumb = aEntry[2].replace('background-image:url(','').replace(");","").replace("'","")
            if sThumb.startswith('//'):
                sThumb = f'https:{sThumb}'          
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))

            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('siteUrl',  siteUrl) 
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear',sYear)

            if '/movie' in siteUrl:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters' , sTitle, sYear, sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addTV(SITE_IDENTIFIER, 'showSeasons' , sTitle, sYear, sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)  
    
        sNextPage = __checkForNextPage(sHtmlContent)
        oOutputParameterHandler = cOutputParameterHandler()
        if sNextPage:
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
    cook = oRequestHandler.GetCookies()
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', sUrl.encode('utf-8'))
    oRequestHandler.addHeaderEntry('Cookie', cook.encode('utf-8'))
    oRequestHandler.addHeaderEntry('authority', 'nabd8lb.net'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('upgrade-insecure-requests', '1')
    oRequestHandler.addHeaderEntry('sec-fetch-dest', 'document'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('sec-fetch-mode', 'navigate'.encode('utf-8'))
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="block-post">.+?href="([^"]+)" title="([^"]+)".+?src=(.+?) class='
    aResult = oParser.parse(sHtmlContent, sPattern)   
    itemList = []	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if '/movie' in aEntry[0]:
                continue 

            siteUrl = aEntry[0]
            sTitle = cUtil().CleanSeriesName(aEntry[1]).replace('S ','S')
            sTitle = re.sub(r"S\d{1,2}", "", sTitle)
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
            sThumb = aEntry[2].replace('background-image:url(','').replace(");","").replace("'","")
            if sThumb.startswith('//'):
                sThumb = f'https:{sThumb}'     
            sDesc = ''

            if sTitle not in itemList:
                itemList.append(sTitle)	
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('siteUrl',  siteUrl) 
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sYear',sYear)
        
                if '/movie' in siteUrl:
                    oGui.addMovie(SITE_IDENTIFIER, 'showHosters' , sTitle, sYear, sThumb, sDesc, oOutputParameterHandler)
                else:
                    oGui.addTV(SITE_IDENTIFIER, 'showSeasons' , sTitle, sYear, sThumb, sDesc, oOutputParameterHandler)
        progress_.VSclose(progress_)  

        sNextPage = __checkForNextPage(sHtmlContent)
        oOutputParameterHandler = cOutputParameterHandler()
        if sNextPage:
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
    cook = oRequestHandler.GetCookies()
    oRequestHandler.addHeaderEntry('user-agent', UA)
    oRequestHandler.addHeaderEntry('cookie', cook.encode('utf-8'))
    oRequestHandler.addHeaderEntry('authority', 'nabd8lb.net'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('upgrade-insecure-requests', '1')
    oRequestHandler.addHeaderEntry('sec-fetch-dest', 'document'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('sec-fetch-mode', 'navigate'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('sec-fetch-site', 'none'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('sec-fetch-user', '?1'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('sec-ch-ua-mobile', '?0'.encode('utf-8'))
    sHtmlContent = oRequestHandler.request()
        
    sPattern =  'data-season="([^"]+)">(.+?)</li>' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()   
        for aEntry in aResult[1]:
    
            seriesID = aEntry[0]
            siteUrl = f'{URL_MAIN}wp-content/themes/vo2022/temp/ajax/seasons.php?seriesID={seriesID}'
            sTitle = f"{sMovieTitle} {cUtil().CleanSeriesName(aEntry[1]).replace('S ','S')}"
            sYear = ''
            sDesc = ''
            
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('siteUrl', siteUrl) 
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes' , sTitle, sYear, sThumb, sDesc, oOutputParameterHandler)
    else:
        oOutputParameterHandler = cOutputParameterHandler()
        sTitle = sMovieTitle + ' S1'
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('siteUrl',  sUrl) 
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sYear','')
        oOutputParameterHandler.addParameter('sDesc','')
            
        oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes' , sTitle, '', sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()
 
def showEpisodes():
    oGui = cGui()
       
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    Referer = sUrl

    oParser = cParser()        
    oRequestHandler = cRequestHandler(sUrl)
    cook = oRequestHandler.GetCookies()
    oRequestHandler.addHeaderEntry('user-agent', UA)
    oRequestHandler.addHeaderEntry('referer', Referer.encode('utf-8'))
    oRequestHandler.addHeaderEntry('cookie', cook.encode('utf-8'))
    oRequestHandler.addHeaderEntry('authority', 'nabd8lb.net'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('sec-fetch-dest', 'empty'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('sec-fetch-mode', 'cors'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('sec-fetch-site', 'same-origin'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('sec-ch-ua-mobile', '?0'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('x-requested-with', 'XMLHttpRequest') 
    sHtmlContent = oRequestHandler.request()

    sPattern = 'class="epNum" href="([^"]+)".+?<span>(.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:

            siteUrl = f'{aEntry[0]}?do=views'
            sTitle = f'{sMovieTitle} E{aEntry[1]}'
            sYear = ''
            sDesc = ''
        
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('siteUrl', siteUrl) 
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters' , sTitle , sYear, sThumb, sDesc, oOutputParameterHandler)
      
    oGui.setEndOfDirectory()	
   
def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<link rel="next" href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    Referer = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    cook = oRequestHandler.GetCookies()  
    sHtmlContent = oRequestHandler.request()

    sPattern =  'vo_postID="([^"]+)' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        sID = aResult[1][0] 

    sPattern = 'id="s_.+?onClick="([^"]+)'
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            ServerIDs = aEntry.replace('getServer2(this.id,','').replace(');','') 
            sHosterID = ServerIDs.split(',')[0]
            serverId = ServerIDs.split(',')[1]
      
            url = f'{URL_MAIN}wp-content/themes/vo2022/temp/ajax/iframe2.php?id={sID}&video={sHosterID}&serverId={serverId}'
            oRequestHandler = cRequestHandler(url)
            cook = oRequestHandler.GetCookies()
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Referer', Referer.encode('utf-8'))
            oRequestHandler.addHeaderEntry('Cookie', cook.encode('utf-8'))
            oRequestHandler.addHeaderEntry('authority', 'nabd8lb.net'.encode('utf-8'))
            oRequestHandler.addHeaderEntry('sec-fetch-dest', 'empty'.encode('utf-8'))
            oRequestHandler.addHeaderEntry('sec-fetch-mode', 'cors'.encode('utf-8'))
            oRequestHandler.addHeaderEntry('x-requested-with', 'XMLHttpRequest')
            sHtmlContent2 = oRequestHandler.request()
    
            sPattern = 'iframe.+?src=\"(.+?)\"'
            aResult = oParser.parse(sHtmlContent2, sPattern)
            if aResult[0]:
                sHosterUrl = aResult[1][0]
 
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
                       
    oGui.setEndOfDirectory()