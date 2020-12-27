#-*- coding: utf-8 -*-
#zombi.(@geekzombi)
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
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.player import cPlayer
import xbmcgui
import urllib2,urllib,re
import unicodedata
 
SITE_IDENTIFIER = 'movizland'
SITE_NAME = 'movizland'
SITE_DESC = 'arabic anime'
 
URL_MAIN = 'https://hd.movizland.online'

MOVIE_AR = ('https://hd.movizland.online/category/newmovies/arab/', 'showMovies')
MOVIE_EN = ('https://hd.movizland.online/category/newmovies/newforeign/', 'showMovies')
MOVIE_HI = ('https://hd.movizland.online/category/newmovies/india/', 'showMovies')
KID_MOVIES = ('https://hd.movizland.online/category/newmovies/anime/', 'showMovies')
MOVIE_TURK = ('https://hd.movizland.online/category/newmovies/turkey/', 'showMovies')
MOVIE_ASIAN = ('https://hd.movizland.online/category/newmovies/asia/', 'showMovies')

MOVIE_PACK = ('https://hd.movizland.online/category/newmovies/backs/', 'showMovie')

DOC_NEWS = ('https://hd.movizland.online/category/newmovies/documentary/', 'showMovies')

SERIE_EN = ('https://hd.movizland.online/category/series/foreign-series/', 'showSeries')
SERIE_AR = ('https://hd.movizland.online/category/series/arab-series/', 'showSeries')
SPORT_WWE = ('https://hd.movizland.online/category/series/wwe/', 'showMovies')

SERIE_TR = ('https://hd.movizland.online/category/series/turkish-series/', 'showSeries')
ANIM_NEWS = ('https://hd.movizland.online/category/series/anime-series/', 'showMovies')

