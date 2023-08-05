# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import VSlog, siteManager, addon
from resources.lib.parser import cParser
from resources.lib.util import Quote
from bs4 import BeautifulSoup
import os
ADDON = addon()
icons = ADDON.getSetting('defaultIcons')

SITE_IDENTIFIER = 'arabseed'
SITE_NAME = 'Arabseed'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

oParser = cParser()
 
oRequestHandler = cRequestHandler(URL_MAIN)
sHtmlContent = oRequestHandler.request()
    # (.+?) ([^<]+)

sPattern = 'HomeURL = "(.+?)";'
aResult = oParser.parse(sHtmlContent, sPattern)
    
if (aResult[0]):
    URL_MAIN = aResult[1][0]
    #VSlog(URL_MAIN)

MOVIE_CLASSIC = (URL_MAIN + '/index.php?cat=19530', 'showMovies')
MOVIE_EN = (URL_MAIN + '/index.php?cat=2195', 'showMovies')
MOVIE_AR = (URL_MAIN + '/index.php?cat=325393', 'showMovies')
MOVIE_DUBBED = (URL_MAIN + '/index.php?cat=3304', 'showMovies')
MOVIE_HI = (URL_MAIN + '/index.php?cat=3726', 'showMovies')
MOVIE_ASIAN = (URL_MAIN + '/index.php?cat=5025', 'showMovies')
MOVIE_TURK = (URL_MAIN + '/index.php?cat=325394', 'showMovies')
KID_MOVIES = (URL_MAIN + '/index.php?cat=3482', 'showMovies')
MOVIE_NETFLIX = (URL_MAIN + '/index.php?cat=136791', 'showMovies')
SERIE_TR = (URL_MAIN + '/index.php?cat=2925', 'showSeries')
SERIE_DUBBED = (URL_MAIN + '/index.php?cat=25308', 'showSeries')
SERIE_EGY = (URL_MAIN + '/index.php?cat=318494', 'showSeries')
SERIE_HEND = (URL_MAIN + '/index.php?cat=76025', 'showSeries')
SERIE_EN = (URL_MAIN + '/index.php?cat=4', 'showSeries')
SERIE_AR = (URL_MAIN + '/index.php?cat=4257', 'showSeries')
SERIE_KR = (URL_MAIN + '/index.php?cat=72239', 'showSeries')
RAMADAN_SERIES = (URL_MAIN + '/index.php?cat=318535/', 'showSeries')
SERIE_NETFLIX = (URL_MAIN + '/index.php?cat=136790', 'showMovies')
SPORT_WWE = (URL_MAIN + '/index.php?cat=2811', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '/find/?find=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '/find/?find=', 'showSeries')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'SEARCH_MOVIES', icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', 'SEARCH_SERIES', icons + '/Search.png', oOutputParameterHandler)
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', icons + '/MoviesEnglish.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عربية', icons + '/Arabic.png', oOutputParameterHandler)
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_DUBBED[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'افلام مدبلجة', icons + '/Arabic.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أسيوية', icons + '/Asian.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية', icons + '/Turkish.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_CLASSIC[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كلاسيكية', icons + '/Movies.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', icons + '/Hindi.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', icons + '/Cartoon.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', icons + '/TVShowsEnglish.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات عربية', icons + '/Arabic.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_EGY[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات مصرية', icons + '/Arabic.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', icons + '/Turkish.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_DUBBED[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات مدبلجة', icons + '/Dubbed.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_KR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات كورية', icons + '/TVShowsKorean.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', RAMADAN_SERIES)
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', ' 2023 مسلسلات رمضان', icons + '/Ramadan.png', oOutputParameterHandler)
    
    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND[0])
    # oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات هندية', icons + '/Hindi.png', oOutputParameterHandler)

    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', SERIE_DUBBED[0])
    # oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات مدبلجة', icons + '/Dubbed.png', oOutputParameterHandler)

    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    # oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات إنمي', icons + '/Anime.png', oOutputParameterHandler)  
 
    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    # oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'برامج تلفزيونية',icons + '/Programs.png', oOutputParameterHandler)
	
    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_PLAY[0])
    # oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'مسرحيات', icons + '/Theater.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_WWE[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مصارعة', icons + '/WWE.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NETFLIX[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات Netfilx', icons + '/TVShows.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NETFLIX[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'افلام Netfilx', icons + '/Movies.png', oOutputParameterHandler)
             
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
    ##VSlog("Movies Link : " + sUrl)
    ###VSlog("html Link : " + sHtmlContent)
    import requests
    s = requests.Session()            
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
							'Referer': Quote(sUrl)}
    r = s.post(sUrl, headers=headers)
    sHtmlContent = r.content.decode('utf8')
    
    if sSearch:
       import requests
       s = requests.Session()            
       headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
							'Referer': Quote(sUrl)}
       psearch = sUrl.rsplit('?find=', 1)[1]
       data = {'search':psearch,'type':'movies'}
       r = s.post(URL_MAIN + '/wp-content/themes/Elshaikh2021/Ajaxat/SearchingTwo.php', headers=headers,data = data)
       sHtmlContent = r.content.decode('utf8')
     # (.+?) ([^<]+) .+?
    
    sPattern = '<div class=\"PlayButton\">.*\s*<a href=\"(.+?)\">.*\s*<div class=\"Poster\">.*\s*<img src=\".*\".data-src=\"(.+?)\".*alt=\"(.+?)\">.*\s*</div>'
    

    matches = re.findall(sPattern, sHtmlContent)
    aResult = [True,matches]

	
    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
 
            sTitle = aEntry[2].replace("مشاهدة","").replace("برنامج","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("مدبلج للعربية","").replace("مدبلج","").replace("عرض","").replace("الرو","")
            siteUrl = aEntry[0]
            #VSlog("Movie Link : " + siteUrl)
            
            s1Thumb = aEntry[1]
            sThumb = re.sub(r'-\d*x\d*.','.', s1Thumb)
            ###VSlog(sThumb)
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
               sYear = str(m.group(0))
               sTitle = sTitle.replace(sYear,'')


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage != False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
def showPacks(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
    ##VSlog("Packs Link : " + sUrl)
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 

      # (.+?) ([^<]+) .+?


    sPattern = '<div class="BlockItem"><a href="([^<]+)">.+?src="([^<]+)" class.+?<div class="BlockTitle">([^<]+)</div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
 

            siteUrl = aEntry[0]
            sTitle = aEntry[2].replace("مشاهدة","").replace("برنامج","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("مدبلج للعربية","مدبلج")
            
            s1Thumb = aEntry[1]
            sThumb = re.sub(r'-\d*x\d*.','.', s1Thumb)
            sDesc = ''


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			

            oGui.addMovie(SITE_IDENTIFIER, 'showPack', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
 
        
 
    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage != False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showPacks', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)
        oGui.setEndOfDirectory()

def showPack():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    ##VSlog("Pack Link : " + sUrl)
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
            s1Thumb = aEntry[1]
            sThumb = re.sub(r'-\d*x\d*.','.', s1Thumb)
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
    
    ##VSlog("Series Page Link : " + sUrl)
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if sSearch:
       import requests
       s = requests.Session()            
       headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
							'Referer': Quote(sUrl)}
       psearch = sUrl.rsplit('?find=', 1)[1]
       data = {'search':psearch,'type':'series'}
       r = s.post(URL_MAIN + '/wp-content/themes/Elshaikh2021/Ajaxat/SearchingTwo.php', headers=headers,data = data)

  

       sHtmlContent = r.content.decode('utf8',errors='ignore')
       sPattern = '<div class="Movie.+?">.+?<a href="([^<]+)">.+?data-image="([^<]+)" alt="([^<]+)">'

    else:
     # (.+?) ([^<]+) .+?
       import requests
       s = requests.Session()            
       headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'}
       if 'category/' in sUrl:
           psearch = sUrl.rsplit('category/', 1)[1].replace('/','')
       if 'index.php' in sUrl:
           psearch = sUrl.rsplit('/index.php?cat=', 1)[1].replace('/','')
       data = {'category':psearch,'currentTermID':psearch}
       r = s.post(URL_MAIN + '/wp-content/themes/Elshaikh2021/Ajaxat/Home/FilteringShows.php', headers=headers,data = data)
       sHtmlContent = r.content.decode('utf8',errors='ignore')
       sHtmlContentfull = r.content.decode('utf8')
       sPattern = '<div class="Movie.+?">.+?<a href="([^<]+)">.+?data-image="([^<]+)" alt="([^<]+)">'

    sPattern = 'class=\"PlayButton\">.*\s*<a href=\"(.+?)\">.*\s*<div class=\"Poster\">.*\s*<img.class=\".*\".data-image=\"(.+?)\".*alt=\"(.+?)\">.*\s*</div>'
    matches = re.findall(sPattern, sHtmlContent)
    aResult = [True,matches]
    ##VSlog(aResult)
    itemList = []
    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
 
            sTitle = aEntry[2].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("برنامج","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("مشاهدة وتحميل","").replace("اون لاين","").replace("مدبلج للعربية","مدبلج")
            siteUrl = aEntry[0]
            ##VSlog("TV Show Link: " + siteUrl)
            
            s1Thumb = aEntry[1]
            sThumb = re.sub(r'-\d*x\d*.','.', s1Thumb)
            sDesc = ''
            sTitle = sTitle.replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("موسم","S").replace("S ","S").split('الحلقة')[0]

            if sTitle not in itemList:
                ##VSlog(sTitle + " NOT FOUND, WILL BE ADDED TO LIST")
                itemList.append(sTitle)
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
                if 'الموسم' in aEntry[2]:
                    oGui.addTV(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
                else:
                    oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

 
        
 
    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage != False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)
        oGui.setEndOfDirectory()
 
def showSeasons():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    ##VSlog("TV Show Link: " + sUrl)
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    oParser = cParser()
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
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
            r = s.post(URL_MAIN + '/wp-content/themes/Elshaikh2021/Ajaxat/Single/Episodes.php', headers=headers,data = data)
            sHtmlContent = r.content.decode('utf8',errors='ignore')
            sPattern = 'href="([^<]+)">([^<]+)<em>([^<]+)</em>'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] is True:
                oOutputParameterHandler = cOutputParameterHandler() 
                for aEntry in aResult[1]:
                    siteUrl = aEntry[0]
                    ##VSlog("Season Link: " + siteUrl)
                    sEp = "E"+aEntry[2]
                    sTitle = sSeason+sEp
                    sThumb = sThumb
                    sDesc = ''

                    oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
            

 
                    oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
    else:

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
                sTitle = sMovieTitle+' '+sEp
                siteUrl = aEntry[0]
                ##VSlog("Episodes Link: " + siteUrl)
                sThumb = sThumb
                sDesc = ''
                sHost = ''

                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sHost', sHost)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
            

 
                oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 
 
def showEps():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    ##VSlog("Episodes Link2: " + sUrl)
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
            ##VSlog("Episode Link: " + siteUrl)
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

    soup = BeautifulSoup(sHtmlContent, "html.parser")
    sHtmlContent = str(soup.find("div",{"class":"pagination"}))
    
    sPattern = '<li><a class=\"next.page-numbers\" href=\"(.+?)\">»<'
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        return URL_MAIN+aResult[1][0]

    return False

def showHosters():
    oGui = cGui()
    
    icons = ADDON.getSetting('defaultIcons')
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    from resources.lib.util import Quote

    oParser = cParser()
    
    sPattern =  '<a href="([^<]+)" class="watchBTn">' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0] is True:
        murl = aResult[1][0] 
        VSlog(murl)
        oRequest = cRequestHandler(murl)
        oRequest.addHeaderEntry('User-Agent', 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1')
        oRequest.addHeaderEntry('Referer', Quote(URL_MAIN))
        sHtmlContent = oRequest.request()
        soup = BeautifulSoup(sHtmlContent, "html.parser")
        sHtmlContent = soup.find("div",{"class":"containerServers"})
        
        sections = sHtmlContent.findAll("h3")
        
        
        sectionlist = []
        for i in range(0,len(sections)):
            if i < len(sections)-1:
            
                sStart = str(sections[i])
                sEnd = str(sections[i+1])
                oHtmlContent = oParser.abParse(str(sHtmlContent), sStart, sEnd)
                sectionlist.append(oHtmlContent)
                quality = sections[i].text.replace("مشاهدة ","")+'p'
                VSlog(quality)

                sPattern = 'data-link=\"(.+?)\">.*?\s*?<i class'

                aResult = [True, re.findall(sPattern, str(oHtmlContent))]
                VSlog(aResult)
                if aResult[0] is True:
                   for aEntry in aResult[1]:
                
                       url = aEntry
                       sThumb = icons + '/resolution/' + quality + '.png'
                       if url.startswith('//'):
                          url = 'http:' + url
                       sTitle = ('%s  [COLOR coral]%s[/COLOR]') % (sMovieTitle, quality)
                                                    
                       sHosterUrl = url
                       if 'userload' in sHosterUrl:
                          sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                       if 'mystream' in sHosterUrl:
                          sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN    
                       oHoster = cHosterGui().checkHoster(sHosterUrl)
                       if oHoster != False:
                          oHoster.setDisplayName(sTitle)
                          oHoster.setFileName(sMovieTitle)
                          cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
                    
            else:
                VSlog(sections[i])

                sStart = str(sections[i])
                VSlog("Last start: " + sStart)
                cHtmlContent = oParser.abParse(str(sHtmlContent), sStart)

                sPattern = 'data-link=\"(.+?)\">.*?\s*?<i class'
                quality = sections[i].text.replace("مشاهدة ","")+'p'
                aResult = [True, re.findall(sPattern, str(cHtmlContent))]

                if aResult[0] is True:
                   for aEntry in aResult[1]:
                
                       url = aEntry
                       VSlog("Hoster Link: " + url)
                       sThumb = icons + '/resolution/' + quality + '.png'
                       if url.startswith('//'):
                          url = 'http:' + url
                       sTitle = ('%s  [COLOR coral]%s[/COLOR]') % (sMovieTitle, quality)
                                                    
                       sHosterUrl = url
                       if 'userload' in sHosterUrl:
                          sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                       if 'mystream' in sHosterUrl:
                          sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN    
                       oHoster = cHosterGui().checkHoster(sHosterUrl)
                       if oHoster != False:
                          oHoster.setDisplayName(sTitle)
                          oHoster.setFileName(sMovieTitle)
                          cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
                          
    oGui.setEndOfDirectory()