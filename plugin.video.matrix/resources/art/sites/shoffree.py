# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser
from resources.lib.util import Quote
from resources.lib.Styling import getGenreIcon

from bs4 import BeautifulSoup
import requests

ADDON = addon()
icons = ADDON.getSetting('defaultIcons')

SITE_IDENTIFIER = 'shoffree'
SITE_NAME = 'Shoffree'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

oParser = cParser()
 
oRequestHandler = cRequestHandler(URL_MAIN)
sHtmlContent = oRequestHandler.request()
    # (.+?) ([^<]+)

sPattern = '<meta property="og:url" content="(.+?)" />'
aResult = oParser.parse(sHtmlContent, sPattern)
    
if (aResult[0]):
    URL_MAIN = aResult[1][0]
    VSlog(URL_MAIN)

MOVIE_EN = (URL_MAIN + '/movies', 'showMovies')
SERIE_EN = (URL_MAIN + '/series', 'showSeries')

ANIM_NEWS = (URL_MAIN + '/anime', 'showSeries')

URL_SEARCH_MOVIES = (URL_MAIN + '/search?query=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '/search?query=', 'showSeries')
FUNCTION_SEARCH = 'showMovies'

s = requests.Session()
        
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'SEARCH_MOVIES', icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', 'SEARCH_SERIES', icons + '/Search.png', oOutputParameterHandler)
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'جميع الافلام', icons + '/MoviesEnglish.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', True)
    oGui.addDir(SITE_IDENTIFIER, 'showGenresM', 'افلام حسب النوع', icons + '/Genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', True)
    oGui.addDir(SITE_IDENTIFIER, 'showLangsM', 'افلام حسب اللغة', icons + '/Movies.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'جميع المسلسلات', icons + '/TVShowsEnglish.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', True)
    oGui.addDir(SITE_IDENTIFIER, 'showGenresS', 'مسلسلات حسب النوع', icons + '/Genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', True)
    oGui.addDir(SITE_IDENTIFIER, 'showLangsS', 'مسلسلات حسب اللغة', icons + '/Genres.png', oOutputParameterHandler)
	
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات إنمي', icons + '/Anime.png', oOutputParameterHandler)  

    oGui.setEndOfDirectory()

def showLangsM():
    oGui = cGui()
    sPattern = '<option value=\".*\">(.+?)</option'
    
    sUrl = MOVIE_EN[0]
    r = s.get(sUrl)
    soup = BeautifulSoup(r.content,"html.parser") 
    sHtmlContent = str(soup.find("select",{"name":"lang"}))
    
    matches = re.findall(sPattern, sHtmlContent)
    aResult = [True,matches]
    
    #VSlog(aResult)
    
    if aResult[0] is True:
        for aEntry in aResult[1]:
            CatURL = MOVIE_EN[0] + '?lang=' + aEntry
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', CatURL)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', aEntry, icons + '/Language.png', oOutputParameterHandler)
        oGui.setEndOfDirectory()
    else:
        pass

def showGenresM():
    oGui = cGui()   
    sPattern = '<option value=\".+?\">(.+?)</option'
    
    sUrl = MOVIE_EN[0]
    r = s.get(sUrl)
    soup = BeautifulSoup(r.content,"html.parser") 
    sHtmlContent = str(soup.find("select",{"name":"genre"}))
    
    matches = re.findall(sPattern, sHtmlContent)
    aResult = [True,matches]
    
    #VSlog(aResult)
    
    if aResult[0] is True:
        for aEntry in aResult[1]:
            CatURL = MOVIE_EN[0] + '?genre=' + aEntry
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', CatURL)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', aEntry, getGenreIcon(aEntry), oOutputParameterHandler)
        oGui.setEndOfDirectory()
    else:
        pass
        
def showLangsS():
    oGui = cGui()
    sPattern = '<option value=\".*\">(.+?)</option'
    
    sUrl = SERIE_EN[0]
    r = s.get(sUrl)
    soup = BeautifulSoup(r.content,"html.parser") 
    sHtmlContent = str(soup.find("select",{"name":"lang"}))
    
    matches = re.findall(sPattern, sHtmlContent)
    aResult = [True,matches]
    
    #VSlog(aResult)
    
    if aResult[0] is True:
        for aEntry in aResult[1]:
            CatURL = SERIE_EN[0] + '?lang=' + aEntry
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', CatURL)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', aEntry, icons + '/Language.png', oOutputParameterHandler)
        oGui.setEndOfDirectory()
    else:
        pass

