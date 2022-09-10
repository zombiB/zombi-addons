# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager
from resources.lib.parser import cParser
from resources.lib.util import Quote
 
SITE_IDENTIFIER = 'arabseed'
SITE_NAME = 'arabseed'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_CLASSIC = (URL_MAIN + '/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d9%83%d9%84%d8%a7%d8%b3%d9%8a%d9%83%d9%8a%d9%87/', 'showMovies')
MOVIE_EN = (URL_MAIN + '/category/foreign-movies3/', 'showMovies')
MOVIE_AR = (URL_MAIN + '/category/arabic-movies-5/', 'showMovies')
MOVIE_DUBBED = (URL_MAIN + '/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d9%85%d8%af%d8%a8%d9%84%d8%ac%d8%a9/', 'showMovies')
MOVIE_HI = (URL_MAIN + '/category/indian-movies/', 'showMovies')
MOVIE_ASIAN = (URL_MAIN + '/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%a7%d8%b3%d9%8a%d9%88%d9%8a%d8%a9/', 'showMovies')
MOVIE_TURK = (URL_MAIN + '/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%aa%d8%b1%d9%83%d9%8a%d8%a9/', 'showMovies')
KID_MOVIES = (URL_MAIN + '/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%a7%d9%86%d9%8a%d9%85%d9%8a%d8%b4%d9%86/', 'showMovies')
SERIE_TR = (URL_MAIN + '/category/2925', 'showSeries')
SERIE_DUBBED = (URL_MAIN + '/category/25308', 'showSeries')
SERIE_ASIA = (URL_MAIN + '/category/72239', 'showSeries')
SERIE_HEND = (URL_MAIN + '/category/76025', 'showSeries')
SERIE_EN = (URL_MAIN + '/category/4', 'showSeries')
SERIE_AR = (URL_MAIN + '/category/4257', 'showSeries')

RAMADAN_SERIES = (URL_MAIN + '/category/238601', 'showSeries')
ANIM_NEWS = (URL_MAIN + '/category/2496', 'showSeries')

