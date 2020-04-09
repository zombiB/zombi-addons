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
import urllib2,urllib,re
import unicodedata
 
SITE_IDENTIFIER = 'cartoonrbi'
SITE_NAME = 'cartoon3rbi'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'http://www.cartoon3rbi.net/'


KID_MOVIES = ('http://www.cartoon3rbi.net/films.html', 'showMovies')
KID_CARTOON = ('https://www.cartoon3rbi.net/cartoon2549.html', 'showSeries')


URL_SEARCH = ('http://www.cartoon3rbi.net/search.html', 'showSeries')
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
        sUrl = 'http://www.cartoon3rbi.net/search.html'+sSearchText
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
 
#([^<]+)(.+?)
    sPattern = '<div class="cartoon_cat_pic"><a href="([^<]+)" title="([^<]+)"><img src="([^<]+)" alt'

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
            siteUrl = URL_MAIN+str(aEntry[0])
            sThumbnail = aEntry[2]
            sInfo = ""


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
		
def __checkForNextPage(sHtmlContent):
    sPattern = "<a href='([^<]+)'>«"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        aResult = URL_MAIN+aResult[1][0]
        return aResult

    return False	
	
def __checkForNextPageEp(sHtmlContent):
    sPattern = "<a href='([^<]+)'>«"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        aResult = URL_MAIN+aResult[1][0]
        return aResult

    return False		
 
def showSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 
    sPattern = '<li><a href="([^<]+)">([^<]+)</a></li'

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
            siteUrl = URL_MAIN+str(aEntry[0])
            sThumbnail = ""
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            oGui.addMovie(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumbnail, aEntry[1], oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
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

    sPattern = '<div class="cartoon_eps_pic"><a href="(.+?)" title="(.+?)"><span class="copy_right"></span><span class="playtime">(.+?)</span><img src="(.+?)" alt'

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
            siteUrl = URL_MAIN+str(aEntry[0])
            sThumbnail = URL_MAIN+str(aEntry[3])

 
            #print sUrl
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            

 
            oGui.addMovie(SITE_IDENTIFIER, 'showLink', aEntry[1], '', sThumbnail, aEntry[2], oOutputParameterHandler)
 
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPageEp(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showEps', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()
       
  
def showLink():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #print sUrl
   
    
    #Recuperation infos
    sname = '0'

    sPage='0'

    #(.+?)([^<]+)
    sPattern = "&p=(.+?)',"

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        sname = aResult[1][0]

    sPattern = "server_ch([^<]+),'(.+?)'"

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent.replace('\n',''))
    #fh.close()

    #print sPage
   
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break


            #https://www.cartoon3rbi.net/plugins/servers.php?server=7&url=x5lwx42&p=2549&funame=slam_dunk_s1_02.mp4


            sErver = aEntry[0].replace("(","")


            sPage = aEntry[1]
            #print sErver
            siteUrl = 'https://www.cartoon3rbi.net/plugins/servers.php?server='+sErver+'&url='+sPage+sname
            sTitle = 'server '+':'+sErver



            #print siteUrl 
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            

 
            oGui.addMovie(SITE_IDENTIFIER, 'showLinkS', sTitle, '', sThumbnail, "", oOutputParameterHandler)
 
        progress_.VSclose(progress_) 
               
        
    sPattern = '<iframe.+?src="([^<]+)" frameborder'
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
            url = url.replace('?pli=1#t=1','').replace('https://docs.google.com','https://drive.google.com') 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False): 
				   sDisplayTitle = sTitle
				   oHoster.setDisplayName(sDisplayTitle)
				   oHoster.setFileName(sTitle)
				   cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				

        progress_.VSclose(progress_) 
       
    oGui.setEndOfDirectory()
    
    
 
def showLinkS():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    #(.+?)([^<]+)
    sPattern = '<iframe.+?src="([^<]+)" frameborder'
    
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
 
            sTitle = 'click here'
            siteUrl = aEntry
            sInfo = ""
 
            #print sUrl
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
	    oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)        
           
 
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
    #sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/plugins/like.php','').replace('<iframe src="http://www.facebook.com/plugins/likebox.php','')(.+?)
               
        
    sPattern = '<iframe allowfullscreen="true" src="(.+?)" frameborder'
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
            url = url.replace('?pli=1#t=1','').replace('https://docs.google.com','https://drive.google.com') 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False): 
				   sDisplayTitle = sTitle
				   oHoster.setDisplayName(sDisplayTitle)
				   oHoster.setFileName(sTitle)
				   cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				

        progress_.VSclose(progress_) 
                
    oGui.setEndOfDirectory()