def showGenresS():
    oGui = cGui()
    sPattern = '<option value=\"(.+?)\">(.+?)</option>'
    
    sUrl = SERIE_EN[0]
    r = s.get(sUrl)
    soup = BeautifulSoup(r.content,"html.parser") 
    sHtmlContent = str(soup.find("select",{"name":"genre"}))
    
    matches = re.findall(sPattern, sHtmlContent)
    aResult = [True,matches]
    
    #VSlog(aResult)
    
    if aResult[0] is True:
        for aEntry in aResult[1]:
            CatURL = SERIE_EN[0] + '?genre=' + aEntry[0]
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', CatURL)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', aEntry[1], getGenreIcon(aEntry[1]), oOutputParameterHandler)
        oGui.setEndOfDirectory()
    else:
        pass
    
    
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText is not False:
        sUrl = URL_MAIN + '/search?query='+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText is not False:
        sUrl = URL_MAIN + '/search?query='+sSearchText
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
    sHtmlContent = oRequestHandler.request()
     # (.+?) ([^<]+) .+?
    sPattern = '<div class="BlockItem.+?<a href="(.+?)" title="(.+?)">.+?data-src="(.+?)" alt='
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1].replace("مشاهدة","").replace("برنامج","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("مدبلج للعربية","").replace("مدبلج","").replace("عرض","").replace("الرو","")
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
               sYear = str(m.group(0))
               sTitle = sTitle.replace(sYear,'')
            sDisplayTitle = ('%s (%s)') % (sTitle, sYear)


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage != False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)
 
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
    sHtmlContent = oRequestHandler.request()
     # (.+?) ([^<]+) .+?
    sPattern = '<div class="BlockItem.+?<a href="(.+?)" title="(.+?)">.+?data-src="(.+?)" alt='
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("برنامج","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("مشاهدة وتحميل","").replace("اون لاين","").replace("مدبلج للعربية","مدبلج")
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
            sDesc = ''
            sTitle = sTitle.replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("موسم","S").replace("S ","S").split('الحلقة')[0]


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage != False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)
 
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
    sHtmlContent = oRequestHandler.request()

    sStart = '>المواسم</div>'
    sEnd = '<section class="text-center"'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    # (.+?) .+? ([^<]+)
    sPattern = '<a href="(.+?)" title="(.+?)">.+?data-src="(.+?)" alt='

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            sTitle = aEntry[1].replace("-"," ").replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("كامل","").replace("برنامج","").replace("فيلم","").replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الأول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("موسم","S").replace("S ","S")
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
            sDesc = ""

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sMovieUrl', sUrl)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addSeason(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 
 
def showEps():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    oParser = cParser()
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    # (.+?) .+? ([^<]+)
    sPattern = '<a class="sku" href="(.+?)" title=.+?data-src="(.+?)" alt.+?class="episode" style="display: inline;">.+?<i>(.+?)</i></span>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:

 
            sEp =  "E"+aEntry[2].replace(" ","")
            sTitle = sMovieTitle+sEp
            siteUrl = aEntry[0]
            sThumb = aEntry[1]
            sDesc = ''
            sHost = ''

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sHost', sHost)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            

 
            oGui.addEpisode(SITE_IDENTIFIER, 'showHostersepisode', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 

 
def __checkForNextPage(sHtmlContent):
    sPattern = '<meta property="og:url" content="(.+?)" />'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0] is True:
        URL_MAIN = aResult[1][0].split("?p=")[0]
    
    sPattern = '<a class=\"page-link\" href=\"(.+?)\">(.+?)</a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0] is True:
        for aEntry in aResult[1]:
            if 'التالي' in aEntry[1]:
                return URL_MAIN+aEntry[0]

    return False

  