REPLAYTV_PLAY = (URL_MAIN + '/category/%D9%85%D8%B3%D8%B1%D8%AD%D9%8A%D8%A7%D8%AA-%D8%B9%D8%B1%D8%A8%D9%8A%D9%87/', 'showMovies')
REPLAYTV_NEWS = (URL_MAIN + '/category/%D8%A8%D8%B1%D8%A7%D9%85%D8%AC-%D8%AA%D9%84%D9%81%D8%B2%D9%8A%D9%88%D9%86%D9%8A%D8%A9', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '/find/?find=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '/find/?find=', 'showSeries')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'SEARCH_MOVIES', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', 'SEARCH_SERIES', 'search.png', oOutputParameterHandler)
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', 'film.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عربية', 'film.png', oOutputParameterHandler)
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أسيوية', 'film.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية', 'film.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_CLASSIC[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كلاسيكية', 'film.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', 'film.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', 'crtoon.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', 'mslsl.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات عربية', 'mslsl.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أسيوية', 'mslsl.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', 'mslsl.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات هندية', 'mslsl.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_DUBBED[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات مدبلجة', 'mslsl.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات إنمي', 'anime.png', oOutputParameterHandler)  
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'برامج تلفزيونية', 'brmg.png', oOutputParameterHandler)
	
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_PLAY[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'مسرحيات', 'msrh.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/category/%d9%85%d8%b5%d8%a7%d8%b1%d8%b9%d9%87/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مصارعة', 'wwe.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/category/netfilx/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-netfilz/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات Netfilx', 'mslsl.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/category/netfilx/%d8%a7%d9%81%d9%84%d8%a7%d9%85-netfilx/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'افلام Netfilx', 'film.png', oOutputParameterHandler)
             
    oGui.setEndOfDirectory()

 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText is not False:
        sUrl = URL_MAIN + '/find/?find='+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText is not False:
        sUrl = URL_MAIN + '/find/?find='+sSearchText
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

    oParser = cParser()
    sURL_MAIN='0'
    # (.+?) ([^<]+)

    sPattern = 'HomeURL = "(.+?)";'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        sURL_MAIN = aResult[1][0]
    if sSearch:
       import requests
       s = requests.Session()            
       headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
							'Referer': Quote(sUrl)}
       psearch = sUrl.rsplit('?find=', 1)[1]
       data = {'search':psearch,'type':'movies'}
       r = s.post(sURL_MAIN + '/wp-content/themes/Elshaikh2021/Ajaxat/SearchingTwo.php', headers=headers,data = data)
       sHtmlContent = r.content.decode('utf8')
     # (.+?) ([^<]+) .+?
    sPattern = '</div><a href="([^<]+)">.+?data-src="(.+?)" alt="(.+?)">'
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[2].replace("مشاهدة","").replace("برنامج","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("مدبلج للعربية","").replace("مدبلج","")
            siteUrl = aEntry[0]
            sThumb = aEntry[1]
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
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
def showPacks(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 

      # (.+?) ([^<]+) .+?


    sPattern = '<div class="BlockItem"><a href="([^<]+)">.+?src="([^<]+)" class.+?<div class="BlockTitle">([^<]+)</div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 

            siteUrl = aEntry[0]
            sTitle = aEntry[2].replace("مشاهدة","").replace("برنامج","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("مدبلج للعربية","مدبلج")
            
            sThumb = aEntry[1]
            sDesc = ''


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			

            oGui.addMovie(SITE_IDENTIFIER, 'showPack', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage != False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showPacks', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()

def showPack():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
     # (.+?) ([^<]+) .+?
    sPattern = '<div class="BlockItem"><a href="([^<]+)">.+?src="([^<]+)" class.+?<div class="BlockTitle">([^<]+)</div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
 


            sTitle = aEntry[2].replace("</em>","").replace("<em>","").replace("</span>","").replace("<span>","").replace("مشاهدة","").replace("برنامج","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("مدبلج للعربية","مدبلج")
            siteUrl = aEntry[0]
            sThumb = aEntry[1]
            sDesc = ""
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

    oParser = cParser()
    sURL_MAIN='0'
    # (.+?) ([^<]+)

    sPattern = 'HomeURL = "(.+?)";'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        sURL_MAIN = aResult[1][0]
    if sSearch:
       import requests
       s = requests.Session()            
       headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
							'Referer': Quote(sUrl)}
       psearch = sUrl.rsplit('?find=', 1)[1]
       data = {'search':psearch,'type':'series'}
       r = s.post(sURL_MAIN + '/wp-content/themes/Elshaikh2021/Ajaxat/SearchingTwo.php', headers=headers,data = data)
       sHtmlContent = r.content.decode('utf8',errors='ignore')
       sPattern = '<div class="Movie.+?">.+?<a href="([^<]+)">.+?data-image="([^<]+)" alt="([^<]+)">'

    else:
     # (.+?) ([^<]+) .+?
       import requests
       s = requests.Session()            
       headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'}
       psearch = sUrl.rsplit('/category/', 1)[1]
       data = {'category':psearch,'currentTermID':psearch}
       r = s.post(sURL_MAIN + '/wp-content/themes/Elshaikh2021/Ajaxat/Home/FilteringShows.php', headers=headers,data = data)
       sHtmlContent = r.content.decode('utf8',errors='ignore')
       sPattern = '<div class="Movie.+?">.+?<a href="([^<]+)">.+?data-image="([^<]+)" alt="([^<]+)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[2].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("برنامج","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("مشاهدة وتحميل","").replace("اون لاين","").replace("مدبلج للعربية","مدبلج")
            siteUrl = aEntry[0]
            sThumb = aEntry[1]
            sDesc = ''
            sTitle = sTitle.replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("موسم","S").replace("S ","S").split('الحلقة')[0]


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            if 'الموسم' in aEntry[2]:
                oGui.addTV(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage != False:
            oOutputParameterHandler = cOutputParameterHandler()
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
    sHtmlContent = oRequestHandler.request()
    sURL_MAIN='0'
    # (.+?) ([^<]+)

    sPattern = 'HomeURL = "(.+?)";'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        sURL_MAIN = aResult[1][0]
    # (.+?) .+? ([^<]+)
    sPattern = 'data-id="(.+?)" data-season="(.+?)"><i class="fa fa-folder"></i>الموسم <span>(.+?)</span></li>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            sSeason = aEntry[2].replace("مترجم","").replace("مترجمة","").replace(" الحادي عشر","11").replace(" الثاني عشر","12").replace(" الثالث عشر","13").replace(" الرابع عشر","14").replace(" الخامس عشر","15").replace(" السادس عشر","16").replace(" السابع عشر","17").replace(" الثامن عشر","18").replace(" التاسع عشر","19").replace(" العشرون","20").replace(" الحادي و العشرون","21").replace(" الثاني و العشرون","22").replace(" الثالث و العشرون","23").replace(" الرابع والعشرون","24").replace(" الخامس و العشرون","25").replace(" السادس والعشرون","26").replace(" السابع والعشرون","27").replace(" الثامن والعشرون","28").replace(" التاسع والعشرون","29").replace(" الثلاثون","30").replace(" الحادي و الثلاثون","31").replace(" الثاني والثلاثون","32").replace(" الاول","1").replace(" الثاني","2").replace(" الثانى","2").replace(" الثالث","3").replace(" الرابع","4").replace(" الخامس","5").replace(" السادس","6").replace(" السابع","7").replace(" الثامن","8").replace(" التاسع","9").replace(" العاشر","10")
            sSeason = sMovieTitle+" S"+sSeason
            pseason = aEntry[1]
            post = aEntry[0]
            import requests
            s = requests.Session()            
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'}
            data = {'post_id':post,'season':pseason}
            r = s.post(sURL_MAIN + '/wp-content/themes/Elshaikh2021/Ajaxat/Single/Episodes.php', headers=headers,data = data)
            sHtmlContent = r.content.decode('utf8',errors='ignore')
            sPattern = 'href="([^<]+)">([^<]+)<em>([^<]+)</em>'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] is True:
                oOutputParameterHandler = cOutputParameterHandler() 
                for aEntry in aResult[1]:
                    siteUrl = aEntry[0]
                    sEp = "E"+aEntry[2]
                    sTitle = sSeason+sEp
                    sThumb = sThumb
                    sDesc = ''

                    oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
            

 
                    oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
       
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

    sStart = '<div class="ContainerEpisodesList"'
    sEnd = '<div style="clear: both;"></div>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    # (.+?) .+? ([^<]+)
    sPattern = '<a href="(.+?)">.+?<em>(.+?)</em>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:

 
            sEp = "E"+aEntry[1].replace(" ","")
            if "مدبلج" in sMovieTitle:
                sMovieTitle = sMovieTitle.replace("مدبلج","")
                sMovieTitle = "مدبلج"+sMovieTitle
            sTitle = sMovieTitle+sEp
            siteUrl = aEntry[0]
            sThumb = sThumb
            sDesc = ''
            sHost = ''

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sHost', sHost)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            

 
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 

 
def __checkForNextPage(sHtmlContent):
    sPattern = '<a class="next page-numbers" href="(.+?)">'
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0] is True:
        return URL_MAIN+aResult[1][0]

    return False

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    oParser = cParser()
            
    sPattern =  '<a href="([^<]+)" class="watchBTn">' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0] is True:
        m3url2 = aResult[1][0] 
        oRequest = cRequestHandler(m3url2)
        sHtmlContent2 = oRequest.request()


    # (.+?) .+? ([^<]+)
               
    sPattern = 'data-post="(.+?)" data-server="(.+?)" data-qu="(.+?)" class'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent2, sPattern)


	
    if aResult[0] is True:
        for aEntry in aResult[1]:
            import requests
            s = requests.Session()            
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
							'Referer': Quote(sUrl)}
            data = {'post_id':aEntry[0],'server':aEntry[1],'qu':aEntry[2]}
            r = s.post(URL_MAIN +'/wp-content/themes/Elshaikh2021/Ajaxat/Single/Server.php', headers=headers,data = data)
            sHtmlContent = r.content.decode('utf8',errors='ignore')
            sTitle = aEntry[2]
            sTitle = ('%s  [COLOR coral]%s[/COLOR]') % (sMovieTitle, sTitle)
   
            sPattern = 'src="(.+?)"'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
	
            if aResult[0] is True:
               for aEntry in aResult[1]:
        
                   url = str(aEntry)
                   sThumb = sThumb
                   if url.startswith('//'):
                      url = 'http:' + url
								            
                   sHosterUrl = url
                   if 'userload' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                   if 'moshahda' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                   if 'mystream' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN    
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster != False:
                      sDisplayTitle = sTitle
                      oHoster.setDisplayName(sDisplayTitle)
                      oHoster.setFileName(sMovieTitle)
                      cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    oGui.setEndOfDirectory()