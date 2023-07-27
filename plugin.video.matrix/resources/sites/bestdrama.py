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


ADDON = addon()
icons = ADDON.getSetting('defaultIcons')

SITE_IDENTIFIER = 'bestdrama'
SITE_NAME = 'Best-Drama'
SITE_DESC = 'Asian Movies and TV Shows'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

REPLAYTV_PLAY = (URL_MAIN + 'cate-serie/برامج/', 'showSeries', 'برامج تلفزيونية')
#DRAMA_CN = (URL_MAIN + 'cate-serie/%d8%af%d8%b1%d8%a7%d9%85%d8%a7-%d8%b5%d9%8a%d9%86%d9%8a%d8%a9/', 'showSeries', 'دراما صينية')
SERIE_FULL = (URL_MAIN + 'cate-serie/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa/', 'showSeries', 'مسلسلات')
SERIE_THAI = (URL_MAIN + 'cate-serie/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%aa%d8%a7%d9%8a%d9%84%d9%86%d8%af%d9%8a%d8%a9/', 'showSeries', 'مسلسلات تايلندية')
#SERIE_TR = (URL_MAIN + 'cate-serie/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%aa%d8%b1%d9%83%d9%8a%d8%a9/', 'showSeries', 'مسلسلات تركية')
SERIE_CN = (URL_MAIN + 'cate-serie/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%b5%d9%8a%d9%86%d9%8a%d8%a9/', 'showSeries', 'مسلسلات صينية')
#SERIE_AR = (URL_MAIN + 'cate-serie/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%b9%d8%b1%d8%a8%d9%8a%d8%a9/', 'showSeries', 'مسلسلات عربية')
SERIE_KR = (URL_MAIN + 'cate-serie/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d9%83%d9%88%d8%b1%d9%8a%d8%a9/', 'showSeries', 'مسلسلات كورية')
SERIE_JP = (URL_MAIN + 'cate-serie/مسلسلات-يابانية/', 'showSeries', 'مسلسلات يابانية')
#SERIE_GENRES = (True, 'showSeriesGenres', 'تصنيفات المسلسلات')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')

URL_SEARCH_SERIES = (URL_MAIN + '?s=', 'showSeries')
URL_SEARCH_MOVIES = (URL_MAIN + '?s=', 'showMovies')

FUNCTION_SEARCH = 'showSeries'

WhiteList = ('افلام','مسلسلات','برامج','اطفال','رمضان','انمي','كرتون','كارتون','دراما', 'الدراما')
def load():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', 'Search Series', icons + '/Search.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_FULL[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_FULL[1], SERIE_FULL[2], icons + '/Asian.png', oOutputParameterHandler)

    # oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    # oGui.addDir(SITE_IDENTIFIER, SERIE_AR[1], SERIE_AR[2], icons + '/Turkish.png', oOutputParameterHandler)

    # oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    # oGui.addDir(SITE_IDENTIFIER, SERIE_TR[1], SERIE_TR[2], icons + '/Turkish.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_KR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_KR[1], SERIE_KR[2], icons + '/Korean.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_CN[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_CN[1], SERIE_CN[2], icons + '/Chinese.png', oOutputParameterHandler)
    
    # oOutputParameterHandler.addParameter('siteUrl', DRAMA_CN[0])
    # oGui.addDir(SITE_IDENTIFIER, DRAMA_CN[1], DRAMA_CN[2], icons + '/Chinese.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_JP[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_JP[1], SERIE_JP[2], icons + '/Japanese.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_THAI[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_THAI[1], SERIE_THAI[2], icons + '/Thai.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_PLAY[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_PLAY[1], REPLAYTV_PLAY[2] , icons + '/Programs.png', oOutputParameterHandler)
    
    #oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    #oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], SERIE_GENRES[2] , icons + '/Genres.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()

def showSeriesGenres():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    GenreList = []
    GenreList.append([URL_MAIN + 'cate-serie/%d8%b1%d9%88%d9%85%d8%a7%d9%86%d8%b3%d9%8a/', 'showSeries', 'رومانسي'])
    GenreList.append([URL_MAIN + 'cate-serie/%d9%83%d9%88%d9%85%d9%8a%d8%af%d9%8a/', 'showSeries', 'كوميدي'])
    
        
    for item in GenreList:
        oOutputParameterHandler.addParameter('siteUrl',  item[0]) 
        oGui.addDir(SITE_IDENTIFIER, item[1] , item[2], getThumb(item[2]), oOutputParameterHandler)
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
	
