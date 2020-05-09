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
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.player import cPlayer
import urllib2,urllib,re
import unicodedata
 
SITE_IDENTIFIER = 'awaan'
SITE_NAME = 'awaan'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'http://awaan.ae/'
URL_SERIE = 'https://www.awaan.ae/show/allprograms/30348/%D8%A7%D9%84%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA'

MOVIE_AR = ('https://www.awaan.ae/show/allprograms/208109/%D8%A3%D9%81%D9%84%D8%A7%D9%85?p=1', 'showMovies')
SERIE_AR = ('https://www.awaan.ae/show/allprograms/30348/%D8%A7%D9%84%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA?p=1', 'showSeries')

RAMADAN_SERIES = ('https://www.awaan.ae/show/allprograms/214766/%D8%B1%D9%85%D8%B6%D8%A7%D9%86?p=1', 'showSeries')
KID_CARTOON = ('https://www.awaan.ae/show/allprograms/205911/%D9%83%D8%A7%D8%B1%D8%AA%D9%88%D9%86?p=1', 'showSeries')
REPLAYTV_NEWS = ('https://www.awaan.ae/show/allprograms/30350/%D8%AA%D8%B1%D9%81%D9%8A%D9%87?p=1', 'showSeries')
REPLAYTV_PLAY = ('http://awaan.ae/show/205952/%D9%85%D8%B3%D8%B1%D8%AD%D9%8A%D8%A7%D8%AA-%D8%B2%D9%85%D8%A7%D9%86?p=1', 'showEps')
ISLAM_SHOWS = ('https://www.awaan.ae/show/allprograms/30349/%D8%A5%D8%B3%D9%84%D8%A7%D9%85%D9%8A%D8%A7%D8%AA?p=1', 'showSeries')

ISLAM_QURAN = ('https://www.awaan.ae/show/allprograms/208779/%D8%A7%D9%84%D9%82%D8%B1%D8%A2%D9%86-%D8%A7%D9%84%D9%83%D8%B1%D9%8A%D9%85?p=1', 'showSeries')
URL_SEARCH = ('https://www.awaan.ae/research', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Search', 'search.png', oOutputParameterHandler)

            
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = 'https://www.awaan.ae/research'+sSearchText
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
 # .+? ([^<]+)

    sPattern = '<div class="col-md-3 col-sm-4 col-xs-6 shows-video-col">.+?<a href="([^<]+)">.+?<p style="display: none">([^<]+)</p>.+?data-src="([^<]+)" style'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = str(aEntry[1]).decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            siteUrl = str(aEntry[0])
            sThumbnail = 'https:'+str(aEntry[2])
            sInfo = ""


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)

        progress_.VSclose(progress_)
    page = sUrl.split('?p=')[1]
    page = int(page)+1
    sTitle = 'More' 
    sTitle = '[COLOR red]'+sTitle+'[/COLOR]'
    page = str(page)
    siteUrl = sUrl.split('?p=')[0]
    siteUrl = siteUrl +'?p='+ page

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl',siteUrl)
    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
    oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
    oGui.addMovie(SITE_IDENTIFIER, 'showMovies', sTitle, '', 'next.png', '', oOutputParameterHandler)
 
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
 #.+?([^<]+)

    sPattern = ' <div class="col-md-3 col-sm-4 col-xs-6 shows-video-col">.+?<a href="([^<]+)">.+?<p style="display: none">([^<]+)</p>.+?<div class="img-div scaleZoomImg">.+?<div class="embed-responsive-item image-div lazy-image-handler" data-src="([^<]+)" style'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = str(aEntry[1]).decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            siteUrl = str(aEntry[0])+'?p=1'
            sThumbnail = 'https:'+str(aEntry[2])
            sInfo = ""


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			
            oGui.addMisc(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)

        progress_.VSclose(progress_)
    page = sUrl.split('?p=')[1]
    page = int(page)+1
    sTitle = 'More' 
    sTitle = '[COLOR red]'+sTitle+'[/COLOR]'
    page = str(page)
    siteUrl = sUrl.split('?p=')[0]
    siteUrl = siteUrl +'?p='+ page

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl',siteUrl)
    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
    oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
    oGui.addMovie(SITE_IDENTIFIER, 'showSeries', sTitle, '', 'next.png', '', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
 
def __checkForNextPage(sHtmlContent):
    sPattern = ''
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if (aResult[0] == True):

        return '?p='+aResult[1][0]
    return False
  
def showEps():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    sLink = ""
    sLink = sUrl
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
# ([^<]+) .+?
    sPattern = '<div class="embed-responsive-item image-div  lazy-image-handler  "  data-src="([^<]+)"  style="background-image.+?<div class="content">.+?<a href="([^<]+)" class="title-link">([^<]+)</a>'

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
            siteUrl = str(aEntry[1])
            sTitle = str(aEntry[2])
            sThumbnail = 'https:'+str(aEntry[0])
            sInfo = "" 

 
            #print sUrl
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            

 
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
 
        progress_.VSclose(progress_)
    page = sUrl.split('?p=')[1]
    page = int(page)+1
    sTitle = 'More' 
    sTitle = '[COLOR red]'+sTitle+'[/COLOR]'
    page = str(page)
    siteUrl = sUrl.split('?p=')[0]
    siteUrl = siteUrl +'?p='+ page

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl',siteUrl)
    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
    oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
    oGui.addMovie(SITE_IDENTIFIER, 'showEps', sTitle, '', 'next.png', '', oOutputParameterHandler)
 

       
    oGui.setEndOfDirectory()

 

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    oParser = cParser()
            
    sPattern =  'href="([^<]+)" class="btn btn-awaanbluebtn btn-viewall">شاهد الآن</a' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if (aResult[0] == True):
        m3url = aResult[1][0]
        if m3url.startswith('//'):
			m3url = 'http:' + m3url 	
        oRequest = cRequestHandler(m3url)
        sHtmlContent = oRequest.request()

    oParser = cParser()
            
    sPattern =  'id="video_embedd" src="([^<]+)" allowfullscreen=' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if (aResult[0] == True):
        m3url = aResult[1][0]
        if m3url.startswith('//'):
			m3url = 'http:' + m3url 	
        oRequest = cRequestHandler(m3url)
        sHtmlContent = oRequest.request()
    #recup du lien mp4
    sPattern = 'src: "([^<]+)",'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        
        sUrl = str(aResult[1][0])
        if sUrl.startswith('//'):
			sUrl = 'http:' + sUrl 
                 
        #on lance video directement
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setTitle(sMovieTitle)
        oGuiElement.setMediaUrl(sUrl)
        oGuiElement.setThumbnail(sThumbnail)

        oPlayer = cPlayer()
        oPlayer.clearPlayList()
        oPlayer.addItemToPlaylist(oGuiElement)
        oPlayer.startPlayer()
        return
    
    else:
        return

    oGui.setEndOfDirectory()	