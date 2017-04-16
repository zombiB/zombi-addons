#-*- coding: utf-8 -*-
#zombi
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
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

MOVIE_ANIME = ('https://cima4u.tv/category/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D9%83%D8%B1%D8%AA%D9%88%D9%86-movies-anime-cartoon/', 'showMovies')
SERIE_TR = ('https://cima4u.tv/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-series/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%AA%D8%B1%D9%83%D9%8A%D8%A9-series-turkish/', 'showSeries')

SERIE_ASIA = ('https://cima4u.tv/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-series/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%A7%D8%B3%D9%8A%D9%88%D9%8A%D8%A9-series-asian/', 'showSeries')
SERIE_EN = ('https://cima4u.tv/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-series/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%A7%D8%AC%D9%86%D8%A8%D9%8A-series-english/', 'showSeries')
SERIE_AR = ('https://cima4u.tv/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-series/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9-arabic-series/', 'showSeries')
ANIM_NEWS = ('https://cima4u.tv/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-series/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D9%83%D8%B1%D8%AA%D9%88%D9%86-anime-series/', 'showSeries')


SPORT_NEWS = ('https://cima4u.tv/category/%D9%85%D8%B5%D8%A7%D8%B1%D8%B9%D8%A9-%D8%AD%D8%B1%D8%A9-wwe/', 'showMovies')
REPLAYTV_NEWS = ('https://cima4u.tv/category/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-series/%D8%A8%D8%B1%D8%A7%D9%85%D8%AC-%D8%AA%D9%84%D9%8A%D9%81%D8%B2%D9%8A%D9%88%D9%86%D9%8A%D8%A9-tv-shows/', 'showSeries')
URL_SEARCH = ('https://cima4u.tv/?s=', 'showMovies')
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
 

    sPattern = '<div class="block"><a href="(.+?)"><div class="image"><div class="img1" style="background-image:url(.+?);"></div>.+?<div class="boxtitle">(.+?)</div><div class="boxdetil">(.+?)</div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
 
            sTitle = str(aEntry[2]).replace("&#8217;","'")
            siteUrl = str(aEntry[0])
            sThumbnail = str(aEntry[1]).replace("(","").replace(")","")
            sInfo = str(aEntry[3])


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showMoviesLinks', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)

        cConfig().finishDialog(dialog)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
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
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
 
            sTitle = aEntry[2].replace("&#8217;","'")
            siteUrl = str(aEntry[0])
            sThumbnail = str(aEntry[1]).replace("(","").replace(")","")
            sInfo = str(aEntry[3])


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showSeriesLinks', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)

        cConfig().finishDialog(dialog)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()

