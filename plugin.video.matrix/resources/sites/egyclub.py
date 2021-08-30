#-*- coding: utf-8 -*-
#zombi https://github.com/zombiB/zombi-addons/
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, isMatrix
from resources.lib.parser import cParser
import re
 
SITE_IDENTIFIER = 'egyclub'
SITE_NAME = 'egyclub'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'https://www.egy-club.com'
MOVIE_EN = ('https://www.egy-club.com/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%a7%d8%ac%d9%86%d8%a8%d9%8a', 'showMovies')
MOVIE_AR = ('https://www.egy-club.com/category/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%B9%D8%B1%D8%A8%D9%8A', 'showMovies')
MOVIE_HI = ('https://www.egy-club.com/category/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D9%87%D9%86%D8%AF%D9%8A', 'showMovies')

MOVIE_TURK = ('https://www.egy-club.com/category/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%AA%D8%B1%D9%83%D9%8A', 'showMovies')
KID_MOVIES = ('https://www.egy-club.com/category/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%A7%D9%86%D9%8A%D9%85%D9%8A%D8%B4%D9%86', 'showMovies')

MOVIE_CLASSIC = ('https://www.egy-club.com/category/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D9%83%D9%84%D8%A7%D8%B3%D9%8A%D9%83%D9%8A%D8%A9-%D8%B9%D8%A7%D9%84%D9%85%D9%8A%D8%A9', 'showMovies')
SERIE_EN = ('https://www.egy-club.com/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%A7%D8%AC%D9%86%D8%A8%D9%8A', 'showSeries')
SERIE_TR = ('https://www.egy-club.com/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%AA%D8%B1%D9%83%D9%8A', 'showSeries')
SERIE_AR = ('https://www.egy-club.com/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%B9%D8%B1%D8%A8%D9%8A', 'showSeries')
SERIE_ASIA = ('https://www.egy-club.com/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D9%83%D9%84%D8%A7%D8%B3%D9%8A%D9%83%D9%8A%D8%A9', 'showSeries')
DOC_NEWS = ('https://www.egy-club.com/category/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D9%88%D8%AB%D8%A7%D8%A6%D9%82%D9%8A%D8%A9', 'showMovies')


