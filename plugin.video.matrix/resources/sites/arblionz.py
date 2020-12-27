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
from resources.lib.player import cPlayer
import urllib2,urllib,re
import unicodedata
 
SITE_IDENTIFIER = 'arblionz'
SITE_NAME = 'arblionz'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'https://www.arblionz.org'
MOVIE_EN = ('https://www.arblionz.org/category/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%A7%D8%AC%D9%86%D8%A8%D9%8A%D8%A9-%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%A7%D9%88%D9%86-%D9%84%D8%A7%D9%8A%D9%86-2', 'showMovies')
MOVIE_AR = ('https://www.arblionz.org/category/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9-1', 'showMovies')
MOVIE_HI = ('https://www.arblionz.org/category/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D9%87%D9%86%D8%AF%D9%8A%D8%A9/', 'showMovies')
RAMADAN_SERIES = ('https://www.arblionz.org/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%B1%D9%85%D8%B6%D8%A7%D9%86/', 'showMovies')

KID_MOVIES = ('https://www.arblionz.org/genre/%D8%A7%D9%86%D9%85%D9%8A%D8%B4%D9%86', 'showMovies')
SERIE_TR = ('https://www.arblionz.org/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%AA%D8%B1%D9%83%D9%8A%D8%A9-%D9%85%D8%AA%D8%B1%D8%AC%D9%85%D8%A9/', 'showMovies')
SERIE_TR_AR = ('https://www.arblionz.org/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%AA%D8%B1%D9%83%D9%8A%D8%A9-%D9%85%D8%AF%D8%A8%D9%84%D8%AC%D8%A9/', 'showMovies')
SERIE_EN = ('https://www.arblionz.org/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%A7%D8%AC%D9%86%D8%A8%D9%8A%D8%A9/', 'showMovies')
SERIE_AR = ('https://www.arblionz.org/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9/', 'showMovies')

ANIM_NEWS = ('https://www.arblionz.org/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%A7%D9%86%D9%85%D9%8A-%D9%85%D8%AA%D8%B1%D8%AC%D9%85%D8%A9/', 'showMovies')

REPLAYTV_NEWS = ('https://www.arblionz.org/category/%D8%A8%D8%B1%D8%A7%D9%85%D8%AC-%D8%AA%D9%84%D9%8A%D9%81%D8%B2%D9%8A%D9%88%D9%86%D9%8A%D8%A9/', 'showMovies')

DOC_NEWS = ('https://www.arblionz.org/genre/%D9%88%D8%AB%D8%A7%D8%A6%D9%82%D9%8A', 'showMovies')
DOC_SERIES = ('https://www.arblionz.org/genre/%D9%88%D8%AB%D8%A7%D8%A6%D9%82%D9%8A', 'showMovies')

SPORT_WWE = ('https://www.arblionz.org/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%B1%D9%85%D8%B6%D8%A7%D9%86/', 'showMovies')

