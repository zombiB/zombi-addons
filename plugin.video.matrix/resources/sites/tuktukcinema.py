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
 
SITE_IDENTIFIER = 'tuktukcinema'
SITE_NAME = 'tuktukcinema'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'https://tuktukcinema.net'

MOVIE_TOP = ('https://tuktukcinema.net/rate/', 'showMovies')
MOVIE_EN = ('https://tuktukcinema.net/category/movies/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%A7%D8%AC%D9%86%D8%A8%D9%8A/', 'showMovies')
MOVIE_HI = ('https://tuktukcinema.net/category/movies/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d9%87%d9%86%d8%af%d9%89/', 'showMovies')
MOVIE_ASIAN = ('https://tuktukcinema.net/category/movies/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%a7%d8%b3%d9%8a%d9%88%d9%8a1/', 'showMovies')
KID_MOVIES = ('https://tuktukcinema.net/category/movies/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%a7%d9%86%d9%85%d9%8a1/', 'showMovies')
MOVIE_TURK = ('https://tuktukcinema.net/category/movies/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%aa%d8%b1%d9%83%d9%8a1/', 'showMovies')
SERIE_EN = ('https://tuktukcinema.net/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa/?sercat=%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%a7%d8%ac%d9%86%d8%a8%d9%8a', 'showSeries')
SERIE_ASIA = ('https://tuktukcinema.net/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa/?sercat=%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%a3%d8%b3%d9%8a%d9%88%d9%8a', 'showSeries')
SERIE_TR = ('https://tuktukcinema.net/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa/?sercat=%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%aa%d8%b1%d9%83%d9%8a', 'showSeries')
ANIM_NEWS = ('https://tuktukcinema.net/category/%d8%a7%d9%86%d9%85%d9%8a/', 'showSeries')
SPORT_WWE = ('https://tuktukcinema.net/category/wwe/', 'showMovies')
DOC_SERIES = ('https://tuktukcinema.net/genre/%d9%88%d8%ab%d8%a7%d8%a6%d9%82%d9%8a/', 'showMovies')
URL_SEARCH = ('https://tuktukcinema.net/search/', 'showMovies')
URL_SEARCH_MOVIES = ('https://tuktukcinema.net/search/', 'showMovies')
URL_SEARCH_SERIES = ('https://tuktukcinema.net/search/', 'showSeries')
FUNCTION_SEARCH = 'showSeries'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

            
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = 'https://tuktukcinema.net/search/'+sSearchText
        showMovies(sUrl)
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

    # (.+?) .+? ([^<]+)   
    sPattern = '<a title="(.+?)" href="(.+?)" alt.+?<img data-src="(.+?)">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = str(aEntry[0]).decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            sTitle = sTitle.replace("مشاهدة","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","")
            siteUrl = str(aEntry[1])+'/watch'
            sThumbnail = str(aEntry[2])
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
  # ([^<]+) .+?

    sPattern = '<li><a href="([^<]+)">([^<]+)</a></li>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1].decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            sTitle =  "PAGE " + sTitle
            sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
            siteUrl = str(aEntry[0])
            sThumbnail = ""
            sInfo = ""


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			
            oGui.addTV(SITE_IDENTIFIER, 'showMovies', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
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
 # ([^<]+) .+?
    sPattern = '<a title="(.+?)" href="(.+?)" alt.+?<img data-src="(.+?)">'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = str(aEntry[0]).decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            sTitle = sTitle.replace("مشاهدة","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("مسلسل","")
            siteUrl = str(aEntry[1])
            sThumbnail = str(aEntry[2])
            sInfo = ''


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			
            oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)

        progress_.VSclose(progress_)
  # ([^<]+) .+?

    sPattern = '<li><a class="page-numbers" href="([^<]+)">([^<]+)</a></li>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1].decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            sTitle =  "PAGE " + sTitle
            sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
            siteUrl = URL_MAIN + str(aEntry[0])
            sThumbnail = ""
            sInfo = ""


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			
            oGui.addTV(SITE_IDENTIFIER, 'showSeries', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()


def showSeasons():
	oGui = cGui()
	import requests
    
	oInputParameterHandler = cInputParameterHandler()
	sUrl = oInputParameterHandler.getValue('siteUrl')
	sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
	sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
	oRequestHandler = cRequestHandler(sUrl)
	sHtmlContent = oRequestHandler.request()

   
	oParser = cParser()
	sId1 = ""
	sId2 = ""
    
    #Recuperation infos (.+?)

	sPattern = '<div class="loadTabsInSeries" data-slug="(.+?)" data-parent=".+?" data-id="(.+?)"></div><section'
	aResult = oParser.parse(sHtmlContent, sPattern)
	
	
	if (aResult[0] == True):
		total = len(aResult[1])
		progress_ = progress().VScreate(SITE_NAME)
		for aEntry in aResult[1]:
			progress_.VSupdate(progress_, total)
			if progress_.iscanceled():
				break
			sId1 = aEntry[0]
			sId2 = aEntry[1]

    #print sId
    
  # ([^<]+) .+?
	headers = {'Host': 'tuktukcinema.net',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
		'Accept': '*/*',
		'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
		'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		'X-Requested-With': 'XMLHttpRequest',
		'Referer': sUrl,
		'Connection': 'keep-alive'}
	data = {'action':'getTabsInsSeries','id':sId2,'slug':sId1,'parent':'0'}
	s = requests.Session()
	r = s.post('https://tuktukcinema.net/wp-admin/admin-ajax.php', headers=headers,data = data)
	sHtmlContent += r.content
    #print sHtmlContent
    # .+? ([^<]+)
	sPattern = ' <a href="([^<]+)" style.+?<div class="image"><img.+?src="([^<]+)" class=.+?<div class="ep-info">.+?<h2>([^<]+)</h2>'

	oParser = cParser()
	aResult = oParser.parse(sHtmlContent, sPattern)
	
	
	if (aResult[0] == True):
		total = len(aResult[1])
		progress_ = progress().VScreate(SITE_NAME)
		for aEntry in aResult[1]:
			progress_.VSupdate(progress_, total)
			if progress_.iscanceled():
				break
 
			sTitle = aEntry[2].replace("مشاهدة","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("مسلسل","")
			siteUrl = str(aEntry[0])+'/watch/'
			sThumbnail = aEntry[1]
			sInfo = ""
			


			oOutputParameterHandler = cOutputParameterHandler()
			oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
			oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
    # .+? ([^<]+)
	sPattern = '<li class="MovieItem">.+?<a href="([^<]+)">.+?<img src="([^<]+)">.+?<div class="TitleBlock">([^<]+)</div>'

	oParser = cParser()
	aResult = oParser.parse(sHtmlContent, sPattern)
	
	
	if (aResult[0] == True):
		total = len(aResult[1])
		progress_ = progress().VScreate(SITE_NAME)
		for aEntry in aResult[1]:
			progress_.VSupdate(progress_, total)
			if progress_.iscanceled():
				break
 
			sTitle = aEntry[2]
			siteUrl = str(aEntry[0])
			sThumbnail = aEntry[1]
			sInfo = ""
			


			oOutputParameterHandler = cOutputParameterHandler()
			oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
			oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			oGui.addMisc(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
	oGui.setEndOfDirectory()
 
     # (.+?)
def __checkForNextPage(sHtmlContent):
    sPattern = '<li><a href="(.+?)" >الصفحة التالية &laquo;</a></li>'
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if (aResult[0] == True):
        #print aResult[1][0]
        return aResult[1][0]

    return False


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')



    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    sHtmlContent = oRequestHandler.request()
    # (.+?) ([^<]+) .+?
               

    sPattern = 'data-server="([^<]+)">'
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
				sTitle = " " 
				if 'thevideo.me' in url:
					sTitle = " (thevideo.me)"
				if 'flashx' in url:
					sTitle = " (flashx)"
				if 'streamcherry' in url:
					sTitle = " (streamcherry)"
				if url.startswith('//'):
					url = 'http:' + url
				
					
            
				sHosterUrl = url 
				#print sHosterUrl
				oHoster = cHosterGui().checkHoster(sHosterUrl)
				if (oHoster != False):
					sDisplayTitle = sMovieTitle+sTitle
					oHoster.setDisplayName(sDisplayTitle)
					oHoster.setFileName(sMovieTitle)
					cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				

               
        
    sPattern = '<a target="_blank" href="([^<]+)" class="btn download_btn col-md-1">'
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
				sTitle = " " 
				if 'thevideo.me' in url:
					sTitle = " (thevideo.me)"
				if 'flashx' in url:
					sTitle = " (flashx)"
				if 'streamcherry' in url:
					sTitle = " (streamcherry)"
				if url.startswith('//'):
					url = 'http:' + url
            
				sHosterUrl = url
				#print sHosterUrl
				oHoster = cHosterGui().checkHoster(sHosterUrl)
				if (oHoster != False):
					sDisplayTitle = sMovieTitle+sTitle
					oHoster.setDisplayName(sDisplayTitle)
					oHoster.setFileName(sMovieTitle)
					cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				
                
    oGui.setEndOfDirectory()