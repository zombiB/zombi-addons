# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager
from resources.lib.parser import cParser
 
SITE_IDENTIFIER = 'cartoonrbi'
SITE_NAME = 'CartoonArbi'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

KID_MOVIES = (URL_MAIN + '/films.html', 'showMovies')
KID_CARTOON = (URL_MAIN + '/cartoon2549.html', 'showSeries')

 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', 'crtoon.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', KID_CARTOON[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات كرتون', 'crtoon.png', oOutputParameterHandler)    
            
    oGui.setEndOfDirectory()

   
def showMovies(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 
#([^<]+)(.+?)
    sPattern = '<div class="cartoon_cat_pic"><a href="([^<]+)" title="([^<]+)"><img src="([^<]+)" alt'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1]
            siteUrl = URL_MAIN+'/'+aEntry[0]
            sThumb = aEntry[2]
            sDesc = ""

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMovie(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage != False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
		
def __checkForNextPage(sHtmlContent):
    sPattern = "<a href='([^<]+)'>«"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        aResult = URL_MAIN+'/'+aResult[1][0]
        return aResult

    return False	
	
def __checkForNextPageEp(sHtmlContent):
    sPattern = "<a href='([^<]+)'>«"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        aResult = URL_MAIN+'/'+aResult[1][0]
        return aResult

    return False		
 
def showSeries(sSearch = ''):
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
 
    sPattern = '<li><a href="([^<]+)">([^<]+)</a></li'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1].replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الجزء","الموسم").replace("الموسم","S").replace("موسم","S").replace("S ","S")
            siteUrl = URL_MAIN+'/'+aEntry[0]
            sThumb = ""
			


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addTV(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumb, '', oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage != False:
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
    sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="cartoon_eps_pic"><a href="(.+?)" title="(.+?)"><span class="copy_right"></span><span class="playtime">(.+?)</span><img src="(.+?)" alt'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

   
    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            siteUrl = aEntry[0]
            sThumb = aEntry[3]
            sTitle = aEntry[1].replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("موسم","S").replace("S ","S").replace("الحلقة "," E").replace("حلقة "," E")

 
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            

 
            oGui.addEpisode(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, '', oOutputParameterHandler)
 
 
        sNextPage = __checkForNextPageEp(sHtmlContent)
        if sNextPage != False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showEps', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()
       
def showLink():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sUrl = sUrl.replace("cartoon","watch-")
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #Recuperation infos
    sname = '0'

    sPage='0'

    # (.+?) ([^<]+)
    sPattern = '&id=(.+?)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        sname = aResult[1][0]

    sPattern = "server_ch([^<]+),'(.+?)'"

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
   
    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            sErver = aEntry[0].replace("(","")
            sPage = aEntry[1]
            siteUrl = URL_MAIN + '/plugins/server'+sErver+'/embed.php?url='+sPage+'&id='+sname
			
            oRequestHandler = cRequestHandler(siteUrl)
            oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
            oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
            oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
            oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
            sData = oRequestHandler.request()
   
            sPattern = 'src="(.+?)"'
            oParser = cParser()
            aResult = oParser.parse(sData, sPattern)
	
            if aResult[0] is True:
               for aEntry in aResult[1]:
                   url = str(aEntry).replace('preview?pli=1#t=1','').replace('https://docs.google.com','https://drive.google.com')  
                   sTitle = " "
                   sThumb = sThumb
                   if '.m3u8' in url:
                      url2 = url.split('=') 
                      url = url2[1].replace("&token","")
                   if url.startswith('//'):
                      url = 'http:' + url
								            
                   sHosterUrl = url
                   if 'userload' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                   if 'moshahda' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                   if '.m3u8' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
                   if 'mystream' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN    
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster != False:
                      oHoster.setDisplayName(sMovieTitle)
                      oHoster.setFileName(sMovieTitle)
                      cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
       
    oGui.setEndOfDirectory()