URL_SEARCH = ('https://www.egy-club.com/?s=', 'showMovies')
URL_SEARCH_MOVIES = ('https://www.egy-club.com/?s=%D9%81%D9%8A%D9%84%D9%85+', 'showMovies')
URL_SEARCH_SERIES = ('https://www.egy-club.com/?s=%D9%85%D8%B3%D9%84%D8%B3%D9%84+', 'showSeries')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'SEARCH_MOVIES', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', 'SEARCH_SERIES', 'search.png', oOutputParameterHandler)

            
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = 'https://www.egy-club.com/?s='+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = 'https://www.egy-club.com/?s='+sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return

 
def showMovies(sSearch = ''):
    import requests
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    if isMatrix(): 
       sHtmlContent = str(sHtmlContent.encode('latin-1',errors='ignore'),'utf-8',errors='ignore')
 # (.+?) ([^<]+) .+?
    sPattern = '<div class="BlockItem"><a href="(.+?)"><img data-src="(.+?)">.+?<div class="TitleBlockMovieNormal InFilmBlock">(.+?)</div><div class="DescBlockMovieNormal">(.+?)</div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = str(aEntry[1])
            sTitle = sTitle.replace("مشاهدة","").replace("مشاهده","").replace("مترجمة","").replace("مسلسل","").replace("انمي","").replace("مترجم","").replace("كاملة","").replace("جودة عالية","").replace("كامل","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("أون لاين","")
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sMovieTitle2', sTitle) 
            oOutputParameterHandler.addParameter('sYear', sYear)                  
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showServer', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 # ([^<]+) .+?
    sPattern = '"slug":([^<]+),.+?"termid":([^<]+),'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = "[COLOR teal]Next >>>[/COLOR]"
            slug = str(aEntry[0])
            termid = str(aEntry[1])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('slug', slug)
            oOutputParameterHandler.addParameter('sId', "20")
			
            oGui.addMovie(SITE_IDENTIFIER, 'showMovie', sTitle, '', '', '', oOutputParameterHandler)

        progress_.VSclose(progress_)

 
    if not sSearch:
        oGui.setEndOfDirectory()
 
def showMovie():
    import requests
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    slug = oInputParameterHandler.getValue('slug')
    sId = oInputParameterHandler.getValue('sId')
 
    headers = {'Host': 'www.egy-club.com',
							'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Mobile Safari/537.36',
							'Accept': '*/*',
							'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
							'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
							'X-Requested-With': 'XMLHttpRequest',
							'Referer': sUrl,
							'Connection': 'keep-alive'}
    data = {'taxonomy':'category','slug':slug,'termid':'2','offset':sId}

    s = requests.Session()
    r = s.post('https://www.egy-club.com/wp-content/themes/Final/Interface/Ajax/archive/block.php', data = data)
    sHtmlContent = r.content.decode('utf8',errors='ignore')
    if isMatrix(): 
       sHtmlContent = str(sHtmlContent.encode('latin-1',errors='ignore'),'utf-8',errors='ignore')
     # (.+?) ([^<]+) .+?
    sPattern = '<div class="BlockItem"><a href="(.+?)"><img data-src="(.+?)">.+?<div class="TitleBlockMovieNormal InFilmBlock">(.+?)</div><div class="DescBlockMovieNormal">(.+?)</div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
		
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = str(aEntry[2])
            sTitle = sTitle.replace("مشاهدة","").replace("كاملة","").replace("جودة عالية","").replace("كامل","").replace("مترجمة","").replace("مسلسل","").replace("انمي","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("أون لاين","")
            siteUrl = str(aEntry[0])
            sThumb = str(aEntry[1])
            sDesc = str(aEntry[3])
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sMovieTitle2', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addMovie(SITE_IDENTIFIER, 'showServer', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
 # ([^<]+) .+?
    sPattern = '<a href="([^<]+)">'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
 
        sTitle = "[COLOR teal]Next >>>[/COLOR]"

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl',siteUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('slug', slug)
        oOutputParameterHandler.addParameter('sId', int(sId)+20)
			
        oGui.addMovie(SITE_IDENTIFIER, 'showMovie', sTitle, '', 'next.png', '', oOutputParameterHandler)

        progress_.VSclose(progress_)
       
    oGui.setEndOfDirectory()
 
def showSeries(sSearch = ''):
    import requests
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')



    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    if isMatrix(): 
       sHtmlContent = str(sHtmlContent.encode('latin-1',errors='ignore'),'utf-8',errors='ignore')
 # ([^<]+) .+?
    sPattern = '<div class="BlockItem">.+?<a href="([^<]+)">.+?<img data-src="([^<]+)">.+?<div class="TitleBlockMovieNormal InFilmBlock">([^<]+)</div>.+?<div class="DescBlockMovieNormal">([^<]+)</div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = str(aEntry[2])
            sTitle = sTitle.replace("مشاهدة","").replace("مترجمة","").replace("مسلسل","").replace("انمي","").replace("مترجم","").replace("كامل","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("كامل","")
            siteUrl = str(aEntry[0])
            sThumb = str(aEntry[1])
            sDesc = str(aEntry[3])
            sYear = ''
            sDisplayTitle2 = sTitle.split('الحلقة')[0].split('حلقة')[0].split('الموسم')[0].split('موسم')[0]
            sDisplayTitle2 = sDisplayTitle2.split('مدبلج')[0]
            sDisplayTitle = sTitle.replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("S ","S").replace("موسم","S").replace("S ","S")


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle2)
            oOutputParameterHandler.addParameter('sMovieTitle2', sDisplayTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)

            oGui.addTV(SITE_IDENTIFIER, 'showServer', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

 # ([^<]+) .+?
    sPattern = '"slug":([^<]+),.+?"termid":([^<]+),'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = "[COLOR teal]Next >>>[/COLOR]"
            slug = str(aEntry[0])
            termid = str(aEntry[1])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('slug', slug)
            oOutputParameterHandler.addParameter('sId', "20")
			
            oGui.addTV(SITE_IDENTIFIER, 'showSerie', sTitle, '', '', '', oOutputParameterHandler)

        progress_.VSclose(progress_)
 
 
    if not sSearch:
        oGui.setEndOfDirectory() 
 
def showSerie():
    import requests
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    slug = oInputParameterHandler.getValue('slug')
    sId = oInputParameterHandler.getValue('sId')
 
    headers = {'Host': 'www.egy-club.com',
							'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Mobile Safari/537.36',
							'Accept': '*/*',
							'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
							'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
							'X-Requested-With': 'XMLHttpRequest',
							'Referer': sUrl,
							'Connection': 'keep-alive'}
    data = {'taxonomy':'category','slug':slug,'termid':'10','offset':sId}

    s = requests.Session()
    r = s.post('https://www.egy-club.com/wp-content/themes/Final/Interface/Ajax/archive/block.php',data = data)
    sHtmlContent = r.content.decode('utf8',errors='ignore')
     # (.+?) ([^<]+) .+?
    sPattern = '<a href="([^<]+)">.+?<img data-src="([^<]+)">.+?<div class="TitleBlockMovieNormal InFilmBlock">([^<]+)</div>.+?<div class="DescBlockMovieNormal">([^<]+)</div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 


            sTitle = str(aEntry[2])
            sTitle = sTitle.replace("مشاهدة","").replace("كاملة","").replace("جودة عالية","").replace("كامل","").replace("مترجمة","").replace("مسلسل","").replace("انمي","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("أون لاين","")
            siteUrl = str(aEntry[0])
            sThumb = str(aEntry[1])
            sDesc = str(aEntry[3])
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addMovie(SITE_IDENTIFIER, 'showServer', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
 # ([^<]+) .+?
    sPattern = '<a href="([^<]+)">'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
 
        sTitle = "[COLOR teal]Next >>>[/COLOR]"

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl',siteUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('slug', slug)
        oOutputParameterHandler.addParameter('sId', int(sId)+20)
			
        oGui.addTV(SITE_IDENTIFIER, 'showSerie', sTitle, '', 'next.png', '', oOutputParameterHandler)

        progress_.VSclose(progress_)
       
    oGui.setEndOfDirectory()  
def showServer():
    oGui = cGui()
    import requests
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sMovieTitle2 = oInputParameterHandler.getValue('sMovieTitle2')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    #print sHtmlContent 

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    sHtmlContent = oRequestHandler.request()
    if isMatrix(): 
       sHtmlContent = sHtmlContent.encode('utf8',errors='ignore').decode('utf8',errors='ignore')

   
    oParser = cParser()
    
    #Recuperation infos
    sId = ''
     # (.+?) ([^<]+) .+?
    sPattern = 'href="https://www.egy-club.com/wp-json/wp/v2/posts/(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        sId = aResult[1][0]
    
    for i in range(0,7):
        progress_ = progress().VScreate(SITE_NAME)
            
        headers = {'Host': 'www.egy-club.com',
							'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
							'Accept': '*/*',
							'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
							'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
							'X-Requested-With': 'XMLHttpRequest',
							'Referer': sUrl,
							'Connection': 'keep-alive'}
        data = {'action':'GetServer','post':sId,'id':str(i)}
        s = requests.Session()
				
        r = s.post('https://www.egy-club.com/wp-admin/admin-ajax.php',data = data)
        page = r.content.decode('utf8',errors='ignore')        

    # (.+?) ([^<]+) .+?
        sPattern = '<iframe.+?src="(.+?)"'
        oParser = cParser()
        aResult = oParser.parse(page, sPattern)
        if (aResult[0] == True):
            total = len(aResult[1])
            progress_ = progress().VScreate(SITE_NAME)
            for aEntry in aResult[1]:
                progress_.VSupdate(progress_, total)
                if progress_.iscanceled():
                   break
            
                url = str(aEntry)
                sTitle = sMovieTitle2
                if url.startswith('//'):
                   url = 'http:' + url
            
                sHosterUrl = url 
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                   oHoster.setDisplayName(sTitle)
                   oHoster.setFileName(sTitle)
                   cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
				

            progress_.VSclose(progress_)  
       
    oGui.setEndOfDirectory()