URL_SEARCH = ('https://www.arblionz.org/?s=', 'showMovies')
URL_SEARCH_MOVIES = ('https://www.arblionz.org/?s=', 'showMovies')
URL_SEARCH_SERIES = ('https://www.arblionz.org/?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
 
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
        sUrl = 'https://www.arblionz.org/?s='+sSearchText
        showMovies(sUrl)
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
    sgn = requests.Session()
    data = sgn.get(sUrl).content
    sHtmlContent = data
 # ([^<]+) .+?
    sPattern = '<a href="([^<]+)" data-src="([^<]+)" class="image"></a>.+?<h3>([^<]+)</h3></a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = str(aEntry[2]).decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            sTitle = sTitle.replace("مشاهدة","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","")
            siteUrl = str(aEntry[0]).replace("/film/","/watch/").replace("/episode/","/watch/")
            sThumb = str(aEntry[1])
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
				sYear = str(m.group(0))
				sTitle = sTitle.replace(sYear,'')
            sDisplayTitle = ('%s (%s)') % (sTitle, sYear)


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showServer', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
  
def showServer():
    import requests
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')



    oRequestHandler = cRequestHandler(sUrl)
    sgn = requests.Session()
    data = sgn.get(sUrl).content
    sHtmlContent = data

    #print sHtmlContent
   
    oParser = cParser()
    sId='0'
    # (.+?) ([^<]+)
    sPattern = '_post_id=(.+?)",'
    aResult = oParser.parse(sHtmlContent, sPattern)

   
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sId = aEntry

            for i in range(0,5):

				sTitle = 'server '+': '+str(i)
				siteUrl = 'https://www.arblionz.org/ajaxCenter?_action=getserver&_post_id='+sId+'&serverid='+str(i)
				sInfo = ""

				oOutputParameterHandler = cOutputParameterHandler()
				oOutputParameterHandler.addParameter('siteUrl', siteUrl)
				oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
				oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            

 
				oGui.addMovie(SITE_IDENTIFIER, 'showHosters2', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
 
        progress_.VSclose(progress_)
    sId='0'
    # (.+?) ([^<]+)
    sPattern = '_post_id=(.+?)",'
    aResult = oParser.parse(sHtmlContent, sPattern)

   
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break





			
            sId = aEntry

            #print sId
   
			

            sTitle = 'سيرفرات التحميل'
            siteUrl = 'https://arblionz.com/ajaxCenter?_action=getdownloadlinks&postId='+sId
            sInfo = ""

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            

 
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
 
        progress_.VSclose(progress_)
     # (.+?) ([^<]+) .+?
    sPattern = '<a class="active" href="(.+?)"><span>([^<]+)</span><span class="numEp">([^<]+)</span>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1] + aEntry[2]
            siteUrl = str(aEntry[0]).replace("/episode/","/watch/")
            sThumb = ""
            sDesc = ""
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showServer', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
    # (.+?)
               
       
    oGui.setEndOfDirectory()
 
def showHosters():
    import requests
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')



    oRequestHandler = cRequestHandler(sUrl)
    cook = oRequestHandler.GetCookies()
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('origin', 'www.arblionz.org')
    oRequestHandler.addHeaderEntry('Cookie', cook)
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Referer', 'https://www.arblionz.org/download/%D9%81%D9%8A%D9%84%D9%85-beyond-the-woods-2020-%D9%85%D8%AA%D8%B1%D8%AC%D9%85-%D8%A7%D9%88%D9%86-%D9%84%D8%A7%D9%8A%D9%86')
    sHtmlContent = oRequestHandler.request()
    # (.+?) .+?
    #print sHtmlContent           

    sPattern = 'href="(.+?)"'
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
				if url.startswith('//'):
					url = 'http:' + url
            
				sHosterUrl = url 
				oHoster = cHosterGui().checkHoster(sHosterUrl)
				if (oHoster != False):
					sDisplayTitle = sTitle
					oHoster.setDisplayName(sDisplayTitle)
					oHoster.setFileName(sMovieTitle)
					cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				
                
    oGui.setEndOfDirectory()  
def showHosters2():
    import requests
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')



    oRequestHandler = cRequestHandler(sUrl)
    cook = oRequestHandler.GetCookies()
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('origin', 'www.arblionz.org')
    oRequestHandler.addHeaderEntry('Cookie', cook)
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Referer', 'https://www.arblionz.org/download/%D9%81%D9%8A%D9%84%D9%85-beyond-the-woods-2020-%D9%85%D8%AA%D8%B1%D8%AC%D9%85-%D8%A7%D9%88%D9%86-%D9%84%D8%A7%D9%8A%D9%86')
    sHtmlContent = oRequestHandler.request()
    # (.+?) .+?       

    sPattern = "([^<]+)"
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
				if 'mystream' in url:
					sTitle = " (mystream)"
				if 'streamcherry' in url:
					sTitle = " (streamcherry)"
				if 'streamango' in url:
					sTitle = " (streamango)"
				if url.startswith('//'):
					url = 'http:' + url
            
				sHosterUrl = url 
				oHoster = cHosterGui().checkHoster(sHosterUrl)
				if (oHoster != False):
					sDisplayTitle = sTitle
					oHoster.setDisplayName(sDisplayTitle)
					oHoster.setFileName(sMovieTitle)
					cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				
                
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
    sPattern = '<span class="label series"><i class="icon-play mr-1"></i>([^<]+)</span>.+?<a href="([^<]+)" class="box">.+?data-src="([^<]+)" class="img-fluid w-100 lazy" alt="([^<]+)"/>.+?<span class="badge badge-pill badge-secondary ml-1">([^<]+)</span>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = str(aEntry[3]).decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            sTitle = sTitle.replace("مشاهدة","").replace("مترجم","").replace("فيلم","")
            siteUrl = str(aEntry[1])
            sThumb = str(aEntry[2])
            sYear = aEntry[4]
            sDisplayTitle = ('%s (%s) ') % (sTitle, sYear)
            sDesc = '[COLOR yellow]'+aEntry[0]+'[/COLOR]'+" episodes"


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

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
    sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()
    
    #Recuperation infos
    sNote = ''

    sPattern = '<div class="widget-body"><div class="text-white"><p>([^<]+)</p>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        sNote = aResult[1][0]
     # (.+?) ([^<]+) .+?
    sPattern = 'class="text-white">([^<]+)</a>.+?<a href="(.+?)">.+?<img src="(.+?)" class="img-fluid" alt='

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = sMovieTitle+' '+aEntry[0]
            siteUrl = str(aEntry[1])
            sThumb = aEntry[2]
            sDesc = sNote.decode("utf8")
            sDesc = cUtil().unescape(sDesc).encode("utf8")
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
    # .+? ([^<]+)
    sPattern = '<a href="http([^<]+).com/watch/(.+?)"'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent.replace('\n',''))
    #fh.close()

    #print aResult
   
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = "مشاهدة"
            sTitle = '[COLOR cyan]'+sTitle+'[/COLOR]'
            siteUrl = 'http'+aEntry[0]+'.com/watch/' + str(aEntry[1])
            sThumb = sThumb
            sDesc = ""
 
            #print sUrl
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            

 
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
 
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
	

 
 
def __checkForNextPage(sHtmlContent):
    sPattern = '<li class="active"><a href="javascript:;">.+?</a></li><li><a href="(.+?)">'
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if (aResult[0] == True):
        #print aResult[1][0]
        return aResult[1][0]

    return False