URL_SEARCH = ('https://hd.movizland.online/search/', 'showMoviesearch')
URL_SEARCH_MOVIES = ('https://hd.movizland.online/search/', 'showMoviesearch')
URL_SEARCH_SERIES = ('https://hd.movizland.online/search/', 'showSearchSeries')
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
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = 'https://hd.movizland.online/search/'+sSearchText
        showSearchSeries(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = 'https://hd.movizland.online/search/'+sSearchText
        showMoviesearch(sUrl)
        oGui.setEndOfDirectory()
        return
   
 
def showMoviesearch(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 

      # (.+?) ([^<]+) .+?

    sPattern = '<div class="BlockItem"><a href="([^<]+)">.+?<div class="BlockImageItem"><img width=".+?" height=".+?" src="([^<]+)" class="attachment-defaultb size-defaultb wp-post-image" alt="([^<]+)" />'

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
 

            siteUrl = aEntry[0]
 
            sTitle = aEntry[2].decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            sTitle = sTitle.replace("مشاهدة","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","")
            
            sThumbnail = aEntry[1]
            sInfo = ''


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMoviesearch', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
 
def showSearchSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 

      # (.+?) ([^<]+) .+?

    sPattern = '<div class="BlockItem"><a href="([^<]+)"><div class="EPSNumber">.+?<div class="BlockImageItem"><img width=".+?" height=".+?" src="([^<]+)" class="attachment-defaultb size-defaultb wp-post-image" alt="([^<]+)" />'

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
 

            siteUrl = aEntry[0]
 
            sTitle = aEntry[2].decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            sTitle = sTitle.replace("مشاهدة","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","")
            
            sThumbnail = aEntry[1]
            sInfo = ''


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			

            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
 
    if not sSearch:
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


    sPattern = '<div class="BlockItem"><a href="([^<]+)">.+?src="([^<]+)" class.+?<div class="BlockTitle">([^<]+)</div>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 

            siteUrl = aEntry[0]
 
            sTitle = aEntry[2].decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            sTitle = sTitle.replace("مشاهدة","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","")
            
            sThumbnail = aEntry[1]
            sInfo = ''
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
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
def showMovie(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 

      # (.+?) ([^<]+) .+?


    sPattern = '<div class="BlockItem">.+?<a href="([^<]+)">.+?<img width=".+?" height=".+?" src="([^<]+)" class.+?<div class="BlockTitle">([^<]+)</div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 

            siteUrl = aEntry[0]
 
            sTitle = aEntry[2].decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            sTitle = sTitle.replace("مشاهدة","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","")
            
            sThumbnail = aEntry[1]
            sInfo = ''


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			

            oGui.addMovie(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()

def showEps():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
     # (.+?) ([^<]+) .+?
    sPattern = '<div class="BlockItem">.+?<a href="([^<]+)">.+?<img width=".+?" height=".+?" src="([^<]+)" class="attachment-defaultb size-defaultb wp-post-image" alt="([^<]+)" />'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 


            sTitle = aEntry[2].decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            sTitle = sTitle.replace("</em>","").replace("<em>","").replace("</span>","").replace("<span>","")
            siteUrl = str(aEntry[0])
            sThumbnail = str(aEntry[1])
            sInfo = ""
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
       
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
# ([^<]+) .+?
    sPattern = '<div class="BlockItem"><a href="(.+?)">.+?<img width=".+?" height=".+?" src="([^<]+)" class.+?class="BlockTitle">([^<]+)</div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 

            sTitle = aEntry[2].decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            sTitle = sTitle.replace("مشاهدة","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("مسلسل","").replace("Web-dl","")
 
 
            siteUrl = aEntry[0]
            sInfo = ""
            sThumbnail = str(aEntry[1])

			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler) 

        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()

def showEpisodes():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
     # (.+?) ([^<]+) .+?
    sPattern = '<div class="BlockItem"><a href="([^<]+)"><div class="EPSNumber"> <em>([^<]+)</em> <span>([^<]+)</span>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 


            sTitle1 = sMovieTitle 
            sTitle = sMovieTitle + aEntry[2]+" "+aEntry[1]
            siteUrl = str(aEntry[0])
            sThumbnail = sThumbnail
            sInfo = ""
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle1)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addMisc(SITE_IDENTIFIER, 'showEpisodes2', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
       
    oGui.setEndOfDirectory()

def showEpisodes2():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
     # (.+?) ([^<]+) .+?
    sPattern = '<div class="BlockItem"><a href="([^<]+)"><div class="EPSNumber"> <em>([^<]+)</em> <span>([^<]+)</span>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 


            sTitle = sMovieTitle + aEntry[2]+" "+aEntry[1]
            siteUrl = str(aEntry[0])
            sThumbnail = sThumbnail
            sInfo = ""
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
       
    oGui.setEndOfDirectory()
	
 
	
def __checkForNextPage(sHtmlContent):
    sPattern = '<li><a href="([^<]+)" >الصفحة التالية &laquo;</a></li>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False

 
def showHosters():
    oGui = cGui()
    import requests
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    #print sHtmlContent 

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

   
    oParser = cParser()

  # ([^<]+) .+?
    headers = {'Host': '4k.movizland.online',
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
     'Accept': '*/*',
     'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
     'X-Requested-With': 'XMLHttpRequest',
     'Referer': sUrl,
     'Connection': 'keep-alive'}

    data = {'watch':'1'}
    s = requests.Session()
    r = s.post(sUrl, headers=headers,data = data)
    sHtmlContent += r.content
    # ([^<]+) (.+?)      

    sPattern = '</td><td>([^<]+)</td><td><a href="(.+?)" target'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if (aResult[0] == True):
			total = len(aResult[1])
			progress_ = progress().VScreate(SITE_NAME)
			for aEntry in aResult[1]:
				progress_.VSupdate(progress_, total)
				if progress_.iscanceled():
					break
            
				url = str(aEntry[1])
				sTitle =  str(aEntry[0])
				if '?download' in url:
					url = url.replace("moshahda","ddcdd")
				if url.startswith('//'):
					url = 'http:' + url
            
				sHosterUrl = url 
				oHoster = cHosterGui().checkHoster(sHosterUrl)
				if (oHoster != False):
					oHoster.setDisplayName(sMovieTitle)
					oHoster.setFileName(sMovieTitle)
					cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				

			progress_.VSclose(progress_)
    # ([^<]+) (.+?)      

    sPattern = 'rel="nofollow" href="(.+?)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if (aResult[0] == True):
			total = len(aResult[1])
			progress_ = progress().VScreate(SITE_NAME)
			for aEntry in aResult[1]:
				progress_.VSupdate(progress_, total)
				if progress_.iscanceled():
					break
            
				url = str(aEntry[1])
				sTitle =  str(aEntry[0])
				if url.startswith('//'):
					url = 'http:' + url
            
				sHosterUrl = url 
				oHoster = cHosterGui().checkHoster(sHosterUrl)
				if (oHoster != False):
					oHoster.setDisplayName(sTitle)
					oHoster.setFileName(sMovieTitle)
					cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				

			progress_.VSclose(progress_)             

    sPattern = 'rel="nofollow" href="(.+?)">'
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
				if 'vidcloud' in url:
					sTitle = " (vidcloud)"
				if url.startswith('//'):
					url = 'http:' + url
            
				sHosterUrl = url 
				oHoster = cHosterGui().checkHoster(sHosterUrl)
				if (oHoster != False):
					oHoster.setDisplayName(sMovieTitle)
					oHoster.setFileName(sMovieTitle)
					cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				

			progress_.VSclose(progress_)            

    sPattern = 'allowfullscreen data-srcout="([^<]+)" FRAMEBORDER'
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
				if 'vidcloud' in url:
					sTitle = " (vidcloud)"
				if url.startswith('//'):
					url = 'http:' + url
            
				sHosterUrl = url 
				oHoster = cHosterGui().checkHoster(sHosterUrl)
				if (oHoster != False):
					oHoster.setDisplayName(sMovieTitle)
					oHoster.setFileName(sMovieTitle)
					cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				

			progress_.VSclose(progress_)           

    sPattern = '<IFRAME allowfullscreen SRC="(.+?)" FRAMEBORDER'
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
				if 'vidcloud' in url:
					sTitle = " (vidcloud)"
				if url.startswith('//'):
					url = 'http:' + url
            
				sHosterUrl = url 
				oHoster = cHosterGui().checkHoster(sHosterUrl)
				if (oHoster != False):
					oHoster.setDisplayName(sMovieTitle)
					oHoster.setFileName(sMovieTitle)
					cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				

			progress_.VSclose(progress_) 
                
    oGui.setEndOfDirectory()

def showHosters1():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();



    # (.+?) .+? ([^<]+)
               

    sPattern = 'href="(.+?)" class="ViewMovieNow">(.+?)</a>'
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
        
				url = str(aEntry[0])
				sTitle = str(aEntry[1]).decode("utf8").replace('"',"")
				sTitle = cUtil().unescape(sTitle).encode("utf8")
				sTitle = '[COLOR yellow]'+sTitle+'[/COLOR]'

				if 'thevideo.me' in url:
					sTitle = " (thevideo.me)"
				if 'moshahda' in url:
					url = url.replace("moshahda","ddcdd")
				if 'flashx' in url:
					sTitle = " (flashx)"
				if 'streamcherry' in url:
					sTitle = " (streamcherry)"
				if url.startswith('//'):
					url = 'https:' + url
            
				sHosterUrl = url 
				oHoster = cHosterGui().checkHoster(sHosterUrl)
				if (oHoster != False):
					sDisplayTitle = sMovieTitle+sTitle
					oHoster.setDisplayName(sDisplayTitle)
					oHoster.setFileName(sMovieTitle)
					cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				

			progress_.VSclose(progress_)
                
    oGui.setEndOfDirectory()