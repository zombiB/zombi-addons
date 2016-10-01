#-*- coding: utf-8 -*-
#Venom.
#zombi(@zombigeek)

#Cloudflare protection
#https://raw.githubusercontent.com/daniel-lundin/dreamfilm-xbmc/master/cloudflare.py
#https://gist.github.com/Rainbowed/8917670

from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.config import cConfig
import re, urllib, urllib2

SITE_IDENTIFIER = 'akoam_com'
SITE_NAME = 'akoam.com'
SITE_DESC = 'vod arab'

URL_MAIN = 'http://www.akoam.com/'


MOVIE_AR = ('http://akoam.com/cat/155/%D8%A7%D9%84%D8%A3%D9%81%D9%84%D8%A7%D9%85-%D8%A7%D9%84%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9', 'showMovies')
MOVIE_EN = ('http://akoam.com/cat/156/%D8%A7%D9%84%D8%A3%D9%81%D9%84%D8%A7%D9%85-%D8%A7%D9%84%D8%A7%D8%AC%D9%86%D8%A8%D9%8A%D8%A9', 'showMovies')
MOVIE_HI = ('http://akoam.com/cat/168/%D8%A7%D9%84%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%A7%D9%84%D9%87%D9%86%D8%AF%D9%8A%D8%A9', 'showMovies')
MOVIE_ANIME = ('http://akoam.com/cat/179/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%A7%D9%84%D8%A7%D9%86%D9%85%D9%8A-%D8%A7%D9%84%D9%85%D8%AF%D8%A8%D9%84%D8%AC%D8%A9', 'showMovies')


SERIE_AR = ('http://akoam.com/cat/80/%D8%A7%D9%84%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%A7%D9%84%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9', 'showMovies')
SERIE_EN = ('http://akoam.com/cat/166/%D8%A7%D9%84%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%A7%D9%84%D8%A7%D8%AC%D9%86%D8%A8%D9%8A%D8%A9', 'showMovies')

SPORT_NEWS = ('http://akoam.com/cat/87/%D8%B1%D9%8A%D8%A7%D8%B6%D8%A9', 'showMovies')

DOC_NEWS = ('http://akoam.com/cat/94/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D9%88%D8%AB%D8%A7%D8%A6%D9%82%D9%8A%D8%A9', 'showMovies')

ANIM_NEWS = ('http://akoam.com/cat/178/%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%A7%D9%84%D8%A7%D9%86%D9%85%D9%8A', 'showMovies')

REPLAYTV_NEWS = ('http://akoam.com/cat/81/%D8%A7%D9%84%D8%A8%D8%B1%D8%A7%D9%85%D8%AC-%D8%A7%D9%84%D8%AA%D9%84%D9%81%D8%B2%D9%8A%D9%88%D9%86%D9%8A%D8%A9', 'showMovies')


URL_SEARCH = ('http://akoam.com/search/', 'showMovies')
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
        sUrl = 'http://akoam.com/search/'+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

      
    


def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
      #correction
      sUrl = sUrl.replace(URL_SEARCH[0],'')
      sUrl = URL_SEARCH[0] + urllib.quote(sUrl)

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
   
    #print sUrl
     
    #oRequestHandler = cRequestHandler(sUrl)
    #sHtmlContent = oRequestHandler.request()

    headers = {'User-Agent' : 'Mozilla 5.10'}
    request = urllib2.Request(sUrl,None,headers)
      
    try: 
        reponse = urllib2.urlopen(request)
    except urllib2.HTTPError, e:
        print e.read()
        print e.reason
      
    sHtmlContent = reponse.read()
    reponse.close()
    
    #fh = open('c:\\test.txt', "w")
    ##fh.write(sHtmlContent)
    #<a href="(.+?)">.+?<img src="(.+?)"
	
    
    sPattern = 'subject_box shape"><a href="([^<]+)">.+?<img src="([^<]+)" alt="Ø§Ø³Ù… Ø§Ù„Ù…ÙˆØ¶ÙˆØ¹"><div class="subject_title "><h3>([^<]+)</h3><span class="desc">([^<]+)</span>'


    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == False):
        oGui.addNone(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sTitle = aEntry[2]
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[1]))
            if 'hd-arab' in sUrl:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', aEntry[1], '', oOutputParameterHandler) 
            else:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', cUtil().DecoTitle(sTitle),'', aEntry[1], aEntry[3], oOutputParameterHandler)         
    
        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def showSeries():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

        
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    #sHtmlContent = sHtmlContent.replace('<strong>Téléchargement VOSTFR','').replace('<strong>Téléchargement VF','').replace('<strong>Téléchargement','')
 
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #<a class='sub_btn show' target='(.+?)' href='(.+?)'>

    sPattern = "style='background-image: url(.+?);'>.+?target='_blank'.+?href='(.+?)'>"

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    #print aResult
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = sMovieTitle
            sTitle = cUtil().DecoTitle(sTitle)
            sPic = aEntry[0].replace('(','').replace(')','')
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sPic, aEntry[0], oOutputParameterHandler)            
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = "</li><li class='pagination_next'><a href='(.+?)'"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False
	
def showEpisode():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
   
    oParser = cParser()
    sPattern = '<h2 class="sub_epsiode_title">(.+?)</h2>'
    sPattern = sPattern + '|' + "style='background-image: url(.+?);'>.+?target='_blank'.+?href='(.+?)'>"
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    Saison = '0'
   
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
       
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
                        
            if aEntry[0]:
                Saison = str(aEntry[0])
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addMisc(SITE_IDENTIFIER, 'showEpisode', '[COLOR red]'+ aEntry[0] + '[/COLOR]', 'series.png', sThumbnail, '', oOutputParameterHandler)
            else:
                sTitle = sMovieTitle 
                sDisplayTitle = cUtil().DecoTitle(sTitle)
                sPic = aEntry[1].replace('(','').replace(')','')
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', aEntry[2])
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sPic, '', oOutputParameterHandler)
 
        cConfig().finishDialog(dialog)
           
    oGui.setEndOfDirectory() 

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #sHtmlContent = sHtmlContent.replace('facebook','<>')
    
    sPattern = '<iframe.+?src="(.+?)".+?</iframe>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    print aResult
     
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sHosterUrl = str(aEntry)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)         
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
