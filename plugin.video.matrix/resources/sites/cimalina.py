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


ADDON = addon()
icons = ADDON.getSetting('defaultIcons')

SITE_IDENTIFIER = 'cimalina'
SITE_NAME = 'CimaLina'
SITE_DESC = 'Movies & TV Shows'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

CatsList = []
MOVIE_EN = (URL_MAIN + 'category/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d8%a3%d8%ac%d9%86%d8%a8%d9%8a%d8%a9/', 'showMovies', 'افلام اجنبية')
CatsList.append(MOVIE_EN)
MOVIE_HI = (URL_MAIN + 'category/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d9%87%d9%86%d8%af%d9%8a%d8%a9/', 'showMovies', 'افلام هندية')
CatsList.append(MOVIE_HI)
MOVIE_ASIAN = (URL_MAIN + 'category/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d8%a7%d8%b3%d9%8a%d9%88%d9%8a%d8%a9/', 'showMovies', 'افلام آسيوية')
CatsList.append(MOVIE_ASIAN)
MOVIE_TR = (URL_MAIN + 'category/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d8%aa%d8%b1%d9%83%d9%8a%d8%a9/', 'showMovies', 'افلام تركية')
CatsList.append(MOVIE_TR)
KIDS_MOVIE = (URL_MAIN + 'category/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d8%a3%d9%86%d9%85%d9%8a/', 'showMovies', 'افلام اطفال')
CatsList.append(KIDS_MOVIE)
MOVIE_PACK = (URL_MAIN + '/assemblies/', 'showMovies', 'سلاسل الافلام')
CatsList.append(MOVIE_PACK)

SERIE_TR = (URL_MAIN + 'category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%aa%d8%b1%d9%83%d9%8a%d8%a9-%d9%85%d8%aa%d8%b1%d8%ac%d9%85%d8%a9/', 'showSeries', 'مسلسلات تركية')
CatsList.append(SERIE_TR)
SERIE_TR_AR = (URL_MAIN + 'category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%aa%d8%b1%d9%83%d9%8a%d8%a9-%d9%85%d8%af%d8%a8%d9%84%d8%ac%d8%a9/', 'showSeries', 'مسلسلات تركية مدبلجة')
CatsList.append(SERIE_TR_AR)
SERIE_KR = (URL_MAIN + 'category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d9%83%d9%88%d8%b1%d9%8a%d8%a9/', 'showSeries', 'مسلسلات كورية')
CatsList.append(SERIE_KR)
SERIE_EN = (URL_MAIN + 'category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%a3%d8%ac%d9%86%d8%a8%d9%8a%d8%a9/', 'showSeries', 'مسلسلات اجنبية')
CatsList.append(SERIE_EN)
SERIE_ASIAN = (URL_MAIN + 'category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%a7%d8%b3%d9%8a%d9%88%d9%8a%d8%a9/', 'showSeries', 'مسلسلات آسيوية')
CatsList.append(SERIE_ASIAN)
KIDS_SERIE = (URL_MAIN + 'category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%a3%d9%86%d9%85%d9%8a/', 'showSeries', 'مسلسلات اطفال')
CatsList.append(KIDS_SERIE)