def showMoviesLinks():
    
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #print sUrl
   
    oParser = cParser()
    
    #Recuperation infos
    sNote = ''
    sCom = ''
    sQua = ''

    sPattern = '<div class="views"><i class="fa fa-eye"></i>(.+?)</div>.+?<div class="storyContent"><h2>القصة : </h2>(.+?)</div>.+?<span>الجودة :</span> <a href="https://cima4u.tv/quality/.+?/">(.+?)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        sNote = aResult[1][0][0]
        sCom = aResult[1][0][1]
        sQua = aResult[1][0][2]
        sCom = cUtil().removeHtmlTags(sCom)
    if (sNote):
        oGui.addText(SITE_IDENTIFIER,'  : عدد المشاهدات'+'[COLOR yellow]'+ str(sNote) + ' [/COLOR]')
    if (sQua):
        oGui.addText(SITE_IDENTIFIER,'  : الجودة'+'[COLOR yellow]'+ str(sQua) + ' [/COLOR]')

    
    
    #Affichage du menu  
    oGui.addText(SITE_IDENTIFIER,'[COLOR olive]_______________[/COLOR]')

    sPattern = '<div class="modalTrailerClose"></div>.+?<iframe.+?src="(.+?)" frameborder'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            if aEntry:
                 sHosterUrl = str(aEntry)
                 sMovieTitle2 = 'trailer'
                 oHoster = cHosterGui().checkHoster(sHosterUrl)
                 if (oHoster != False):
                     oHoster.setDisplayName(sMovieTitle2)
                     oHoster.setFileName(sMovieTitle2)
                     cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

    
    
    #Affichage du menu  
    oGui.addText(SITE_IDENTIFIER,'[COLOR olive]_______________[/COLOR]')



    #data-src="([^<]+)"data-src="" data-load="no"
    sPattern = '<meta itemprop="embedURL" content="([^<]+)" />'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = 'شاهد من هنا'
            sUrl= aEntry
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            if 'Episode' in sUrl:
                oGui.addMovie(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumbnail, sCom, oOutputParameterHandler) 
            else:
				oGui.addMovie(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumbnail, sCom, oOutputParameterHandler)             
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()		
def showSeriesLinks():
    
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #print sUrl
   
    oParser = cParser()
    
    #Recuperation infos
    sNote = ''
    sCom = ''
    sQua = ''

    sPattern = '<div class="views"><i class="fa fa-eye"></i>(.+?)</div>.+?<div class="storyContent"><h2>القصة : </h2>(.+?)</div>.+?<span>الجودة :</span> <a href="https://cima4u.tv/quality/.+?/">(.+?)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        sNote = aResult[1][0][0]
        sCom = aResult[1][0][1]
        sQua = aResult[1][0][2]
        sCom = cUtil().removeHtmlTags(sCom)
    if (sNote):
        oGui.addText(SITE_IDENTIFIER,'  : عدد المشاهدات'+'[COLOR yellow]'+ str(sNote) + '[/COLOR]')
    if (sQua):
        oGui.addText(SITE_IDENTIFIER,'  : الجودة'+'[COLOR yellow]'+ str(sQua) + '[/COLOR]')

    
    
    #Affichage du menu  
    oGui.addText(SITE_IDENTIFIER,'[COLOR olive]_______________[/COLOR]')

    sPattern = '<div class="modalTrailerClose"></div>.+?<iframe.+?src="(.+?)" frameborder'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            if aEntry:
                 sHosterUrl = str(aEntry)
                 sMovieTitle2 = 'trailer'
                 oHoster = cHosterGui().checkHoster(sHosterUrl)
                 if (oHoster != False):
                     oHoster.setDisplayName(sMovieTitle2)
                     oHoster.setFileName(sMovieTitle2)
                     cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

    
    
    #Affichage du menu  
    oGui.addText(SITE_IDENTIFIER,'[COLOR olive]_______________[/COLOR]')



    #data-src="([^<]+)"data-src="" data-load="no"
    sPattern = '<meta itemprop="embedURL" content="([^<]+)" />'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = 'شاهد من هنا'
            sUrl= aEntry
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oGui.addMovie(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumbnail, sCom, oOutputParameterHandler)             
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
def showEpisodes():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 
    sPattern = '<div class="col-md-2" style="padding: 5px; text-align: center;"><a href="(.+?)" class=".+?"><span class="icon-desktop"></span>(.+?)</a></div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
 
            sTitle = aEntry[1]
            siteUrl = str(aEntry[0])
            sThumbnail = str(sThumbnail)
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addMisc(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumbnail, '', oOutputParameterHandler)
        
        cConfig().finishDialog(dialog)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
	

 
       
 
 
 
def __checkForNextPage(sHtmlContent):
    sPattern = '</li><li><a href="([^<]+)" >[^<]+&laquo;</a></li>'
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if (aResult[0] == True):
        #print aResult[1][0]
        return aResult[1][0]

    return False
  
def showEps():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #print sUrl
    


    sPage='0'

    sPattern = 'a href="" data-link="([^<]+)" class=".+?"><img.+?src=".+?" width="40" height="40" alt="" />([^<]+)</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

   
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            sPage = str(aEntry[0])
            sTitle = 'server '+':'+ aEntry[1]
            siteUrl = 'http://live.cima4u.tv/structure/server.php?id='+sPage


            #print siteUrl 
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            

 
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, '', oOutputParameterHandler)
 
        cConfig().finishDialog(dialog)
       
    oGui.setEndOfDirectory()
    



def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    #sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/plugins/like.php','').replace('<iframe src="http://www.facebook.com/plugins/likebox.php','')
               
        
    sPattern = '<iframe.+?src="(.+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            url = str(aEntry)
            if url.startswith('//'):
                url = 'http:' + url
            
            sHosterUrl = url
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				

        cConfig().finishDialog(dialog) 
                
    oGui.setEndOfDirectory()