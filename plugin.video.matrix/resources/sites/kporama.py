# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog, siteManager, dialog, addon
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

SITE_IDENTIFIER = 'kporama'
SITE_NAME = 'Kporama'
SITE_DESC = 'Asian Movies and TV Shows'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

URL_SEARCH = (URL_MAIN + '/search?q=', 'showSeries')
URL_SEARCH_MOVIES = (URL_MAIN + '/search?q=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '/search?q=', 'showSeriesSearch')
URL_SEARCH_MISC = (URL_MAIN + '/search?q=', 'showSeriesSearch')
FUNCTION_SEARCH = 'showSeries'
WhiteList = ('افلام','مسلسلات','برامج','اطفال','رمضان','انمي','كرتون','كارتون')
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
    MenuSoup = soup.find("nav",{"class":"Menu"}).ul
    MenuItems = MenuSoup.findAll("li")
    
    for item in MenuItems:
        mItems=(item.a.text,item.a['href'])
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
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  
		
def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch+'&section=series&year=0&rating=0&formats=0&quality=0'
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        
    
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    
    soup = BeautifulSoup(sHtmlContent, "html.parser")
    GridSoup = soup.find("ul",{"class":"MovieList"})
    GridItems = GridSoup.findAll("li")
    
    oOutputParameterHandler = cOutputParameterHandler()
    for item in GridItems:
        #VSlog(item)
        siteUrl = item.article.a['href']
        sTitle = item.article.a.h3.text
        sYear = item.article.a.span.text 
        
        try:
            sThumb = item.article.a.div.figure.img['data-lazy-src'].replace('"','')
        except:
            sThumb = item.article.a.div.figure.img['src'].replace('"','')
        sThumb = re.sub(r'-\d*x\d*.','.', sThumb)
        
        if sThumb.startswith('//'):
            sThumb = 'https:' + item.article.a.div.figure.img['data-lazy-src'].replace('"','')
           
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
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', icons + '/next.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()

def showSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
            
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    
    soup = BeautifulSoup(sHtmlContent, "html.parser")
    GridSoup = soup.find("ul",{"class":"MovieList"})
    GridItems = GridSoup.findAll("li")
    
    oOutputParameterHandler = cOutputParameterHandler()
    for item in GridItems:
        siteUrl = item.article.a['href']
        sTitle = item.article.a.h3.text
        sYear = ''
        
        try:
            sThumb = item.article.a.div.figure.img['data-lazy-src'].replace('"','')
        except:
            sThumb = item.article.a.div.figure.img['src'].replace('"','')
        sThumb = re.sub(r'-\d*x\d*.','.', sThumb)
        
        if sThumb.startswith('//'):
            sThumb = 'https:' + sThumb
           
        sDesc = ''
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('siteUrl',  siteUrl) 
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sYear',sYear)
        
        oGui.addTV(SITE_IDENTIFIER, 'showEpisodes' , sTitle, sYear, sThumb, sDesc, oOutputParameterHandler)
    
    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        oOutputParameterHandler = cOutputParameterHandler()
        if sNextPage:
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', icons + '/next.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()

 			
def showSeasons():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sSearchText = oInputParameterHandler.getValue('sMovieTitle').split("/")[0].split("الموسم")[0]
    VSlog(sSearchText)
    if sSearchText:
        sUrl = URL_MAIN + '/?s='+sSearchText
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        
    VSlog(sUrl)
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    
    soup = BeautifulSoup(sHtmlContent, "html.parser")
    GridSoup = soup.find("ul",{"class":"MovieList"})
    GridItems = GridSoup.findAll("li")
    
    oOutputParameterHandler = cOutputParameterHandler()
    for item in GridItems:
        siteUrl = item.article.a['href']
        sTitle = 'Season ' + item.article.a.h3.text.split("الموسم")[1].replace("الاول","1").replace("الأول","1").replace("الثاني","2").replace("الثالث","3").replace("الرابع","4").replace("الخامس","5").replace("السادس","6").replace("السابع","7").replace("الثامن","8").replace("التاسع","9").replace("العاشر","10").replace("الحادي عشر","11").replace("الثاني عشر","12").replace("الثالث عشر","13").replace("الرابع عشر","14").replace("الخامس عشر","15").replace("السادس عشر","16").replace("السابع عشر","17")
        sYear = ''
        
        try:
            sThumb = item.article.a.div.figure.img['data-lazy-src'].replace('"','')
        except:
            sThumb = item.article.a.div.figure.img['src'].replace('"','')
        sThumb = re.sub(r'-\d*x\d*.','.', sThumb)
        
        if sThumb.startswith('//'):
            sThumb = 'https:' + sThumb
           
        sDesc = ''
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('siteUrl',  siteUrl) 
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sYear',sYear)
        
        oGui.addTV(SITE_IDENTIFIER, 'showSeasons' , sTitle, sYear, sThumb, sDesc, oOutputParameterHandler)
    
    if sUrl:
        sNextPage = __checkForNextPage(sHtmlContent)
        oOutputParameterHandler = cOutputParameterHandler()
        if sNextPage:
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', icons + '/next.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()
 
def showEpisodes():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    VSlog(sUrl)
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    soup = BeautifulSoup(sHtmlContent, "html.parser")
    SeasonTitle = 'Season' + soup.find("div",{"class":"Wdgt AABox"}).find("div",{"class":"Title AA-Season On"}).span.text
    sDesc = soup.find("article",{"class":"TPost Single"}).find("div",{"class":"Description"}).p.text
    GridSoup = soup.find("div",{"class":"Wdgt AABox"}).find("div",{"class":"TPTblCn AA-cont"}).table.tbody
    GridItems = GridSoup.findAll("tr")
    
    oOutputParameterHandler = cOutputParameterHandler()
    for item in GridItems:
        
        row = item.find("td", {"class":"MvTbTtl"})
        VSlog(row)
        siteUrl = row.a['href']
        sTitle = row.a.text.replace("الحلقة","E").replace("الحلقه","E")
        sYear = ''
        
        try:
            sThumb = item.find("a",{"class":"MvTbImg"}).img['data-lazy-src']
        except:
            sThumb = item.find("a",{"class":"MvTbImg"}).img['src']
            
        sThumb = re.sub(r'-\d*x\d*.','.', sThumb)
        
        if sThumb.startswith('//'):
            sThumb = 'https:' + sThumb
           
        #sDesc = ''
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('siteUrl',  siteUrl) 
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sYear',sYear)
        
        oGui.addEpisode(SITE_IDENTIFIER, 'showHosters' , sTitle, sYear, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()
	
def __checkForNextPage(sHtmlContent):
    soup = BeautifulSoup(sHtmlContent, "html.parser")
    
    try:
        PaginationSection = soup.find("div",{"class":"wp-pagenavi"})
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
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    ## Watch Servers
    cook = oRequestHandler.GetCookies()
    soup = BeautifulSoup(sHtmlContent, "html.parser")
    GridSoupLabels = soup.find("ul",{"class":"TPlayerNv"})
    GridSoupLinks = GridSoupLabels.findNextSibling("div")
    FullHostersList = []
    GridItems = GridSoupLabels.findAll("li")
    GridLinks = GridSoupLinks.findAll("div", {"class":"TPlayerTb"})
    for item in GridItems:
        for Link in GridLinks:
            if Link['id'] == item['data-tplayernv']:
                sHosterUrl = Link.div.form.input['value']
                sHost = item.span.text.replace("🌟","").strip()
                sTitle = item.span.findNextSibling("span").text.replace('مترجم','').replace('-','').strip()
                if '720p' or '1080p' or '480p' or '360p' or '240p' or '4k' or '2160p' in sTitle:
                    sThumb = icons + '/resolution/' + sTitle.replace("HD","").replace("SD","").replace("(","").replace(")","").strip() + '.png'
                
                oRequestHandler = cRequestHandler(sHosterUrl)
                oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'.encode('utf-8'))
                oRequestHandler.addHeaderEntry('Referer', sUrl.encode('utf-8'))
                oRequestHandler.addHeaderEntry('Cookie', cook.encode('utf-8'))
                oRequestHandler.addHeaderEntry('authority', 'post.keeparab.com'.encode('utf-8'))
                oRequestHandler.addHeaderEntry('upgrade-insecure-requests', '1'.encode('utf-8'))

                sHtmlContent2 = oRequestHandler.request()
                sHtmlContent2 = sHtmlContent2.encode("utf-8",errors='ignore').decode("unicode_escape")
                
                soup = BeautifulSoup(sHtmlContent2, "html.parser")
                HostLink = soup.find("div",{"class":"Video"}).iframe['src']
                
                sHosterUrl = HostLink
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
    ## Download Servers
    soup = BeautifulSoup(sHtmlContent, "html.parser")
    DownloadLinksSoup = soup.find("div",{"class":"TPTblCn"}).table.tbody
    
    DownloadLinksRows = DownloadLinksSoup.findAll("tr")
    
    for row in DownloadLinksRows:
        #VSlog(row)
        Columns = row.findAll("td")
        #VSlog(Columns)
        sHost = Columns[2].span.text.replace("🌟","").strip()
        VSlog('sHost : ' + sHost)
        sHosterUrl = Columns[1].a['href']
        sTitle = Columns[3].span.text.replace("HD","").replace("SD","").replace("(","").replace(")","").strip()
        
        if '720p' or '1080p' or '480p' or '360p' or '240p' or '4k' or '2160p' in sTitle:
            sThumb = icons + '/resolution/' + sTitle + '.png'
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
