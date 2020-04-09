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
 
SITE_IDENTIFIER = 'cimau'
SITE_NAME = 'cima4u'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'https://cima4u.tv'


MOVIE_EN = ('https://cima4u.tv/category/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%A7%D8%AC%D9%86%D8%A8%D9%8A-movies-english/', 'showMovies')
MOVIE_AR = ('https://cima4u.tv/category/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%B9%D8%B1%D8%A8%D9%8A-arabic-movies/', 'showMovies')
MOVIE_HI = ('https://cima4u.tv/category/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D9%87%D9%86%D8%AF%D9%8A-indian-movies/', 'showMovies')
MOVIE_PACK = ('http://w.cima4u.tv/category/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%A7%D8%AC%D9%86%D8%A8%D9%8A-movies-english/%D8%B3%D9%84%D8%A7%D8%B3%D9%84-%D8%A7%D9%84%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%A7%D9%84%D9%83%D8%A7%D9%85%D9%84%D8%A9-full-pack/', 'showPack')

KID_MOVIES = ('https://cima4u.tv/category/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D9%83%D8%B1%D8%AA%D9%88%D9%86-movies-anime-cartoon/', 'showMovies')
SERIE_TR = ('https://cima4u.tv/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-series/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%AA%D8%B1%D9%83%D9%8A%D8%A9-series-turkish/', 'showSeries')

SERIE_ASIA = ('https://cima4u.tv/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-series/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%A7%D8%B3%D9%8A%D9%88%D9%8A%D8%A9-series-asian/', 'showSeries')
SERIE_EN = ('https://cima4u.tv/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-series/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%A7%D8%AC%D9%86%D8%A8%D9%8A-series-english/', 'showSeries')
SERIE_AR = ('https://cima4u.tv/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-series/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9-arabic-series/', 'showSeries')

RAMADAN_SERIES = ('http://cima4u.tv/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-series/%D8%B1%D9%85%D8%B6%D8%A7%D9%86-2019/', 'showSeries')

ANIM_NEWS = ('https://cima4u.tv/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-series/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D9%83%D8%B1%D8%AA%D9%88%D9%86-anime-series/', 'showSeries')

DOC_SERIES = ('https://bit.ly/33D7tK0', 'showSeries')


REPLAYTV_NEWS = ('https://cima4u.tv/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-series/%D8%A8%D8%B1%D8%A7%D9%85%D8%AC-%D8%AA%D9%84%D9%8A%D9%81%D8%B2%D9%8A%D9%88%D9%86%D9%8A%D8%A9-tv-shows/', 'showSeries')
URL_SEARCH = ('https://cima4u.tv/?s=', 'showMovies')
URL_SEARCH_MOVIES = ('https://cima4u.tv/?s=', 'showMovies')
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
        sUrl = 'https://cima4u.tv/?s='+sSearchText
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
 #([^<]+) .+?

    sPattern = '<div class="block"><a href="(.+?)"><div class="image"><div class="img1" style="background-image:url(.+?);"></div>.+?<div class="boxtitle">(.+?)</div><div class="boxdetil">(.+?)</div>'

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
            sTitle = sTitle.replace("مشاهدة","").replace("مترجم","").replace("فيلم","").replace("اون لاين","")
            siteUrl = str(aEntry[0])
            sThumbnail = str(aEntry[1]).replace("(","").replace(")","")
            sInfo = str(aEntry[3])
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
			
            oGui.addMovie(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()

  
def showLinks():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
            
    sPattern =  '<meta itemprop="embedURL" content="(.+?)" />' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if (aResult[0] == True):
        m3url = aResult[1][0] 
        oRequest = cRequestHandler(m3url)
        sHtmlContent = oRequest.request()
    oGui.addText(SITE_IDENTIFIER,'[COLOR olive]-------سيرفرات المشاهدة--------[/COLOR]')

    #print sUrl
    


    sPage='0'

    sPattern = 'data-link="([^<]+)" class=".+?"><img.+?src=".+?" width="40" height="40" alt="" />(.+?)</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

   
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            sPage = str(aEntry[0])
            sTitle = 'server '+':'+ aEntry[1]
            siteUrl = 'http://live.cima4u.tv/structure/server.php?id='+sPage
            sInfo = ''


            #print siteUrl 
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            

 
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, '', oOutputParameterHandler)

            

 
        progress_.VSclose(progress_)
	    #Affichage du menu  
    oGui.addText(SITE_IDENTIFIER,'[COLOR olive]-------سيرفرات التحميل--------[/COLOR]')
    # (.+?)
               

    sPattern = '<a href="([^<]+)" target="_blank" class="download_link">'
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
				if 'mystream' in url:
					sTitle = " (mystream)"
				if 'streamcherry' in url:
					sTitle = " (streamcherry)"
				if 'streamango' in url:
					sTitle = " (streamango)"
				if url.startswith('//'):
					url = 'http:' + url
				if url.startswith('https://www.ok'):
					url = url.replace("www.","")
            
				sHosterUrl = url 
				oHoster = cHosterGui().checkHoster(sHosterUrl)
				if (oHoster != False):
					sDisplayTitle = sMovieTitle+sTitle
					oHoster.setDisplayName(sDisplayTitle)
					oHoster.setFileName(sMovieTitle)
					cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				

			progress_.VSclose(progress_) 
       
    oGui.setEndOfDirectory()  