def showSeries(sSearch = ''):
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
    try:
        GridSoup = soup.find("div",{"class":"row mt-3"})
        GridItems = GridSoup.findAll("div",{"class":"postmovie"})
    except:
        #GridSoup = soup.find("div",{"class":"row mb-5"})
        GridItems = soup.findAll("div",{"class":"postmovie"})
        
    oOutputParameterHandler = cOutputParameterHandler()
    for item in GridItems:

        siteUrl = item.h4.a['href']
        sTitle = item.h4.a.text.replace("فيلم","").replace('مسلسل','').replace('حلقات','').replace("مترجم ","").replace("مترجم","").replace("مدبلج ","").replace("مدبلج","").strip()
        
        try:
            sTitleEN = sTitle.split('/')[0]
            sTitleAR = sTitle.split('/')[1]
        except:
            sTitleEN = sTitle
            sTitleAR = ''
            
        sYear = item.find("div",{"class":"post-date"}).text.strip()

        try:
            sThumb = item.find("img",{"class":"lazydata"})['src']
        except:
            sThumb = ''
        sThumb = re.sub(r'-\d*x\d*.','.', sThumb)
        #VSlog(sThumb)
        if sThumb.startswith('//'):
            sThumb = 'https:' + sThumb

        sDesc = ''
        oOutputParameterHandler.addParameter('sMovieTitle', sTitleEN)
        oOutputParameterHandler.addParameter('sTitle2', sTitleAR)
        
        oOutputParameterHandler.addParameter('siteUrl',  siteUrl) 
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sYear',sYear)
        
        oGui.addTV(SITE_IDENTIFIER, 'showEpisodes' , sTitleEN, sYear, sThumb, sDesc, oOutputParameterHandler)
    
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
    
    oInputParameterHandler = cInputParameterHandler()
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sYear = oInputParameterHandler.getValue('sYear')
    
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    
    soup = BeautifulSoup(sHtmlContent, "html.parser")
    GridSoup = soup.find("div",{"class":"box-loop-episode"}).find("div",{"class":"loop-episode"})
    oOutputParameterHandler = cOutputParameterHandler()

    sDesc = soup.find("div",{"class":"info-detail-single"}).p.text.encode('utf-8')
    GridLinks = GridSoup.findAll("div",{"class":"episode_box_tabs_container"})

    for i in range(0,len(GridLinks)):
        EpTxt = GridLinks[i].find("span",{"class":"numepisode"}).text.strip().split('/')[0]
        sTitle = sMovieTitle + ' - E' + EpTxt 
        siteUrl = GridLinks[i].a['href']
 
        oOutputParameterHandler.addParameter('sTitle', sTitle )
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle )
        
        oOutputParameterHandler.addParameter('siteUrl',  siteUrl) 
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sYear',sYear)
        oOutputParameterHandler.addParameter('sDesc',sDesc)
        oOutputParameterHandler.addParameter('sSeason',1)
        oOutputParameterHandler.addParameter('sSaison',1)
        
        oGui.addEpisode(SITE_IDENTIFIER, 'showHostersE' , sTitle, sYear, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()	
    
def __checkForNextPage(sHtmlContent):
    soup = BeautifulSoup(sHtmlContent, "html.parser")
    
    try:
        PaginationSection = soup.find("div",{"class":"pagination"})
        CurrentPage = PaginationSection.find("span",{"class":"current"}).text.strip()
        VSlog('CurrentPage ' + CurrentPage)
        VSlog(PaginationSection)
        Pages = PaginationSection.findAll("a")
        for page in Pages:
            if int(page.text) - int(CurrentPage) ==1:
                VSlog('NextPage' + page['href'])
                return page['href']
    except:
        return False
    return False

def showHostersE():
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
    FullHostersList = []
    
    try:
        GridISoup = soup.find("div",{"class":"single-episode-watch-server"})   
        GridItems = GridISoup.findAll("li",{"class":"getplay"})
        for item in GridItems:
            try:
                sHosterUrl = item['data-url'].replace(",,","")
                sHost = item.text.strip()
                sTitle = sMovieTitle
                #VSlog('sHost : ' + sHost + ' sHosterUrl : ' + sHosterUrl)
                
                oRequestHandler = cRequestHandler(sHosterUrl)
                cook = oRequestHandler.GetCookies()
                oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
                oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
                oRequestHandler.addHeaderEntry('Cookie', cook.encode('utf-8'))
                oRequestHandler.addHeaderEntry('authority', 'best-drama.com')
                oRequestHandler.addHeaderEntry('cache-control', 'max-age=0')        
                sHtmlContent2 = oRequestHandler.request()
                
                sPattern = 'iframe.+?src=\"(.+?)\"'
                oParser = cParser()
                aResult = oParser.parse(sHtmlContent2.lower(), sPattern)
                VSlog(aResult)
                if aResult[0]:
                    sHosterUrl = aResult[1][0]
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
            except:
               oGui.addText('', 'Error - No Links Founds',icons + '/None.png')
    except:
        if 'قريباً' in sHtmlContent:
            oGui.addText('', 'Soon on Asia2TV - No Links Yet',icons + '/None.png')
        else:
            oGui.addText('', 'Error - No Links Founds',icons + '/None.png')
        
    oGui.setEndOfDirectory()