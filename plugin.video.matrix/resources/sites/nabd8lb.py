import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress,VSlog, siteManager, dialog, addon
from resources.lib.util import cUtil, Unquote, urlEncode, Quote
from resources.lib.Styling import getFunc, getThumb, getGenreIcon
from bs4 import BeautifulSoup
import requests
try:  # Python 2
    import urllib2
    from urllib2 import URLError as UrlError

except ImportError:  # Python 3
    import urllib.request as urllib2
    from urllib.error import URLError as UrlError

ADDON = addon()
icons = ADDON.getSetting('defaultIcons')

SITE_IDENTIFIER = 'nabd8lb'
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


URL_SEARCH_MOVIES = (URL_MAIN + '?s=', 'showSearchMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?s=', 'showSearchSeries')
FUNCTION_SEARCH = 'showSearchSeries'
sitemsList = []
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', 'Search Series', icons + '/Search.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchMovies', 'Search Movies', icons + '/Search.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_EN[1], 'أفلام اجنبية', icons + '/Movies.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TURK[1], 'أفلام تركية', icons + '/Turkish.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ASIAN[1], 'أفلام آسيوية', icons + '/Asian.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIET[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIET[1], 'أفلام فيتنامية', icons + '/Vietnamese.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HI[1], 'أفلام هندية', icons + '/Hindi.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_PAK[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_PAK[1], 'أفلام باكستانية', icons + '/Pakistani.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, KID_MOVIES[1], 'أفلام اطفال', icons + '/Kids.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_EN[1], 'مسلسلات اجنبية', icons + '/TVShows.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_AR[1], 'مسلسلات عربية', icons + '/Arabic.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_TR[1], 'مسلسلات تركية', icons + '/Turkish.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR_AR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_TR_AR[1], 'مسلسلات تركية مدبلجة', icons + '/TVShowsTurkish-Dubbed.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_ASIA[1], 'مسلسلات آسيوية', icons + '/Asian.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_THAI[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_THAI[1], 'مسلسلات تايلاندية', icons + '/Thai.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_FI[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_FI[1], 'مسلسلات فلبينية', icons + '/Filipino.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_MAL[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_MAL[1], 'مسلسلات ماليزية', icons + '/Asian.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_HEND[1], 'مسلسلات هندية', icons + '/Hindi.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND_AR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_HEND_AR[1], 'مسلسلات هندية مدبلج', icons + '/TVShowsHindi-Dubbed.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_PAK[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_PAK[1], 'مسلسلات باكستانية', icons + '/Pakistani.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_LATIN[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_LATIN[1], 'مسلسلات لاتينية', icons + '/Latin.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

 
def showSearchSeries(sSearchText=''):
    oGui = cGui()
    if sSearchText in [None,'',' ']:
        sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '?s='+sSearchText
        showSeriesSearch(sSearch=sUrl,stype = 'Movies')
        oGui.setEndOfDirectory()
        return  

def showSearchMovies(sSearchText=''):
    oGui = cGui()
    if sSearchText in [None,'',' ']:
        sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '?s='+sSearchText
        showSeriesSearch(sSearch=sUrl,stype = 'Movies')
        oGui.setEndOfDirectory()
        return  
        
def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
    
    #VSlog(sUrl)
    
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
    
    soup = BeautifulSoup(sHtmlContent, "html.parser")
    GridSoup = soup.find("div",{"class":"sec-line m-h500"})

    GridItems = soup.findAll("div",{"class":"block-post"})

    oOutputParameterHandler = cOutputParameterHandler()
    for item in GridItems:
        #VSlog(item)
        siteUrl = item.a['href']+ '?do=views' + '|Referer=' + item.a['href']
        sTitle = item.find("div",{"class":"title"}).text.replace("مترجم ","").replace("مترجم","").replace("مدبلج ","").replace("فيلم","").replace("+","").replace("حلقات","").replace("الحلقات","").replace("فلم"," ").replace('مترجمة','').replace('اونلاين','').replace('أونلاين','').replace('اون لاين','').replace('أون لاين','').replace('مترجم','').replace('للعربية','').replace('للعربي','').replace('-','').replace('كامل','').replace('مشاهدة','').strip()
        sYear = ''
        sTitle = re.sub(r'/(19|20)[0-9][0-9]/', '', sTitle)
        #VSlog(sTitle)

        sThumb = item.a.div.div['data-wpfc-original-src'].replace('background-image:url(','').replace(");","")

        #VSlog(siteUrl)
        if sThumb.startswith('//'):
            sThumb = 'https:' + sThumb
            
        #sThumb = re.sub(r'-\d*x\d*.','.', sThumb)
        #VSlog(sThumb)
        sDesc = ''
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('siteUrl',  siteUrl) 
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sYear',sYear)
        
        oGui.addTV(SITE_IDENTIFIER, 'showHosters' , sTitle, sYear, sThumb, sDesc, oOutputParameterHandler)
    
    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        oOutputParameterHandler = cOutputParameterHandler()
        if sNextPage:
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)
        oGui.setEndOfDirectory()

def showSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
    
    # if 'page' not in sUrl:
        # sUrl = sUrl + 'page/1/'
    #VSlog(sUrl)
    
    oRequestHandler = cRequestHandler(sUrl)
    cook = oRequestHandler.GetCookies()
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('Referer', sUrl.encode('utf-8'))
    oRequestHandler.addHeaderEntry('Cookie', cook.encode('utf-8'))
    oRequestHandler.addHeaderEntry('authority', 'nabd8lb.net'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('upgrade-insecure-requests', '1')
    oRequestHandler.addHeaderEntry('sec-fetch-dest', 'document'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('sec-fetch-mode', 'navigate'.encode('utf-8'))
    #oRequestHandler.addHeaderEntry('x-requested-with', 'XMLHttpRequest')
    sHtmlContent = oRequestHandler.request()

    
    soup = BeautifulSoup(sHtmlContent, "html.parser")
    GridSoup = soup.find("div",{"class":"sec-line m-h500"})

    GridItems = soup.findAll("div",{"class":"block-post"})
    #VSlog(sHtmlContent)
    oOutputParameterHandler = cOutputParameterHandler()
    for item in GridItems:
        #VSlog(item)
        siteUrl = item.a['href']+ '|Referer=' + item.a['href']
        sTitle = item.find("div",{"class":"title"}).text.replace('مترجمة','').replace('اونلاين','').replace('أونلاين','').replace('اون لاين','').replace('أون لاين','').replace('مترجم','').replace(' حلقة',' الحلقة').replace(' حلقه',' الحلقة').replace(' موسم',' الموسم').replace('للعربية','').replace('للعربي','').replace('-','').replace('كامل','').replace('مشاهدة','').split("الموسم")[0].split("الحلقة")[0].strip()
        sTitle = re.sub(r'/(19|20)[0-9][0-9]/', '', sTitle)
        sYear = ''
        #VSlog(sTitle)

        sThumb = item.a.div.div['data-wpfc-original-src'].replace('background-image:url(','').replace(");","")

        VSlog(siteUrl)
        if sThumb.startswith('//'):
            sThumb = 'https:' + sThumb
            
        # if 'webp' not in sThumb:
            # sThumb = re.sub(r'-\d*x\d*.','.', sThumb)
        #VSlog(sThumb)
        sDesc = ''
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('siteUrl',  siteUrl) 
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sYear',sYear)
        

        oGui.addTV(SITE_IDENTIFIER, 'showSeasons' , sTitle, sYear, sThumb, sDesc, oOutputParameterHandler)

    
    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        oOutputParameterHandler = cOutputParameterHandler()
        if sNextPage:
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)
        oGui.setEndOfDirectory()

 			
def showSeasons(sSearch=''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
      Referer = URL_MAIN
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl').split('|Referer=')[0]
        try:
            Referer = oInputParameterHandler.getValue('siteUrl').split('|Referer=')[1]
        except:
            Referer = URL_MAIN
    
    VSlog(sUrl)
    oInputParameterHandler = cInputParameterHandler()
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    cook = oRequestHandler.GetCookies()
    oRequestHandler.addHeaderEntry('user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('referer', Referer.encode('utf-8'))
    oRequestHandler.addHeaderEntry('cookie', cook.encode('utf-8'))
    oRequestHandler.addHeaderEntry('authority', 'nabd8lb.net'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('upgrade-insecure-requests', '1')
    oRequestHandler.addHeaderEntry('sec-fetch-dest', 'document'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('sec-fetch-mode', 'navigate'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('sec-fetch-site', 'none'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('sec-fetch-user', '?1'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('sec-ch-ua-mobile', '?0'.encode('utf-8'))
    
    sHtmlContent = oRequestHandler.request()
        
    soup = BeautifulSoup(sHtmlContent, "html.parser")
    
    try:
        GridSoup = soup.find("div",{"class":"sec-line"}).find("ul",{"class":"listSeasons"})
        GridItems = GridSoup.findAll("li")
        sDesc = ''
        oOutputParameterHandler = cOutputParameterHandler()
        for item in GridItems:
           #VSlog(item)
            seriesID = item['data-season']
            siteUrl = URL_MAIN + 'wp-content/themes/vo2022/temp/ajax/seasons.php?seriesID=' + seriesID + '|Referer=' + sUrl
            sTitle = item.text.replace("مترجم ","").replace("مترجم","").replace("مدبلج ","").replace("مدبلج","").strip()
            sDisplayTitle = sTitle.replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم السابع والعشرون","S27").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الثالث و الثلاثون","S33").replace("الموسم الأول","S1").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("S ","S")
            sYear = ''
            
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle + ' ' + sDisplayTitle)
            oOutputParameterHandler.addParameter('siteUrl',  siteUrl) 
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear',sYear)
            oOutputParameterHandler.addParameter('sDesc',sDesc)
            
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes' , sDisplayTitle, sYear, sThumb, sDesc, oOutputParameterHandler)
    except:
        oOutputParameterHandler = cOutputParameterHandler()
        sTitle = sMovieTitle + ' S1'
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('siteUrl',  sUrl + '|Referer=' + Referer) 
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sYear','')
        oOutputParameterHandler.addParameter('sDesc','')
            
        oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes' , sTitle, '', sThumb, '', oOutputParameterHandler)
    oGui.setEndOfDirectory()
 
def showEpisodes(sSearch=''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
      Referer = URL_MAIN
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl').split('|Referer=')[0]
        try:
            Referer = oInputParameterHandler.getValue('siteUrl').split('|Referer=')[1]
        except:
            Referer = URL_MAIN
    
    #VSlog(sUrl)
    #VSlog(Referer)
    
    oInputParameterHandler = cInputParameterHandler()
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sSaison = oInputParameterHandler.getValue('sSaison')
    sDesc = oInputParameterHandler.getValue('sDesc')
        
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
    #VSlog(sHtmlContent)
    soup = BeautifulSoup(sHtmlContent, "html.parser")
    
    GridItems = soup.findAll("a",{"class":"epNum"})
    itemsList = []
    oOutputParameterHandler = cOutputParameterHandler()
    for item in GridItems:
        VSlog(item)
        siteUrl = item['href'] + '?do=views' + '|Referer=' + item['href']
        VSlog(siteUrl)
        
        sTitle = item['title'].replace("الحلقة "," E").replace("حلقة "," E").strip()
        VSlog(sTitle)
        sYear = ''
        
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('siteUrl',  siteUrl) 
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sYear',sYear)
        oOutputParameterHandler.addParameter('sDesc',sDesc)
        oGui.addEpisode(SITE_IDENTIFIER, 'showHosters' , sTitle , sYear, sThumb, sDesc, oOutputParameterHandler)
    
    sNextPage = __checkForNextPage(sHtmlContent)
    oOutputParameterHandler = cOutputParameterHandler()
    if sNextPage:
        oOutputParameterHandler.addParameter('siteUrl', sNextPage)
        oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)
  
    oGui.setEndOfDirectory()	

def showSeriesSearch(sSearch, stype):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
      Referer = URL_MAIN
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl').split('|Referer=')[0]
        try:
            Referer = oInputParameterHandler.getValue('siteUrl').split('|Referer=')[1]
        except:
            Referer = URL_MAIN
    
    #VSlog(sUrl)
    #VSlog(Referer)
    
    oInputParameterHandler = cInputParameterHandler()
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sSaison = oInputParameterHandler.getValue('sSaison')
    sDesc = oInputParameterHandler.getValue('sDesc')
        
    oRequestHandler = cRequestHandler(sUrl)
    cook = oRequestHandler.GetCookies()
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
    oRequestHandler.addHeaderEntry('Referer', Referer)
    oRequestHandler.addHeaderEntry('Cookie', cook.encode('utf-8'))
    oRequestHandler.addHeaderEntry('authority', '7obtv.top')
    oRequestHandler.addHeaderEntry('x-requested-with', 'XMLHttpRequest')
    
    sHtmlContent = oRequestHandler.request()
    
    soup = BeautifulSoup(sHtmlContent, "html.parser")
    
    GridItems = soup.findAll("div",{"class":"block-post"})

    
    oOutputParameterHandler = cOutputParameterHandler()
    for item in GridItems:
        sTitle = item.find("div",{"class":"title"}).text.replace('مترجمة','').replace('اونلاين','').replace('أونلاين','').replace('اون لاين','').replace('أون لاين','').replace('مترجم','').replace(' حلقة',' الحلقة').replace(' حلقه',' الحلقة').replace(' موسم',' الموسم').replace('للعربية','').replace('للعربي','').replace('-','').replace('كامل','').replace('مشاهدة','').split("الموسم")[0].split("الحلقة")[0].strip()
        sTitle = re.sub(r'/(19|20)[0-9][0-9]/', '', sTitle)
        if sTitle not in sitemsList:
            sitemsList.append(sTitle)
            siteUrl = item.a['href']+ '|Referer=' + item.a['href']
            
            sYear = ''
            #VSlog(sTitle)

            sThumb = item.a.div.div['data-wpfc-original-src'].replace('background-image:url(','').replace(");","")

            #VSlog(siteUrl)
            if sThumb.startswith('//'):
                sThumb = 'https:' + sThumb
                
            #sThumb = re.sub(r'-\d*x\d*.','.', sThumb)
            #VSlog(sThumb)
            sDesc = ''
            
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('siteUrl',  siteUrl) 
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear',sYear)
            oOutputParameterHandler.addParameter('sDesc',sDesc)
            if stype == 'TVShows':
                oGui.addTV(SITE_IDENTIFIER, 'showSeasons' , sTitle, sYear, sThumb, sDesc, oOutputParameterHandler)
            
            if stype == 'Movies':
                oGui.addMovie(SITE_IDENTIFIER, 'showSeasons' , sTitle, sYear, sThumb, sDesc, oOutputParameterHandler)
    
            sNextPage = __checkForNextPage(sHtmlContent)
            oOutputParameterHandler = cOutputParameterHandler()
            if sNextPage:
                showSeriesSearch(sNextPage, stype)
                # oOutputParameterHandler.addParameter('siteUrl', sNextPage)
                # oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)
    # except:
        # oGui.addText('', 'No Episodes Yet',icons + '/None.png')
  
    oGui.setEndOfDirectory()	
    
def __checkForNextPage(sHtmlContent):
    soup = BeautifulSoup(sHtmlContent, "html.parser")
    
    try:
        PaginationSection = soup.find("div",{"class":"navigation mt20"})
        NextPage = PaginationSection.find("a",{"class":"next page-numbers"})
        VSlog('Next Page : ' + NextPage['href'])
        return NextPage['href']
    except:
        return False
    return False


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl').split('|Referer=')[0]
    Referer = oInputParameterHandler.getValue('siteUrl').split('|Referer=')[1]
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    #VSlog(sUrl)
    oRequestHandler = cRequestHandler(sUrl)
    cook = oRequestHandler.GetCookies()
    oRequestHandler.addHeaderEntry('user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('referer', Referer.encode('utf-8'))
    oRequestHandler.addHeaderEntry('cookie', cook.encode('utf-8'))
    oRequestHandler.addHeaderEntry('authority', 'nabd8lb.net'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('upgrade-insecure-requests', '1')
    oRequestHandler.addHeaderEntry('sec-fetch-dest', 'document'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('sec-fetch-mode', 'navigate'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('sec-fetch-site', 'none'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('sec-fetch-user', '?1'.encode('utf-8'))
    oRequestHandler.addHeaderEntry('sec-ch-ua-mobile', '?0'.encode('utf-8'))
    
    sHtmlContent = oRequestHandler.request()
    #VSlog(sHtmlContent)
    ## Watch Servers
    soup = BeautifulSoup(sHtmlContent, "html.parser")
    sPattern = 'vo_postID=\"(.+?)\"'
    vo_postID = re.findall(sPattern,sHtmlContent)[0]

    GridISoup = soup.find("ul",{"class":"dropdown-menu list-server-mobile"})
    if GridISoup in [None,'none','']:
        GridISoup = soup.find("ul",{"class":"tabs-server"})

    GridItems = GridISoup.findAll("li")
    FullHostersList = []
    for item in GridItems:
        #VSlog(item)
        ServerIDs = item.a['onclick'].replace('getServer2(this.id,','').replace(');','')
        sHosterID = ServerIDs.split(',')[0]
        serverId = ServerIDs.split(',')[1]
        
        url = URL_MAIN + 'wp-content/themes/vo2022/temp/ajax/iframe2.php?id=' + vo_postID + '&video=' + sHosterID + '&serverId=' + serverId
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
            sTitle = sMovieTitle
            #VSlog('sHosterUrl : ' + sHosterUrl)
            if sHosterUrl not in FullHostersList:
                if sHosterUrl:
                    FullHostersList.append(sHosterUrl)
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    
                    if oHoster:
                        oHoster.setDisplayName(sTitle)
                        oHoster.setFileName(sTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
                    else:
                       VSlog("URL ["+sHosterUrl+"] has no hoster resolver")
                       
    # ## Download Servers
    # soup = BeautifulSoup(sHtmlContent, "html.parser")
    # GridISoup = soup.find("div",{"class":"downloadsList"})
    # GridItems = GridISoup.findAll("li")
    # for item in GridItems:
        # sHosterUrl = item.a['href']
        # sTitle = sMovieTitle
        # #VSlog('sHosterUrl : ' + sHosterUrl)
        # if sHosterUrl not in FullHostersList:
            # if sHosterUrl:
                # FullHostersList.append(sHosterUrl)
                # oHoster = cHosterGui().checkHoster(sHosterUrl)
                
                # if oHoster:
                    # oHoster.setDisplayName(sTitle)
                    # oHoster.setFileName(sTitle)
                    # cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
                # else:
                   # VSlog("URL ["+sHosterUrl+"] has no hoster resolver")

    oGui.setEndOfDirectory()