URL_SEARCH = (URL_MAIN + '/?s=', 'showSeries')
FUNCTION_SEARCH = 'showSeries'
sitemsList = []
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchMovies', 'Search Movies', icons + '/Search.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', 'Search Series', icons + '/Search.png', oOutputParameterHandler)
    
    for Cat in CatsList:
        oOutputParameterHandler.addParameter('siteUrl', Cat[0])
        oGui.addDir(SITE_IDENTIFIER, Cat[1], Cat[2], getThumb(Cat[2]), oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearchSeries():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sitemsList = []
        sUrl = URL_MAIN + '/?s='+sSearchText
        showSeriesSearch(sUrl,'TVShows')
        oGui.setEndOfDirectory()
        return  
        
def showSearchMovies():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sitemsList = []
        sUrl = URL_MAIN + '/?s='+sSearchText
        showSeriesSearch(sUrl,'Movies')
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
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    
    soup = BeautifulSoup(sHtmlContent, "html.parser")
    GridSoup = soup.find("div",{"class":"moviesBlocks"})

    GridItems = GridSoup.findAll("div",{"class":"movie"})
    #VSlog(GridSoup)
    oOutputParameterHandler = cOutputParameterHandler()
    for item in GridItems:
       #VSlog(item)
        siteUrl = item.a['href']
        sTitle = item.a.find("div",{"class":"dicr"}).h3.text.replace("مترجم ","").replace("مترجم","").replace("مدبلج ","").replace("تقرير","").replace("+","").replace("فيلم","").replace("فلم","").replace("مشاهدة"," ").strip()
        sYear = ''
        sThumb = item.a.find("img")['src']
        if sThumb.startswith('//'):
            sThumb = 'https:' + sThumb
           
        sDesc = ''
        
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('siteUrl',  siteUrl) 
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sYear',sYear)
        
        oGui.addMovie(SITE_IDENTIFIER, 'showHosters' , sTitle, sYear, sThumb, sDesc, oOutputParameterHandler)
    
    if not sSearch:
        sNextPage = __checkForNextPageM(sHtmlContent)
        oOutputParameterHandler = cOutputParameterHandler()
        if sNextPage:
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)
        oGui.setEndOfDirectory()

def showSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
    
    #VSlog(sUrl)
    
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    
    soup = BeautifulSoup(sHtmlContent, "html.parser")
    GridSoup = soup.find("div",{"class":"moviesBlocks"})

    GridItems = GridSoup.findAll("div",{"class":"movie"})
    #VSlog(GridSoup)
    oOutputParameterHandler = cOutputParameterHandler()
    for item in GridItems:
       #VSlog(item)
        siteUrl = item.a['href'] + '/page/1/'
        sTitle = item.a.find("div",{"class":"dicr"}).h3.text.replace("مترجم ","").replace("مترجم","").replace("مدبلج ","").replace("تقرير","").replace("+","").replace("فيلم","").replace("فلم","").replace("مشاهدة"," ").replace("الجزء","الموسم").split("الموسم")[0].strip()
        sYear = ''
        sThumb = item.a.div.img['src']
        if sThumb.startswith('//'):
            sThumb = 'https:' + sThumb
           
        sDesc = ''
        
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('siteUrl',  siteUrl) 
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sYear',sYear)
        
        oGui.addTV(SITE_IDENTIFIER, 'showSeasons' , sTitle, sYear, sThumb, sDesc, oOutputParameterHandler)
    
    if not sSearch:
        sNextPage = __checkForNextPageS(sHtmlContent)
        oOutputParameterHandler = cOutputParameterHandler()
        if sNextPage:
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)
        oGui.setEndOfDirectory()


