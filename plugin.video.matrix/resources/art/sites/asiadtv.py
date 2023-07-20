# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

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

SITE_IDENTIFIER = 'asiadtv'
SITE_NAME = 'AsiaDramaTV'
SITE_DESC = 'Asian Movies and TV Shows'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

WhiteList = ('افلام','مسلسلات','برامج','اطفال','رمضان','انمي','كرتون','كارتون','دراما', 'الدراما')
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Search Movies', icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', 'Search Series', icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchAll', 'Search All', icons + '/Search.png', oOutputParameterHandler)
    
    showSiteCats()
    
    oGui.setEndOfDirectory()

def showSiteCats():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    
    oRequestHandler = cRequestHandler(URL_MAIN)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    sHtmlContent = oRequestHandler.request()
    
    soup = BeautifulSoup(sHtmlContent, "html.parser")
    MenuSoup = soup.find("div",{"class":"advancedSearch"}).div.form.find("select",{"name":"types"})
    
   #VSlog(MenuSoup)
    MenuItems = MenuSoup.findAll("option")
    
    for item in MenuItems:
        mItems=(item.text.replace("الدراما ال","مسلسلات "), URL_MAIN + 'types/' + item.text.replace(" ","-")+"/")
        oOutputParameterHandler.addParameter('siteUrl',  mItems[1]) 
        oGui.addDir(SITE_IDENTIFIER, getFunc(mItems[0]), mItems[0], getThumb(mItems[0]), oOutputParameterHandler)
    oGui.setEndOfDirectory()
 
def showSearchAll():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/?s='+sSearchText
        showSeriesSearch(sUrl)
        oGui.setEndOfDirectory()
        return  
 
def showSearch():
    oGui = cGui() 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/?s='+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSearchSeries():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/?s='+sSearchText
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
    
   #VSlog(sUrl)
    
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    
    soup = BeautifulSoup(sHtmlContent, "html.parser")
    GridSoup = soup.find("div",{"class":"secPost"})
    try:
        GridItems = GridSoup.findAll("div",{"class":"block-post2"})
    except:
        GridItems = GridSoup.findAll("div",{"class":"block-post2"})
   #VSlog(GridSoup)
    oOutputParameterHandler = cOutputParameterHandler()
    for item in GridItems:
       #VSlog(item)
        siteUrl = item.a['href']
        sTitle = item.find("div",{"class":"blockTitle"}).text.replace("مترجم ","").replace("مترجم","").replace("مدبلج ","").replace("مدبلج","").strip()
        sYear = ''
        
        try:
            sThumb = item.a.div.img['data-img'].replace('"','')
        except:
            sThumb = item.a.div.img['src'].replace('"','')
        sThumb = re.sub(r'-\d*x\d*.','.', sThumb)
        
        if sThumb.startswith('//'):
            sThumb = 'https:' + sThumb
           
        sDesc = ''
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('siteUrl',  siteUrl) 
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sYear',sYear)
        
        oGui.addMovie(SITE_IDENTIFIER, 'showHosters' , sTitle, sYear, sThumb, sDesc, oOutputParameterHandler)
    
    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
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
    GridSoup = soup.find("div",{"class":"secPost"})
    try:
        GridItems = GridSoup.findAll("div",{"class":"block-post2"})
    except:
        GridItems = GridSoup.findAll("div",{"class":"block-post2"})
   #VSlog(GridSoup)
    oOutputParameterHandler = cOutputParameterHandler()
    for item in GridItems:
       #VSlog(item)
        siteUrl = item.a['href']
        sTitle = item.find("div",{"class":"blockTitle"}).text.replace("مترجم ","").replace("مترجم","").replace("مدبلج ","").replace("تقرير","").replace("+","").replace("حلقات","").replace("الحلقات","").replace(" ة "," ").strip()
        sYear = ''
        
        try:
            sThumb = item.a.div.img['data-img'].replace('"','')
        except:
            sThumb = item.a.div.img['src'].replace('"','')
        sThumb = re.sub(r'-\d*x\d*.','.', sThumb)
        
        if sThumb.startswith('//'):
            sThumb = 'https:' + sThumb
           
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

 			
def showSeasons():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
   #VSlog(sUrl)
    oInputParameterHandler = cInputParameterHandler()
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    
    soup = BeautifulSoup(sHtmlContent, "html.parser")
    GridSoup = soup.find("div",{"class":"sec-main"}).find("ul",{"class":"list-seasons"})

    GridItems = GridSoup.findAll("li")

   #VSlog(GridSoup)
    oOutputParameterHandler = cOutputParameterHandler()
    for item in GridItems:
       #VSlog(item)
        siteUrl = item.a['href']
        sTitle = item.a.text.replace("مترجم ","").replace("مترجم","").replace("مدبلج ","").replace("مدبلج","").strip()
        sYear = ''
        sDesc = soup.find("div",{"class":"description"}).text.encode('utf-8')
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('siteUrl',  siteUrl) 
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sYear',sYear)
        oOutputParameterHandler.addParameter('sDesc',sDesc)
        oOutputParameterHandler.addParameter('sSaison',sTitle.split("الموسم")[0].strip())
        oGui.addTV(SITE_IDENTIFIER, 'showEpisodes' , sTitle, sYear, sThumb, sDesc, oOutputParameterHandler)
    
        sNextPage = __checkForNextPage(sHtmlContent)
        oOutputParameterHandler = cOutputParameterHandler()
        if sNextPage:
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeasons', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()
 
