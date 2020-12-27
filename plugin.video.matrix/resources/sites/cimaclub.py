#-*- coding: utf-8 -*-
#zombi
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress
from resources.lib.parser import cParser
from resources.lib.util import cUtil
import urllib2,urllib,re
import unicodedata
 
SITE_IDENTIFIER = 'cimaclub'
SITE_NAME = 'cimaclub'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'https://www.cimaclub.cam'



MOVIE_TOP = ('https://www.cimaclub.io/getposts?type=one&data=rating', 'showMovies')
MOVIE_EN = ('https://www.cimaclub.io/category/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%A3%D8%AC%D9%86%D8%A8%D9%8A-%D9%85%D8%AA%D8%B1%D8%AC%D9%85%D8%A9-%D8%A7%D9%88%D9%86-%D9%84%D8%A7%D9%8A%D9%86', 'showMovies')
MOVIE_AR = ('https://www.cimaclub.io/category/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%B9%D8%B1%D8%A8%D9%8A-%D8%A7%D9%88%D9%86-%D9%84%D8%A7%D9%8A%D9%86', 'showMovies')
MOVIE_TURK = ('https://www.cimaclub.io/category/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%AA%D8%B1%D9%83%D9%8A%D8%A9', 'showMovies')
MOVIE_HI = ('https://www.cimaclub.io/category/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D9%87%D9%86%D8%AF%D9%8A', 'showMovies')
MOVIE_ASIAN = ('https://www.cimaclub.io/category/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%A7%D8%B3%D9%8A%D9%88%D9%8A%D8%A9', 'showMovies')
KID_MOVIES = ('https://www.cimaclub.io/category/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%A7%D9%86%D9%8A%D9%85%D9%8A%D8%B4%D9%86', 'showMovies')

SERIE_LATIN = ('https://www.cimaclub.io/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%A8%D8%B1%D8%A7%D8%B2%D9%8A%D9%84%D9%8A%D8%A9', 'showSerie')
SERIE_DUBBED = ('https://www.cimaclub.io/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D9%85%D8%AF%D8%A8%D9%84%D8%AC%D9%87', 'showSerie')
SERIE_ASIA = ('https://www.cimaclub.io/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D9%83%D9%88%D8%B1%D9%8A', 'showSerie')
SERIE_HEND = ('https://www.cimaclub.cam/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d9%87%d9%86%d8%af%d9%8a%d8%a9/', 'showSerie')
SERIE_TR = ('https://www.cimaclub.io/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%AA%D8%B1%D9%83%D9%8A%D9%87', 'showSerie')
SERIE_EN = ('https://www.cimaclub.io/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%A7%D8%AC%D9%86%D8%A8%D9%8A%D8%A9', 'showSerie')
SERIE_AR = ('http://cimaclub.com/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%B9%D8%B1%D8%A8%D9%8A/', 'showSerie')
SERIE_GENRES = (True, 'showGenres')
ANIM_NEWS = ('https://www.cimaclub.io/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%A7%D9%86%D9%8A%D9%85%D9%8A', 'showSerie')
DOC_NEWS = ('https://www.cimaclub.io/category/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D9%88%D8%AB%D8%A7%D8%A6%D9%82%D9%8A%D8%A9', 'showMovies')
DOC_SERIES = ('https://www.cimaclub.io/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D9%88%D8%AB%D8%A7%D8%A6%D9%82%D9%8A%D8%A9', 'showSerie')
SPORT_NEWS = ('https://www.cimaclub.io/category/%D8%A7%D9%84%D9%85%D8%B5%D8%A7%D8%B1%D8%B9%D9%87-wwe', 'showMovies')
URL_SEARCH = ('https://www.cimaclub.io/search?s=', 'showMovies')
URL_SEARCH_MOVIES = ('https://www.cimaclub.io/search?s=', 'showMovies')
URL_SEARCH_SERIES = ('https://www.cimaclub.io/search?s=', 'showSerie')
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
        sUrl = 'https://www.cimaclub.io/search?s='+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = 'https://www.cimaclub.io/search?s='+sSearchText
        showSerie(sUrl)
        oGui.setEndOfDirectory()
        return
		
