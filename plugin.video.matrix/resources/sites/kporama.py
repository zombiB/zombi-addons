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

SITE_IDENTIFIER = 'kporama'
SITE_NAME = 'Kporama'
SITE_DESC = 'Asian Movies and TV Shows'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_ASIAN = (URL_MAIN + 'movies/', 'showMovies')

MOVIE_KR = (URL_MAIN + 'app/category/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d8%a2%d8%b3%d9%8a%d9%88%d9%8a%d8%a91/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d9%83%d9%88%d8%b1%d9%8a%d8%a91/', 'showMovies')

MOVIE_CN = (URL_MAIN  +'app/category/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d8%a2%d8%b3%d9%8a%d9%88%d9%8a%d8%a91/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d8%b5%d9%8a%d9%86%d9%8a%d8%a91/', 'showMovies')
MOVIE_JP = (URL_MAIN  +'app/category/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d8%a2%d8%b3%d9%8a%d9%88%d9%8a%d8%a91/%d8%a3%d9%81%d9%84%d8%a7%d9%85-%d9%8a%d8%a7%d8%a8%d8%a7%d9%86%d9%8a%d8%a91/', 'showMovies')

SERIE_KR = (URL_MAIN + 'app/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%a2%d8%b3%d9%8a%d9%88%d9%8a%d8%a91/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d9%83%d9%88%d8%b1%d9%8a%d8%a91/', 'showSeries')
SERIE_CN = (URL_MAIN + 'app/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%a2%d8%b3%d9%8a%d9%88%d9%8a%d8%a91/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%b5%d9%8a%d9%86%d9%8a%d8%a91/', 'showSeries')
SERIE_JP = (URL_MAIN + 'app/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%a2%d8%b3%d9%8a%d9%88%d9%8a%d8%a91/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d9%8a%d8%a7%d8%a8%d8%a7%d9%86%d9%8a%d8%a91/', 'showSeries')
REPLAYTV_PLAY = (URL_MAIN + 'app/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%a2%d8%b3%d9%8a%d9%88%d9%8a%d8%a91/%d8%a8%d8%b1%d8%a7%d9%85%d8%ac-%d8%aa%d9%84%d9%8a%d9%81%d8%b2%d9%8a%d9%88%d9%86%d9%8a%d8%a91/', 'showSeries')

URL_SEARCH = (URL_MAIN + '/?s=', 'showSeries')
URL_SEARCH_MOVIES = (URL_MAIN + '/?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '/?s=', 'showSeriesSearch')
URL_SEARCH_MISC = (URL_MAIN + '/?s=', 'showSeriesSearch')
FUNCTION_SEARCH = 'showSeries'
WhiteList = ('افلام','مسلسلات','برامج','اطفال','رمضان','انمي','كرتون','كارتون')
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Search Movies', icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', 'Search Series', icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchAll', 'Search All', icons + '/Search.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ASIAN[1], 'أفلام آسيوية', icons + '/Asian.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_KR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_KR[1], 'أفلام كورية', icons + '/Korean.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_CN[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_CN[1], 'أفلام صينية', icons + '/Chinese.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_JP[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_JP[1], 'أفلام يابانية', icons + '/Japanese.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_KR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_KR[1], 'مسلسلات كورية', icons + '/Korean.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_CN[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_CN[1], 'مسلسلات صينية', icons + '/Chinese.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_JP[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_JP[1], 'مسلسلات يابانية', icons + '/Japanese.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_PLAY[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_PLAY[1], 'برامج ترفيهية', icons + '/Programs.png', oOutputParameterHandler)
    
    #showSiteCats()
    
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
        if mItems[1] not in [None,"", "#"]:
            if mItems[1].startswith("http"):
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
 
def showSeriesSearch():
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
        #VSlog(item)
        siteUrl = item.article.a['href'] 
        sTitle = item.article.a.h3.text.replace("مترجم","").replace("مدبلج","").replace("فيلم","").split("/")[0]
        sYear = item.article.a.span.text 
        
        try:
            sThumb = item.article.a.div.figure.img['data-lazy-src'].replace('"','')
        except:
            sThumb = item.article.a.div.figure.img['src'].replace('"','')
        #sThumb = item.article.a.div.figure.img['src'].replace('"','')
        sThumb = re.sub(r'-\d*x\d*.','.', sThumb)
        
        if sThumb.startswith('//'):
            sThumb = 'https:' + sThumb.replace('"','')
        VSlog(sThumb)
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
        sTitle = item.article.a.h3.text.replace("مترجم","").replace("مدبلج","").replace("مسلسل","").split("/")[0]
        YearPattern = '<span class=\"Year\">(\d+?)</span>'
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
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()


def showEpisodes():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    
   #VSlog(sUrl)
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
       #VSlog(row)
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
        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
        oOutputParameterHandler.addParameter('Episode', sTitle)
        oOutputParameterHandler.addParameter('Season', 1)
        oOutputParameterHandler.addParameter('siteUrl',  siteUrl) 
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sYear',sYear)
        
        oGui.addEpisode(SITE_IDENTIFIER, 'showHosters' , sMovieTitle + ' - ' + sTitle, sYear, sThumb, sDesc, oOutputParameterHandler)

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
    #sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
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
       #VSlog('sHost : ' + sHost)
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