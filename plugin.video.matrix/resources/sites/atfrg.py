#-*- coding: utf-8 -*-
#zombi.(@geekzombi)
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.player import cPlayer
from resources.lib.comaddon import dialog
import xbmcgui
import urllib2,urllib,re
import unicodedata
 
SITE_IDENTIFIER = 'atfrg'
SITE_NAME = 'atfrg'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'https://atfrg.online'


MOVIE_EN = ('https://atfrg.online/movies', 'showMovies')
SERIE_EN = ('https://atfrg.online/serieses', 'showSeries')

URL_SEARCH = ('', 'showMoviesSearch')
FUNCTION_SEARCH = 'showSearch'
 
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
        sUrl = 'https://w2.akoam.net/search/'+sSearchText
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
    import requests,re
    S = requests.Session()
    r = S.get(sUrl).content
    rgx = '''__typename:d}},"(.+?):.+?,title:"(.+?)",posters:.+?,__typename:.+?}},"Image:.+?,path:"(.+?)",size'''
    sHtmlContent = re.findall(rgx,r)
    if sHtmlContent:
        total = len(sHtmlContent[1])
        progress_ = progress().VScreate(SITE_NAME)
        for x,y,z in sHtmlContent:
			progress_.VSupdate(progress_, total)
			if progress_.iscanceled():
				break
			if x=="TvSeries" or x=="Image":u='series'
			else:u="movie"
			if not "movie" in u:
				continue
			sTitle = y
			siteUrl = "https://atfrg.online/"+u+"/"+y
			sThumbnail = z.replace("\u002F","/")
			sInfo = ""


			oOutputParameterHandler = cOutputParameterHandler()
			oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
			oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

			oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
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
    import requests,re
    S = requests.Session()
    r = S.get(sUrl).content
    rgx = ''',__typename:c}},"(.+?):.+?,title:"(.+?)",posters:.+?,id:"Image:.+?,path:"(.+?)",size:e'''
    sHtmlContent = re.findall(rgx,r)
    if sHtmlContent:
        total = len(sHtmlContent[1])
        progress_ = progress().VScreate(SITE_NAME)
        for x,y,z in sHtmlContent:
			progress_.VSupdate(progress_, total)
			if progress_.iscanceled():
				break
				
			if x=="TvSeries" or x=="Image":u='series'
			else:u="movie"
			if "movie" in u:
				continue
			sTitle = y
			siteUrl = "https://atfrg.online/"+u+"/"+y
			sThumbnail = z.replace("\u002F","/")
			sInfo = ""


			oOutputParameterHandler = cOutputParameterHandler()
			oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
			oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

			oGui.addMovie(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
	progress_.VSclose(progress_)
 
	if not sSearch:
		oGui.setEndOfDirectory()
 
      # (.+?) ([^<]+) .+?
 
def __checkForNextPage(sHtmlContent):
    sPattern = "</li><li class='pagination_next'><a href='([^<]+)' class='ako-arrow ako-left-arrow'></a>"
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if (aResult[0] == True):
        #print aResult[1][0]
        return aResult[1][0]

    return False

  
def showSeasons():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()
    # .+? ([^<]+)
    sPattern = '<div class="swiper-slide"><a href="([^<]+)" data.+?<img data-src="([^<]+)" alt="([^<]+)" data'
    
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
 
            sTitle = aEntry[2]
            siteUrl = URL_MAIN + str(aEntry[0])
            sThumbnail = aEntry[1]
            sInfo = ""
 
            #print sUrl
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            

 
            oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
 
        progress_.VSclose(progress_)
    # .+? ([^<]+)
    sPattern = '<div class="swiper-slide col-md-2 col-6" style="min-width:130px;margin-bottom:1rem;"><a href="([^<]+)" style=.+?<img data-src="([^<]+)" alt="([^<]+)" data'
    
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
 
            sTitle = aEntry[2]
            sTitle = sMovieTitle+' '+sTitle
            siteUrl = URL_MAIN + str(aEntry[0])
            sThumbnail = aEntry[1]
            sInfo = ""
 
            #print sUrl
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            

 
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
 
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

    oParser = cParser()
    #recup du lien mp4
    sPattern = 'src="([^<]+)" type="video/mp4" size="([^<]+)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    api_call = False
    
    if (aResult[0] == True):
        
        sUrl=[]
        
        qua=[]
        for i in aResult[1]:
			sUrl.append(i[0].replace("[","%5B").replace("]","%5D").replace("+","%20"))
			qua.append(str(i[1]))
 
        api_call  = dialog().VSselectqual(qua, sUrl)
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setTitle(sMovieTitle)
        oGuiElement.setMediaUrl(api_call)
        oGuiElement.setThumbnail(sThumbnail)

        oPlayer = cPlayer()
        oPlayer.clearPlayList()
        oPlayer.addItemToPlaylist(oGuiElement)
        oPlayer.startPlayer()
        return
    
    else:
        return

    oGui.setEndOfDirectory()