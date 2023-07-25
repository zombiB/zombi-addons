import re
import requests	

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress,VSlog, siteManager, dialog, addon


SITE_IDENTIFIER = 'nabdhlb'
SITE_NAME = 'Nabd8lb'
SITE_DESC = 'Online Movies and TV Shows'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (URL_MAIN + 'category/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%a7%d8%ac%d9%86%d8%a8%d9%8a%d8%a9/', 'showMovies')
MOVIE_TURK = (URL_MAIN + 'category/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d8%aa%d8%b1%d9%83%d9%8a%d8%a9/', 'showMovies')
MOVIE_HI = (URL_MAIN + 'category/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d9%87%d9%86%d8%af%d9%8a%d8%a9/', 'showMovies')
MOVIE_PAK = (URL_MAIN + 'category/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d8%a8%d8%a7%d9%83%d8%b3%d8%aa%d8%a7%d9%86%d9%8a%d8%a9/', 'showMovies')
MOVIE_ASIAN = (URL_MAIN + 'category/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d8%a7%d8%b3%d9%8a%d9%88%d9%8a%d8%a9/', 'showMovies')
MOVIE_VIET = (URL_MAIN + 'category/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d9%81%d9%84%d8%a8%d9%8a%d9%86%d9%8a%d8%a9/', 'showMovies')
KID_MOVIES = (URL_MAIN + 'category/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d8%a3%d9%86%d9%85%d9%8a-%d9%83%d8%b1%d8%aa%d9%88%d9%86/', 'showMovies')
SERIE_TR = (URL_MAIN + 'category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%aa%d8%b1%d9%83%d9%8a%d8%a9-%d9%85%d8%aa%d8%b1%d8%ac%d9%85%d8%a9/', 'showSeries')
SERIE_TR_AR = (URL_MAIN + 'category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%aa%d8%b1%d9%83%d9%8a%d8%a9-%d9%85%d8%af%d8%a8%d9%84%d8%ac%d8%a9/', 'showSeries')
SERIE_EN = (URL_MAIN + 'category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%a7%d8%ac%d9%86%d8%a8%d9%8a%d8%a9/', 'showSeries')
SERIE_AR = (URL_MAIN + 'category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%b9%d8%b1%d8%a8%d9%8a%d8%a9-%d8%ad%d8%b5%d8%b1%d9%8a%d8%a9/', 'showSeries')
SERIE_ASIA = (URL_MAIN + 'category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%a7%d8%b3%d9%8a%d9%88%d9%8a%d8%a9/', 'showSeries')
SERIE_THAI = (URL_MAIN + 'category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%aa%d8%a7%d9%8a%d9%84%d9%86%d8%af%d9%8a%d8%a9-%d9%88-%d8%a7%d9%84%d8%aa%d8%a7%d9%8a%d9%88%d8%a7%d9%86%d9%8a%d8%a9/', 'showSeries')
SERIE_FI = (URL_MAIN + 'category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d9%81%d9%84%d8%a8%d9%8a%d9%86%d9%8a%d8%a9/', 'showSeries')
SERIE_MAL = (URL_MAIN + 'category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d9%85%d8%a7%d9%84%d9%8a%d8%b2%d9%8a%d8%a9/', 'showSeries')
SERIE_HEND = (URL_MAIN + 'category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d9%87%d9%86%d8%af%d9%8a%d8%a9-%d9%85%d8%aa%d8%b1%d8%ac%d9%85%d8%a9/', 'showSeries')
SERIE_HEND_AR = (URL_MAIN + 'category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d9%87%d9%86%d8%af%d9%8a%d8%a9-%d9%85%d8%af%d8%a8%d9%84%d8%ac%d8%a9/', 'showSeries')
SERIE_PAK = (URL_MAIN + 'category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%a8%d8%a7%d9%83%d8%b3%d8%aa%d8%a7%d9%86%d9%8a%d8%a9/', 'showSeries')
SERIE_LATIN = (URL_MAIN + 'category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d9%84%d8%a7%d8%aa%d9%8a%d9%86%d9%8a%d8%a9-%d9%88-%d9%85%d9%83%d8%b3%d9%8a%d9%83%d9%8a%d8%a9/', 'showSeries')

RAMDAN_SERIES = (URL_MAIN +'category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%b1%d9%85%d8%b6%d8%a7%d9%86-2022/', 'showSeries')


URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?s=', 'showSeries')
FUNCTION_SEARCH = 'showMovies'

sitemsList = []
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', 'Search Series', 'search.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Search Movies', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_EN[1], 'أفلام اجنبية', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TURK[1], 'أفلام تركية', 'turk.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ASIAN[1], 'أفلام آسيوية', 'asia.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIET[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIET[1], 'أفلام فيتنامية', 'viet.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HI[1], 'أفلام هندية', 'hend.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_PAK[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_PAK[1], 'أفلام باكستانية', 'paki.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, KID_MOVIES[1], 'أفلام اطفال', 'crtoon.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_EN[1], 'مسلسلات اجنبية', 'agnab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_AR[1], 'مسلسلات عربية', 'arab.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_TR[1], 'مسلسلات تركية', 'turk.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR_AR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_TR_AR[1], 'مسلسلات تركية مدبلجة', 'turk.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_ASIA[1], 'مسلسلات آسيوية', 'asia.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_THAI[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_THAI[1], 'مسلسلات تايلاندية', 'thai.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_FI[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_FI[1], 'مسلسلات فلبينية', 'asia.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_MAL[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_MAL[1], 'مسلسلات ماليزية', 'asia.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_HEND[1], 'مسلسلات هندية', 'hend.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND_AR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_HEND_AR[1], 'مسلسلات هندية مدبلج', 'hend.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_PAK[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_PAK[1], 'مسلسلات باكستانية', 'paki.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_LATIN[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_LATIN[1], 'مسلسلات لاتينية', 'latin.png', oOutputParameterHandler)

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
    cook = oRequestHandler.GetCookies()
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('Referer', sUrl.encode('utf-8'))
    oRequestHandler.addHeaderEntry('Cookie', cook.encode('utf-8'))
    oRequestHandler.addHeaderEntry('authority', 'nabd8lb.net'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('upgrade-insecure-requests', '1')
    oRequestHandler.addHeaderEntry('sec-fetch-dest', 'document'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('sec-fetch-mode', 'navigate'.encode('utf-8'))   
    sHtmlContent = oRequestHandler.request()
    
    sPattern = '<div class="block-post">.+?href="([^"]+)" title="([^"]+)".+?src=(.+?) class='
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

            if not '/movie' in aEntry[0]:
                continue 
            siteUrl = aEntry[0]+'?do=views'
            sTitle = aEntry[1].replace("مترجم ","").replace("مترجم","").replace("مدبلج ","").replace("فيلم","").replace("+","").replace("حلقات","").replace("الحلقات","").replace("فلم"," ").replace('مترجمة','').replace('اونلاين','').replace('أونلاين','').replace('اون لاين','').replace('أون لاين','').replace('مترجم','').replace('للعربية','').replace('للعربي','').replace('-','').replace('كامل','').replace('مشاهدة','').strip()
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')

            sThumb = aEntry[2].replace('background-image:url(','').replace(");","").replace("'","")

            if sThumb.startswith('//'):
                sThumb = 'https:' + sThumb
            
            sDesc = ''
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
    
    oRequestHandler = cRequestHandler(sUrl)
    cook = oRequestHandler.GetCookies()
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('Referer', sUrl.encode('utf-8'))
    oRequestHandler.addHeaderEntry('Cookie', cook.encode('utf-8'))
    oRequestHandler.addHeaderEntry('authority', 'nabd8lb.net'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('upgrade-insecure-requests', '1')
    oRequestHandler.addHeaderEntry('sec-fetch-dest', 'document'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('sec-fetch-mode', 'navigate'.encode('utf-8'))
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="block-post">.+?href="([^"]+)" title="([^"]+)".+?src=(.+?) class='
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

            if '/movie' in aEntry[0]:
                continue 
            siteUrl = aEntry[0]
            sTitle = aEntry[1].replace("مشاهدة","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","").split("الموسم")[0].split("موسم")[0].split("الحلقة")[0].strip()
            sTitle = re.sub(r'/(19|20)[0-9][0-9]/', '', sTitle)
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')

            sThumb = aEntry[2].replace('background-image:url(','').replace(");","").replace("'","")

            if sThumb.startswith('//'):
                sThumb = 'https:' + sThumb
            
            sDesc = ''
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
 			
def showSeasons(sSearch=''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oRequestHandler = cRequestHandler(sUrl)
    cook = oRequestHandler.GetCookies()
    oRequestHandler.addHeaderEntry('user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('cookie', cook.encode('utf-8'))
    oRequestHandler.addHeaderEntry('authority', 'nabd8lb.net'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('upgrade-insecure-requests', '1')
    oRequestHandler.addHeaderEntry('sec-fetch-dest', 'document'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('sec-fetch-mode', 'navigate'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('sec-fetch-site', 'none'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('sec-fetch-user', '?1'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('sec-ch-ua-mobile', '?0'.encode('utf-8'))
    
    sHtmlContent = oRequestHandler.request()
        
    oParser = cParser()
    sPattern =  'data-season="([^"]+)">(.+?)</li>' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
    
            seriesID = aEntry[0]
            siteUrl = URL_MAIN + 'wp-content/themes/vo2022/temp/ajax/seasons.php?seriesID=' + seriesID
            sTitle = aEntry[1].replace("مترجم ","").replace("مترجم","").replace("مدبلج ","").replace("مدبلج","").strip()
            sDisplayTitle = sTitle.replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم السابع والعشرون","S27").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الثالث و الثلاثون","S33").replace("الموسم الأول","S1").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("S ","S")
            sYear = ''
            sDesc = ''
            
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle + ' ' + sDisplayTitle)
            oOutputParameterHandler.addParameter('siteUrl',  siteUrl) 
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear',sYear)
            oOutputParameterHandler.addParameter('sDesc',sDesc)
            
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes' , sDisplayTitle, sYear, sThumb, sDesc, oOutputParameterHandler)
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
 
def showEpisodes(sSearch=''):
    oGui = cGui()
       
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    Referer = sUrl
        
    oRequestHandler = cRequestHandler(sUrl)
    cook = oRequestHandler.GetCookies()
    oRequestHandler.addHeaderEntry('user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'.encode('utf-8'))
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
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            siteUrl = aEntry[0]+'?do=views'
        
            sTitle = ' E' + aEntry[1]
            sTitle = sMovieTitle+sTitle

            sYear = ''
            sDesc = ''
        
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('siteUrl',  siteUrl) 
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear',sYear)
            oOutputParameterHandler.addParameter('sDesc',sDesc)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters' , sTitle , sYear, sThumb, sDesc, oOutputParameterHandler)
      
    oGui.setEndOfDirectory()	
   
def __checkForNextPage(sHtmlContent):
    sPattern = '<link rel="next" href="([^"]+)'
	
    oParser = cParser()
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

    oRequestHandler = cRequestHandler(sUrl)
    cook = oRequestHandler.GetCookies()  
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern =  'data-content-id="([^"]+)' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        sID = aResult[1][0] 

    ## Watch Servers
    sPattern = 'id="s_.+?onClick="([^"]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            ServerIDs = aEntry.replace('getServer2(this.id,','').replace(');','') 
            sHosterID = ServerIDs.split(',')[0]
            serverId = ServerIDs.split(',')[1]
      
            url = URL_MAIN + 'wp-content/themes/vo2022/temp/ajax/iframe2.php?id=' + sID + '&video=' + sHosterID + '&serverId=' + serverId
            oRequestHandler = cRequestHandler(url)
            cook = oRequestHandler.GetCookies()
            oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'.encode('utf-8'))
            oRequestHandler.addHeaderEntry('Referer', Referer.encode('utf-8'))
            oRequestHandler.addHeaderEntry('Cookie', cook.encode('utf-8'))
            oRequestHandler.addHeaderEntry('authority', 'nabd8lb.net'.encode('utf-8'))
            oRequestHandler.addHeaderEntry('sec-fetch-dest', 'empty'.encode('utf-8'))
            oRequestHandler.addHeaderEntry('sec-fetch-mode', 'cors'.encode('utf-8'))
            oRequestHandler.addHeaderEntry('x-requested-with', 'XMLHttpRequest')
            sHtmlContent2 = oRequestHandler.request()
    
            sPattern = 'iframe.+?src=\"(.+?)\"'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent2.lower(), sPattern)
            if aResult[0]:
                sHosterUrl = aResult[1][0]

                if 'mystream' in sHosterUrl:
                    sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN    
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster != False:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
                       

    oGui.setEndOfDirectory()