def showSeriesSearch(sSearch = '', stype= ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
    
    #VSlog(sUrl)
    
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    

    
    soup = BeautifulSoup(sHtmlContent, "html.parser")
    GridSoup = soup.find("div",{"class":"moviesBlocks"})
    GridItems = GridSoup.findAll("div",{"class":"movie"})
    
    total = len(GridItems)
    progress_ = progress().VScreate(SITE_NAME)
    
    oOutputParameterHandler = cOutputParameterHandler()
    
    for item in GridItems:
        progress_.VSupdate(progress_, total)
        if progress_.iscanceled():
            break
        siteUrl = item.a['href'] + '/page/1/'
        sTitle = item.a.find("div",{"class":"dicr"}).h3.text.replace("مترجم ","").replace("مترجم","").replace("مدبلج ","").replace("تقرير","").replace("+","").replace("فيلم","").replace("فلم","").replace("مشاهدة"," ").replace("الجزء","الموسم").split("الحلقة")[0].strip()
        if sTitle not in sitemsList:
            sitemsList.append(sTitle)
            sYear = ''
            sThumb = item.a.div.img['src']
            if sThumb.startswith('//'):
                sThumb = 'https:' + sThumb
               
            sDesc = ''
            
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('siteUrl',  siteUrl) 
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear',sYear)
            
            if stype == 'TVShows':
                oGui.addTV(SITE_IDENTIFIER, 'showSeasons' , sTitle, sYear, sThumb, sDesc, oOutputParameterHandler)
            if stype == 'Movies':
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters' , sTitle, sYear, sThumb, sDesc, oOutputParameterHandler)
                
    progress_.VSclose(progress_)
    sNextPage = __checkForNextPageM(sHtmlContent)
    oOutputParameterHandler = cOutputParameterHandler()
    if sNextPage:
        showSeriesSearch(sSearch = sNextPage, stype = stype)
            
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
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
    oRequestHandler.addHeaderEntry('Referer', Referer.encode('utf-8'))
    oRequestHandler.addHeaderEntry('Cookie', cook.encode('utf-8'))
    oRequestHandler.addHeaderEntry('authority', 'cimalina.cam')
    oRequestHandler.addHeaderEntry('upgrade-insecure-requests', '1')
    
    sHtmlContent = oRequestHandler.request()
    HTMLList = []
    HTMLList.append(sHtmlContent)
    
    soup = BeautifulSoup(sHtmlContent, "html.parser")
    Pages = soup.find("div",{"class":"pagination"}).findAll("li")
    CurrentPage = sUrl.split('/page/')[1].replace('/','')
    if Pages not in [None,'']:
        for page in Pages:
            #VSlog(page.text)
            if page.text not in ['1', 'الصفحة التالية «','«','الصفحة التالية']:
                url = page.a['href']
                #VSlog(url)
                oRequestHandler = cRequestHandler(url)
                cook = oRequestHandler.GetCookies()
                oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
                oRequestHandler.addHeaderEntry('Referer', Referer.encode('utf-8'))
                oRequestHandler.addHeaderEntry('Cookie', cook.encode('utf-8'))
                oRequestHandler.addHeaderEntry('authority', 'cimalina.cam')
                oRequestHandler.addHeaderEntry('upgrade-insecure-requests', '1')
                sHtmlContent = oRequestHandler.request()
                HTMLList.append(sHtmlContent)
    
    for sHtmlContent in HTMLList:
        soup = BeautifulSoup(sHtmlContent, "html.parser")
        GridItems = soup.findAll("div",{"class":"movie"})
        
        oOutputParameterHandler = cOutputParameterHandler()
        for item in GridItems:
            #VSlog(item)
            siteUrl = item.a['href']
            #VSlog(siteUrl)
            EpNum = item.a.find("div",{"class":"dicr"}).h3.text.replace("مترجمة","").replace("مترجم","").replace("مدبلجة","").replace("مدبلج","").replace("فيلم","").replace("فلم","").replace("والأخيرة"," ").replace("مشاهدة"," ").split("الحلقة")[1].strip()
            sTitle = sMovieTitle.strip() + ' E' + EpNum
            sThumb = item.a.div.img['src']
            #VSlog(EpNum)
            sYear = ''
            
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('siteUrl',  siteUrl) 
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear',sYear)
            oOutputParameterHandler.addParameter('sDesc',sDesc)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters' , sTitle , sYear, sThumb, sDesc, oOutputParameterHandler)
  
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
    
    oInputParameterHandler = cInputParameterHandler()
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sDesc = oInputParameterHandler.getValue('sDesc')
        
    oRequestHandler = cRequestHandler(sUrl)
    cook = oRequestHandler.GetCookies()
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
    oRequestHandler.addHeaderEntry('Referer', Referer.encode('utf-8'))
    oRequestHandler.addHeaderEntry('Cookie', cook.encode('utf-8'))
    oRequestHandler.addHeaderEntry('authority', 'cimalina.cam')
    oRequestHandler.addHeaderEntry('upgrade-insecure-requests', '1')
    
    sHtmlContent = oRequestHandler.request()
    soup = BeautifulSoup(sHtmlContent, "html.parser")
    GridItems = soup.findAll("div",{"class":"movie"})
    
    oOutputParameterHandler = cOutputParameterHandler()
    itemsList = []
    for item in GridItems:
        #VSlog(item)
        siteUrl = sUrl
        #VSlog(siteUrl)
        SNum = item.a.find("div",{"class":"dicr"}).h3.text.replace("مترجمة","").replace("مترجم","").replace("مدبلجة","").replace("مدبلج","").replace("فيلم","").replace("فلم","").replace("والأخيرة"," ").replace("مشاهدة"," ")
        SNum = SNum.split("الحلقة")[0].strip()
        SNum = SNum.replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم السابع والعشرون","S27").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الثالث و الثلاثون","S33").replace("الموسم الأول","S1").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("S ","S")
        
        if SNum not in itemsList:
            itemsList.append(SNum)
            sTitle = SNum
            sThumb = item.a.div.img['src']
            #VSlog(SNum)
            sYear = ''
            
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('siteUrl',  siteUrl) 
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear',sYear)
            oOutputParameterHandler.addParameter('sDesc',sDesc)
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes' , sTitle , sYear, sThumb, sDesc, oOutputParameterHandler)
  
    oGui.setEndOfDirectory()	
    