def showLink():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()
    # .+? ([^<]+)
    sPattern = '<a class="button button--.+?" href="([^<]+)">مشاهدة الأن</a>'
    
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
 
            sTitle = "مشاهدة"
            sTitle = '[COLOR cyan]'+sTitle+'[/COLOR]'
            siteUrl = aEntry
            sThumbnail = sThumbnail
            sInfo = ""
 
            #print sUrl
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            if '/tag/'  in siteUrl:
                oGui.addMisc(SITE_IDENTIFIER, 'showPacks', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler) 
            else: 
	            oGui.addMisc(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler) 
 
        progress_.VSclose(progress_)
       
    oGui.setEndOfDirectory()
def showLink2():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()
    # .+? ([^<]+)
    sPattern = '<a class="button button--.+?" href="([^<]+)">مشاهدة الأن</a>'
    
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
 
            sTitle = "مشاهدة"
            sTitle = '[COLOR cyan]'+sTitle+'[/COLOR]'
            siteUrl = aEntry
            sThumbnail = sThumbnail
            sInfo = ""
 
            #print sUrl
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            if '/tag/'  in siteUrl:
                oGui.addMisc(SITE_IDENTIFIER, 'showPacks2', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler) 
            else: 
	            oGui.addMisc(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler) 
 
        progress_.VSclose(progress_)
       
    oGui.setEndOfDirectory()
def showPack(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 #([^<]+) .+?

    sPattern = '<div class="block"><a href="(.+?)"><div class="image"><div class="img1" style="background-image:url(.+?);"></div>.+?<div class="boxtitle">(.+?)</div><div class="boxdetil">(.+?)</div>'

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
            sTitle = sTitle.replace("مشاهدة","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("اون لاين","")
            siteUrl = str(aEntry[0])
            sThumbnail = str(aEntry[1]).replace("(","").replace(")","")
            sInfo = str(aEntry[3])


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showPacks', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showPack', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
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
 

    sPattern = '<div class="block"><a href="(.+?)"><div class="image"><div class="img1" style="background-image:url(.+?);"></div>.+?<div class="boxtitle">(.+?)</div><div class="boxdetil">(.+?)</div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[2].replace("&#8217;","'")
            siteUrl = str(aEntry[0])
            sThumbnail = str(aEntry[1]).replace("(","").replace(")","")
            sInfo = str(aEntry[3])


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showLink2', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)

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

    oParser = cParser()
            
    sPattern =  '<meta itemprop="embedURL" content="(.+?)" />' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if (aResult[0] == True):
        m3url = aResult[1][0] 
        oRequest = cRequestHandler(m3url)
        sHtmlContent = oRequest.request()
 #([^<]+).+?
    sPattern = '<div class="col-md-2" style="padding: 5px; text-align: center;"><a href="(.+?)" class=".+?"><span class="icon-desktop"></span>(.+?)</a></div>'

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
            siteUrl = str(aEntry[0])
            sThumbnail = str(sThumbnail)
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addMisc(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumbnail, '', oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
	

 
       
 
 
 
def __checkForNextPage(sHtmlContent):
    sPattern = '<li><a href="([^<]+)">الصفحة التالية &laquo;</a></li>'
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if (aResult[0] == True):
        #print aResult[1][0]
        return aResult[1][0]

    return False

def showPacks():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
            
    sPattern =  '<a class="button button--.+?" href="([^<]+)">مشاهدة الأن</a>' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if (aResult[0] == True):
        m3url = aResult[1][0] 
        oRequest = cRequestHandler(m3url)
        sHtmlContent = oRequest.request()
 # ([^<]+) .+?
    sPattern = '<div class="block"><a href="(.+?)"><div class="image"><div class="img1" style="background-image:url(.+?);"></div>.+?<div class="boxtitle">(.+?)</div><div class="boxdetil">(.+?)</div>'

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
            sTitle = sTitle.replace("مشاهدة","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("اون لاين","")
            siteUrl = str(aEntry[0])
            sThumbnail = str(aEntry[1]).replace("(","").replace(")","")
            sInfo = str(aEntry[3])
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
       
    oGui.setEndOfDirectory()


def showPacks2():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
            
    sPattern =  '<a class="button button--.+?" href="([^<]+)">مشاهدة الأن</a>' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if (aResult[0] == True):
        m3url = aResult[1][0] 
        oRequest = cRequestHandler(m3url)
        sHtmlContent = oRequest.request()
 # ([^<]+) .+?
    sPattern = '<div class="block"><a href="(.+?)"><div class="image"><div class="img1" style="background-image:url(.+?);"></div>.+?<div class="boxtitle">(.+?)</div><div class="boxdetil">(.+?)</div>'

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
            sTitle = sTitle.replace("مشاهدة","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("اون لاين","")
            siteUrl = str(aEntry[0])
            sThumbnail = str(aEntry[1]).replace("(","").replace(")","")
            sInfo = str(aEntry[3])
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addMovie(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
       
    oGui.setEndOfDirectory()
    



def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();


    #print sHtmlContent
    #(.+?)
               

    sPattern = '<iframe.+?src="(.+?)"'
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
				if 'mystream' in url:
					sTitle = " (mystream)"
				if 'streamcherry' in url:
					sTitle = " (streamcherry)"
				if 'streamango' in url:
					sTitle = " (streamango)"
				if url.startswith('//'):
					url = 'http:' + url
				if url.startswith('https://www.ok'):
					url = url.replace("www.","")
            
				sHosterUrl = url 
				oHoster = cHosterGui().checkHoster(sHosterUrl)
				if (oHoster != False):
					sDisplayTitle = sMovieTitle+sTitle
					oHoster.setDisplayName(sDisplayTitle)
					oHoster.setFileName(sMovieTitle)
					cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				

			progress_.VSclose(progress_) 
                
    oGui.setEndOfDirectory()