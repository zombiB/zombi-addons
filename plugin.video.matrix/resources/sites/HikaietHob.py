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

SITE_IDENTIFIER = 'HikaietHob'
SITE_NAME = '7ikaiet 7ob'
SITE_DESC = 'Turkish TV Shows'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

SERIE_TR = (URL_MAIN + 'all-series1/', 'showSeries')

URL_SEARCH = (URL_MAIN + '/?s=', 'showSeries')
FUNCTION_SEARCH = 'showSeries'
sitemsList = []
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', 'Search Series', icons + '/Search.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_TR[1], 'مسلسلات تركية', icons + '/Turkish.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

 
def showSearchSeries():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/?s='+sSearchText
        showSeriesSearch(sUrl)
        oGui.setEndOfDirectory()
        return  
		
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

    GridItems = GridSoup.findAll("div",{"class":"block-post"})
   #VSlog(GridSoup)
    oOutputParameterHandler = cOutputParameterHandler()
    for item in GridItems:
       #VSlog(item)
        siteUrl = item.a['href']
        sTitle = item.find("div",{"class":"title"}).text.replace("مترجم ","").replace("مترجم","").replace("مدبلج ","").replace("تقرير","").replace("+","").replace("حلقات","").replace("الحلقات","").replace(" ة "," ").split("/")[0].strip()
        sYear = ''
        #VSlog(sTitle)

        sThumb = item.a.div.div['style'].replace('background-image:url(','').replace(");","")

        #VSlog(siteUrl)
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
    
    #VSlog(sUrl)
    oInputParameterHandler = cInputParameterHandler()
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
    oRequestHandler.addHeaderEntry('Referer', SERIE_TR[0])
    sHtmlContent = oRequestHandler.request()
        
    soup = BeautifulSoup(sHtmlContent, "html.parser")
    
    try:
        try:
            GridSoup = soup.find("div",{"class":"secTitle"}).find("ul",{"class":"listSeasons2"})
        except:
            GridSoup = soup.find("div",{"class":"the_content"}).find("ul",{"class":"listSeasons"})

        GridItems = GridSoup.findAll("li")
        try:
            sDesc = soup.find("div",{"class":"story"}).text
        except:
            sDesc = ''
       #VSlog(GridSoup)
        oOutputParameterHandler = cOutputParameterHandler()
        for item in GridItems:
           #VSlog(item)
            seriesID = item['data-season']
            siteUrl = URL_MAIN + '/wp-content/themes/7ob2022/temp/ajax/seasons2.php?seriesID=' + seriesID + '|Referer=' + sUrl
            sTitle = item.text.replace("مترجم ","").replace("مترجم","").replace("مدبلج ","").replace("مدبلج","").replace('الموسم ','S').strip()
            sYear = ''
            
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('siteUrl',  siteUrl) 
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear',sYear)
            oOutputParameterHandler.addParameter('sDesc',sDesc)
            
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes' , sTitle, sYear, sThumb, sDesc, oOutputParameterHandler)
        
        oGui.setEndOfDirectory()
    except:
        oOutputParameterHandler = cOutputParameterHandler()
        sTitle = sMovieTitle + ' S 1'
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
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
    oRequestHandler.addHeaderEntry('Referer', Referer)
    oRequestHandler.addHeaderEntry('Cookie', cook.encode('utf-8'))
    oRequestHandler.addHeaderEntry('authority', '7obtv.top')
    oRequestHandler.addHeaderEntry('x-requested-with', 'XMLHttpRequest')
    
    sHtmlContent = oRequestHandler.request()
    
    soup = BeautifulSoup(sHtmlContent, "html.parser")
    
    GridItems = soup.findAll("div",{"class":"block-post"})
    itemsList = []
    oOutputParameterHandler = cOutputParameterHandler()
    for item in GridItems:
        #VSlog(item)
        siteUrl = item.a['href'] + '?do=views'
        #VSlog(siteUrl)
        
        EpNum = str(item.a.find("div",{"class":"episodeNum"}).contents[3]).replace("<span>","").replace("</span>","").strip()

        sTitle = item.a['title'].strip() + ' E' + EpNum
        try:
            sThumb = item.a.find("div",{"class":"imgSer"})['style'].replace('background-image:url(','').replace(");","")
        except:
            sThumb = item.a.find("div",{"class":"imgBg"})['style'].replace('background-image:url(','').replace(");","")
        #VSlog(sTitle)
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
    # except:
        # oGui.addText('', 'No Episodes Yet',icons + '/None.png')
  
    oGui.setEndOfDirectory()	

def showSeriesSearch(sSearch=''):
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
        sTitle = item.a['title'].strip()
        if sTitle not in sitemsList:
            sitemsList.append(sTitle)
            siteUrl = item.a['href'] 
            if 'php' in siteUrl:
                siteUrl = siteUrl.replace('https://www.zinaclub.com/7obco.php?postUrl=','') + '?do=views' + '|Referer=' + sUrl
            #VSlog(siteUrl)
            
            EpNum = str(item.a.find("div",{"class":"episodeNum"}).contents[3]).replace("<span>","").replace("</span>","").strip()
            #VSlog(EpNum)
            try:
                sThumb = item.a.find("div",{"class":"imgSer"})['style'].replace('background-image:url(','').replace(");","")
            except:
                sThumb = item.a.find("div",{"class":"imgBg"})['style'].replace('background-image:url(','').replace(");","")
            #VSlog(sTitle)
            sYear = ''
            
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('siteUrl',  siteUrl) 
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear',sYear)
            oOutputParameterHandler.addParameter('sDesc',sDesc)
            oGui.addTV(SITE_IDENTIFIER, 'showSeasons' , sTitle , sYear, sThumb, sDesc, oOutputParameterHandler)
    
            sNextPage = __checkForNextPage(sHtmlContent)
            oOutputParameterHandler = cOutputParameterHandler()
            if sNextPage:
                showSeriesSearch(sNextPage)
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
    #oRequestHandler.addHeaderEntry('Referer', Referer)
    oRequestHandler.addHeaderEntry('Cookie', cook.encode('utf-8'))
    #oRequestHandler.addHeaderEntry('authority', '7obtv.top')
    #oRequestHandler.addHeaderEntry('x-requested-with', 'XMLHttpRequest')
    sHtmlContent = oRequestHandler.request()
    
    ## Watch Servers
    soup = BeautifulSoup(sHtmlContent, "html.parser")
    sPattern = 'vo_postID = \"(.+?)\"'
    vo_postID = re.findall(sPattern,sHtmlContent)[0]

    GridISoup = soup.find("ul",{"class":"serversList"})

    GridItems = GridISoup.findAll("li")
    FullHostersList = []
    for item in GridItems:
        sHosterID = item['id'].replace('s_','')
        url = URL_MAIN + 'wp-content/themes/7ob2022/temp/ajax/iframe2.php?id=' + vo_postID + '&video=' + sHosterID
        oRequestHandler = cRequestHandler(url)
        cook = oRequestHandler.GetCookies()
        oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
        oRequestHandler.addHeaderEntry('Referer', sUrl.split('|Referer=')[0])
        oRequestHandler.addHeaderEntry('Cookie', cook.encode('utf-8'))
        oRequestHandler.addHeaderEntry('authority', '7obtv.top')
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
                       
    ## Download Servers
    soup = BeautifulSoup(sHtmlContent, "html.parser")
    GridISoup = soup.find("div",{"class":"downloadsList"})
    GridItems = GridISoup.findAll("li")
    for item in GridItems:
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