def showHostersepisode():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    VSlog('Episode URL : ' + sUrl)
    LinksList = []
    oRequestHandler = cRequestHandler(sUrl)
    cook = oRequestHandler.GetCookies()
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('Cookie', cook)
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('origin', URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
            
    sPattern =  'name="codes" value="(.+?)">' 
    aResult = oParser.parse(sHtmlContent,sPattern)

    if aResult[0] is True:
        mcode = aResult[1][0] #+ '&submit=submit'
        VSlog('mcode : ' + mcode)
    
    
    sPattern =  '<form action="(.+?)" method="post">' 
    aResult = oParser.parse(sHtmlContent,sPattern)
   
    if aResult[0] is True:
        murl = aResult[1][0] 
        LinksList.append(murl)
        #VSlog('murl URL : ' + murl)
        import requests
        s = requests.Session()            
        headers = {'user-agent': 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1',
							'origin': "https://sh.shoffree.com",
							'referer': murl}
        data = {'codes':mcode}
        
        r = s.post(murl,data = data)
        sHtmlContent = r.content.decode('utf8')
        
        
        ## Watch Section
        soup = BeautifulSoup(sHtmlContent, "html.parser")
        watchContainer = soup.find("label",{"class":"btn-success"})
        watchlink = watchContainer.find("a")['href']
        #VSlog("Watchlink: " + str(watchlink))
        
        oHoster = cHosterGui().checkHoster(watchlink)
        sHosterUrl = watchlink
        LinksList.append(watchlink)
        if 'userload' in sHosterUrl:
          sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
        if 'shoffree' in sHosterUrl:
          sHosterUrl = sHosterUrl + "|Referer=" + murl
        if 'mystream' in sHosterUrl:
          sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 

        if oHoster != False:
          oHoster.setDisplayName(sMovieTitle + ' [Watch]')
          oHoster.setFileName(sMovieTitle)
          cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
                 
        ## Download Section
        DownloadContainer = soup.find("label",{"class":"btn btn-secondary"})
        DownloadLinkPage= DownloadContainer.find("a")['href']
        LinksList.append(DownloadLinkPage)
        DownloadLinkPage = DownloadLinkPage.replace("/d/","/stream/")+'?role=d'
        #VSlog("Downloadlink: " + str(DownloadLinkPage))
        
        oRequestHandler = cRequestHandler(DownloadLinkPage)
        sHtmlContent2 = oRequestHandler.request()
        soup = BeautifulSoup(sHtmlContent2, "html.parser")
            
        Container = soup.find("div",{"class":"EpisodesList"})
        downlinks = Container.findAll("a")
        
        for lnk in downlinks:
            quality = str(lnk.contents[0].replace("الجودة","").replace("(","").replace(")","").strip())
            size = lnk.em.text
            url = lnk['href']
            LinksList.append(url)
            oHoster = cHosterGui().checkHoster(url)

            sHosterUrl = url
            if 'userload' in sHosterUrl:
              sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'shoffree' in sHosterUrl:
              sHosterUrl = sHosterUrl + "|Referer=" + murl
            if 'mystream' in sHosterUrl:
              sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
              
            if oHoster != False:
              oHoster.setDisplayName('['+quality+']'+ ' ['+size+']')
              oHoster.setFileName(sMovieTitle)
              cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
        
        ## Others Section
        soup = BeautifulSoup(sHtmlContent, "html.parser")
       
        othersContainers = soup.findAll("div",{"class":"scroller_wrap"})
        
        for Cont in othersContainers:
            othersContainer = Cont.findAll("a")
            
            for sec in othersContainer:
                url = sec['href']
                sHost = sec.div.text.replace("\n","").strip()
                #VSlog('Other Links')
                #VSlog(url)
                if url not in LinksList:
                    LinksList.append(url)
                    oHoster = cHosterGui().checkHoster(url)
                    sHosterUrl = url
                    if 'userload' in sHosterUrl:
                      sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                    if 'shoffree' in sHosterUrl:
                      sHosterUrl = sHosterUrl + "|Referer=" + murl
                    if 'mystream' in sHosterUrl:
                      sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 

                    if oHoster != False:
                      oHoster.setDisplayName(sMovieTitle)
                      oHoster.setFileName(sMovieTitle)
                      cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    #VSlog(LinksList)  
    oGui.setEndOfDirectory()

 
def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    VSlog('Movie URL : ' + sUrl)
    LinksList = []
    oRequestHandler = cRequestHandler(sUrl)
    cook = oRequestHandler.GetCookies()
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('Cookie', cook)
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('origin', URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    
    #VSlog(sHtmlContent)
    oParser = cParser()
            
    sPattern =  '<a href="/movie(.+?)">' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    VSlog(aResult)
    if aResult[0] is True:
        murl = URL_MAIN+'movie'+aResult[1][0] 
        LinksList.append(murl)
    VSlog('murl URL : ' + murl)
    
    oParser = cParser()
    import requests
    s = requests.Session()            
    headers = {'user-agent': 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1',
							'referer': Quote(murl)}
    r = s.get(murl, headers=headers)
    sHtmlContent = r.content.decode('utf8')
    oRequestHandler = cRequestHandler(murl)
    cook = oRequestHandler.GetCookies()

    oParser = cParser()
            
    sPattern =  'name="codes" value="(.+?)">' 
    aResult = oParser.parse(sHtmlContent,sPattern)

    if aResult[0] is True:
        mcode = aResult[1][0] #+ '&submit=submit'
        #VSlog('mcode : ' + mcode)
    
    
    sPattern =  '<form action="(.+?)" method="post">' 
    aResult = oParser.parse(sHtmlContent,sPattern)
   
    if aResult[0] is True:
        murl2 = aResult[1][0] 
        LinksList.append(murl2)
        #VSlog('murl2 URL : ' + murl2)
        import requests
        s = requests.Session()            
        headers = {'user-agent': 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1',
							'origin': "https://sh.shoffree.com",
							'referer': murl}
        data = {'codes':mcode}
        
        r = s.post(murl2,data = data)
        sHtmlContent = r.content.decode('utf8')
        
        
        ## Watch Section
        soup = BeautifulSoup(sHtmlContent, "html.parser")
        watchContainer = soup.find("label",{"class":"btn-success"})
        watchlink = watchContainer.find("a")['href']
        
        oHoster = cHosterGui().checkHoster(watchlink)
        sHosterUrl = watchlink
        LinksList.append(watchlink)
        if 'userload' in sHosterUrl:
          sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
        if 'shoffree' in sHosterUrl:
          sHosterUrl = sHosterUrl + "|Referer=" + murl2
        if 'mystream' in sHosterUrl:
          sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 

        if oHoster != False:
          oHoster.setDisplayName(sMovieTitle + ' [Watch]')
          oHoster.setFileName(sMovieTitle)
          cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
                 
        ## Download Section
        DownloadContainer = soup.find("label",{"class":"btn btn-secondary"})
        DownloadLinkPage= DownloadContainer.find("a")['href']
        LinksList.append(DownloadLinkPage)
        DownloadLinkPage = DownloadLinkPage.replace("/d/","/stream/")+'?role=d'
        #VSlog(str(DownloadLinkPage))
        
        oRequestHandler = cRequestHandler(DownloadLinkPage)
        sHtmlContent2 = oRequestHandler.request()
        soup = BeautifulSoup(sHtmlContent2, "html.parser")
            
        Container = soup.find("div",{"class":"EpisodesList"})
        downlinks = Container.findAll("a")
        
        for lnk in downlinks:
            quality = str(lnk.contents[0].replace("الجودة","").replace("(","").replace(")","").strip())
            size = lnk.em.text
            url = lnk['href']
            LinksList.append(url)
            oHoster = cHosterGui().checkHoster(url)

            sHosterUrl = url
            if 'userload' in sHosterUrl:
              sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'shoffree' in sHosterUrl:
              sHosterUrl = sHosterUrl + "|Referer=" + murl2
            if 'mystream' in sHosterUrl:
              sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
              
            if oHoster != False:
              oHoster.setDisplayName('['+quality+']'+ ' ['+size+']')
              oHoster.setFileName(sMovieTitle)
              cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
        
        ## Others Section
        soup = BeautifulSoup(sHtmlContent, "html.parser")
       
        othersContainers = soup.findAll("div",{"class":"scroller_wrap"})
        
        for Cont in othersContainers:
            othersContainer = Cont.findAll("a")
            
            for sec in othersContainer:
                url = sec['href']
                sHost = sec.div.text.replace("\n","").strip()
                
                if url not in LinksList:
                    LinksList.append(url)
                    oHoster = cHosterGui().checkHoster(url)
                    sHosterUrl = url
                    if 'userload' in sHosterUrl:
                      sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                    if 'shoffree' in sHosterUrl:
                      sHosterUrl = sHosterUrl + "|Referer=" + murl2
                    if 'mystream' in sHosterUrl:
                      sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 

                    if oHoster != False:
                      oHoster.setDisplayName(sMovieTitle)
                      oHoster.setFileName(sMovieTitle)
                      cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    #VSlog(LinksList)  
    oGui.setEndOfDirectory()