def showEpisodes():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
   #VSlog(sUrl)
    oInputParameterHandler = cInputParameterHandler()
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sSaison = oInputParameterHandler.getValue('sSaison')
    
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    
    soup = BeautifulSoup(sHtmlContent.replace("eplist2 list-eps","eplist2list-eps"), "html.parser")
    GridSoup = soup.find("div",{"class":"sec-main"}).find("ul",{"class":"eplist2list-eps"})
    Eps = GridSoup#.find_next_sibling("div")
    #VSlog(soup)
    try:
        GridItems = Eps.findAll("li")

        itemsList = []
        oOutputParameterHandler = cOutputParameterHandler()
        for item in GridItems:
            #VSlog(item)
            siteUrl = item.a['href']
            sTitle = item.a['title'].replace("الحلقة ","E").replace("الحلقة","E").replace("الحلقه ","E").replace("الحلقه","E").replace("END","").replace("والاخيرة","").replace("والأخيرة","").strip()
            sYear = ''
            sDesc = soup.find("div",{"class":"description"}).text.encode('utf-8')
            itemsList.append([sTitle,siteUrl])
        
        itemsList.sort()
        for item in itemsList:
            siteUrl = item[1]
            sTitle = item[0]
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle + ' ' +  sTitle )
            oOutputParameterHandler.addParameter('siteUrl',  siteUrl) 
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear',sYear)
            oOutputParameterHandler.addParameter('sDesc',sDesc)
            oGui.addTV(SITE_IDENTIFIER, 'showHosters' , sTitle, sYear, sThumb, sDesc, oOutputParameterHandler)
        
        sNextPage = __checkForNextPage(sHtmlContent)
        oOutputParameterHandler = cOutputParameterHandler()
        if sNextPage:
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)
    except:
        oGui.addText('', 'No Episodes Yet',icons + '/None.png')
  
    oGui.setEndOfDirectory()	
    
def __checkForNextPage(sHtmlContent):
    soup = BeautifulSoup(sHtmlContent, "html.parser")
    
    try:
        PaginationSection = soup.find("div",{"class":"navigation mt20"})
        NextPage = PaginationSection.find("a",{"class":"next page-numbers"})
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
   #VSlog(sUrl)
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    ## Watch Servers
    cook = oRequestHandler.GetCookies()
    soup = BeautifulSoup(sHtmlContent, "html.parser")
    WatchPage = soup.find("div",{"class":"poster"}).find("div",{"class":"single_buttons mt10"}).form

    FullHostersList = []
    
    url = WatchPage['action']
    inputmethod = WatchPage.input['name']
    inputvalue = WatchPage.input['value']
    
    s = requests.Session()            
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'}
    data = {inputmethod:inputvalue}
   #VSlog(data)
    r = s.post(url, headers=headers,data = data)
    sHtmlContent = r.content.decode('utf8',errors='ignore')
    soup = BeautifulSoup(sHtmlContent, "html.parser")
   #VSlog(sHtmlContent)
    GridISoup = soup.find("ul",{"class":"ServerNames"})
    GridItems = GridISoup.findAll("li")
    for item in GridItems:
       #VSlog(item)
        sHosterFrame = item['data-server']
       #VSlog(sHosterFrame)
        sPattern = 'iframe src=\"(.+?)\"'
        oParser = cParser()
        aResult = oParser.parse(sHosterFrame.lower(), sPattern)
        if aResult[0]:
            sHosterUrl = aResult[1][0].replace("&quot;","")
            sHost = item.i.text.strip()
            sTitle = sMovieTitle
           #VSlog('sHost : ' + sHost + ' sHosterUrl : ' + sHosterUrl)
            if 'asiatvplayer' in sHosterUrl:
                sHosterUrl = sHosterUrl + '|Referer=' + url
            if sHosterUrl not in FullHostersList:
                if sHosterUrl:
                    FullHostersList.append(sHosterUrl)
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    
                    if oHoster:
                        oHoster.setDisplayName(sTitle)
                        oHoster.setFileName(sHost)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
                    else:
                       VSlog("URL ["+sHosterUrl+"] has no hoster resolver")

    oGui.setEndOfDirectory()