def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ["korean series","http://cimaclub.com/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D9%83%D9%88%D8%B1%D9%8A%D8%A9/"] )
    liste.append( ["مسلسلات-رمضان-2016","http://cimaclub.com/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%B9%D8%B1%D8%A8%D9%8A/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%B1%D9%85%D8%B6%D8%A7%D9%86-2016/"] )


    
	            
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSerie', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()   

 
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

    sPattern = '<div class="content-box">.+?<a href="([^<]+)" data-src="([^<]+)" class="image"></a>.+?<h3>([^<]+)</h3></a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if "فيلم" not in aEntry[2]:
				continue
 
            sTitle = str(aEntry[2]).decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            sTitle = sTitle.replace("مشاهدة","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","")
            siteUrl = str(aEntry[0]).replace("/film/","/watch/").replace("/post/","/watch/")
            sThumb = str(aEntry[1]).replace("(","").replace(")","")
            sDesc = ""
            annee = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
				annee = str(m.group(0))
				sTitle = sTitle.replace(annee,'')
            if annee:
				sTitle = sTitle + '(' + annee + ')'


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showServers', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()

def showSerie(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 
     # (.+?) ([^<]+) .+?
    sPattern = '<div class="content-box">.+?<a href="([^<]+)" data-src="([^<]+)" class="image"></a>.+?<h3>([^<]+)</h3></a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if "فيلم" in aEntry[2]:
				continue
 
            sTitle = aEntry[2]
            siteUrl = str(aEntry[0]).replace("/episode/","/watch/").replace("/post/","/watch/")
            sThumb = str(aEntry[1]).replace("(","").replace(")","")
            sDesc = ""


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addTV(SITE_IDENTIFIER, 'showServers', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSerie', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
		

	
def showEpisodes():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 # ([^<]+) .+?

    sPattern = '<a href="([^<]+)" class="col-6 col-s-4 col-m-3 col-l-1 button-block"><h3>([^<]+)<span>([^<]+)</span></h3></a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[2]+"-"+aEntry[1]
            siteUrl = str(aEntry[0]).replace("/episode/","/watch/").replace("/post/","/watch/")
            sThumb = str(sThumb)
            sDesc = ""
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            if 'season' in siteUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', '[COLOR cyan]'+sTitle+'[/COLOR]', '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addTV(SITE_IDENTIFIER, 'showServers', sTitle, '', sThumb, '', oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
	
def showSeries():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 
    sPattern = 'id="WatchBTn" href="([^<]+)" class'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = sMovieTitle
            siteUrl = str(aEntry)
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            if 'seasons' in sUrl:
                oGui.addMovie(SITE_IDENTIFIER, 'showSeries', aEntry[1], '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showServers', aEntry[1], '', sThumb, '', oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
       
        oGui.setEndOfDirectory()
 
       
 
 
 
def __checkForNextPage(sHtmlContent):
    sPattern = '<li class="active"><a href="javascript:;">.+?</a></li><li><a href="(.+?)">'
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if (aResult[0] == True):
        #print aResult[1][0]
        return aResult[1][0]

    return False

  
def showServers():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
	    #Affichage du menu  
    oGui.addText(SITE_IDENTIFIER,'[COLOR olive]-------سيرفرات المشاهدة--------[/COLOR]')



    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    sHtmlContent = oRequestHandler.request()

    #print sHtmlContent
   
    oParser = cParser()

    sId='0'
    # (.+?) ([^<]+) .+?

    sPattern = '&_post_id=([^<]+)",'
    aResult = oParser.parse(sHtmlContent, sPattern)

   
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            

        for i in range(0,5):



			
            sId = "https://www.cimaclub.io/ajaxCenter?_action=getserver&_post_id="+aEntry


   
			

            sTitle = 'server '+': '+str(i)
            siteUrl = sId+'&serverid='+str(i)
            sInfo = ""


            #print siteUrl 
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            

 
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
	    #Affichage du menu  
    oGui.addText(SITE_IDENTIFIER,'[COLOR olive]-------سيرفرات التحميل--------[/COLOR]')


    #print sHtmlContent2
    # (.+?) .+? ([^<]+)        	
    sPattern = 'rel="nofollow" href="(.+?)" class='
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if (aResult[0] == True):
			total = len(aResult[1])
			progress_ = progress().VScreate(SITE_NAME)
			for aEntry in aResult[1]:
				progress_.VSupdate(progress_, total)
				if progress_.iscanceled():
					break
            
				url = str(aEntry)
				sTitle = sMovieTitle
				if 'thevideo.me' in url:
					sTitle = " (thevideo.me)"
				if 'flashx' in url:
					sTitle = " (flashx)"
				if 'streamcherry' in url:
					sTitle = " (streamcherry)"
				if 'cloudvideo' in url:
					sTitle = " (cloudvideo)"
				if 'streamcloud' in url:
					sTitle = " (streamcloud)"
				if 'userscloud' in url:
					sTitle = " (userscloud)"
				if 'clicknupload' in url:
					sTitle = " (clicknupload)"
				if url.startswith('//'):
					url = 'http:' + url
				
					
            
				sHosterUrl = url 
				oHoster = cHosterGui().checkHoster(sHosterUrl)
				if (oHoster != False):
					sDisplayTitle = sTitle
					oHoster.setDisplayName(sDisplayTitle)
					oHoster.setFileName(sMovieTitle)
					cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
	    #Affichage du menu  
    oGui.addText(SITE_IDENTIFIER,'[COLOR olive]----------------------------[/COLOR]')
 
     # (.+?) ([^<]+) .+?
    sPattern = '<li><a class="Hoverable" href="([^<]+)" title="([^<]+)"><em>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1]
            siteUrl = str(aEntry[0]).replace("/episode/","/watch/").replace("/post/","/watch/")
            sThumb = ""
            sDesc = ""


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showServers', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
     # (.+?) ([^<]+) .+?
    sPattern = 'data-season=".+?" data-series=".+?"><a href="([^<]+)" title="([^<]+)">'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = '[COLOR cyan]'+aEntry[1]+'[/COLOR]'
            siteUrl = str(aEntry[0])
            sThumb = ""
            sDesc = ""


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
      

               
       
    oGui.setEndOfDirectory()	
 
def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')



    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    sHtmlContent = oRequestHandler.request()


    #(.+?)
               

    sPattern = '([^<]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)


    #print aResult

	
    if (aResult[0] == True):
			total = len(aResult[1])
			progress_ = progress().VScreate(SITE_NAME)
			for aEntry in aResult[1]:
				progress_.VSupdate(progress_, total)
				if progress_.iscanceled():
					break
        
				url = str(aEntry)
				sTitle = " "
				if 'thevideo.me' in url:
					sTitle = " (thevideo.me)"
				if 'flashx' in url:
					sTitle = " (flashx)"
				if 'Cloudvid' in url:
					sTitle = " (Cloudvid)"
				if 'govid' in url:
					url = url.replace("play","down").replace("embed-","")
				if url.startswith('//'):
					url = 'http:' + url
				
					
            
				sHosterUrl = url 
				oHoster = cHosterGui().checkHoster(sHosterUrl)
				if (oHoster != False):
					sDisplayTitle = sMovieTitle+sTitle
					oHoster.setDisplayName(sDisplayTitle)
					oHoster.setFileName(sMovieTitle)
					cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
				

			progress_.VSclose(progress_) 		
                
    oGui.setEndOfDirectory()