def __checkForNextPageM(sHtmlContent):
    soup = BeautifulSoup(sHtmlContent, "html.parser")
    
    try:
        PaginationSection = soup.find("div",{"class":"navigation"})
        Current = PaginationSection.find("li",{"class":"active"}).a.text.strip()
        #VSlog('Current Page : ' + Current)
        
        NextPages = PaginationSection.findAll("li")

        for page in NextPages:
            #VSlog('page : ' + str(page.a.text))
            try:
                if page.a.text:
                    if int(page.a.text) - int(Current) ==1: 
                        #VSlog('Next Page : ' + page.a['href'])
                        return page.a['href']
            except:
                continue
    except:
        return False

def __checkForNextPageS(sHtmlContent):
    soup = BeautifulSoup(sHtmlContent, "html.parser")
    
    try:
        PaginationSection = soup.find("div",{"class":"pagination"})
        NextPage = PaginationSection.find("a",{"class":"next page-numbers"})
        #VSlog('Next Page : ' + NextPage['href'])
        return NextPage['href']
    except:
        return False
    return False
    
def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    cook = oRequestHandler.GetCookies()
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
    oRequestHandler.addHeaderEntry('Cookie', cook.encode('utf-8'))
    sHtmlContent = oRequestHandler.request()
    cook = oRequestHandler.GetCookies()
    
    ## Go to watchlist -----------------------------------------------
    soup = BeautifulSoup(sHtmlContent, "html.parser")
    details = soup.find("form",{"class":"formWatch"})
    ActionURL = details['action']
    ServersID = details.find("input",{"name":"servers"})['value']
    DownloadsID = details.find("input",{"name":"downloads"})['value']
    
    headers = {'authority': 'a6.foxcima.me',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'referer': URL_MAIN,
                'origin': URL_MAIN,
                'cookie': cook,
                'upgrade-insecure-requests': '1'}
    data = {'servers':ServersID,'downloads':DownloadsID,'submit':''}
   
    s = requests.Session()
    r = s.post(ActionURL, headers=headers, data=data )
    sHtmlContent = r.content.decode('utf8')         
               
    ## Watch Servers -----------------------------------------------
    soup = BeautifulSoup(sHtmlContent, "html.parser")  

    GridISoup = soup.find("ul",{"class":"serversList"})

    GridItems = GridISoup.findAll("li")
    FullHostersList = []
    for item in GridItems:  
        
        sPattern = "iframe.+?src=\'(.+?)\'"
        oParser = cParser()
        aResult = oParser.parse(str(item).lower(), sPattern)
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
                          
    ## Download Servers -----------------------------------------------
    soup = BeautifulSoup(sHtmlContent, "html.parser")
    GridISoup = soup.find("div",{"class":"downloadsList"})
    GridItems = GridISoup.findAll("li")
    for item in GridItems:
        VSlog(item)
        sHosterUrl = item.a['href']
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

    oGui.setEndOfDirectory()