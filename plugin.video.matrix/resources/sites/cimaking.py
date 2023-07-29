# -*- coding: utf-8 -*-
#############################################################
# Yonn1981 https://github.com/Yonn1981/Repo
#############################################################

import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.util import cUtil, Unquote

ADDON = addon()
icons = ADDON.getSetting('defaultIcons')
SITE_IDENTIFIER = 'cimaking'
SITE_NAME = 'CimaKing'
SITE_DESC = 'arabic vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

UA = 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1'


MOVIE_EN = (URL_MAIN + '/category/%D8%A7%D9%81%D9%84%D8%A7%D9%85/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%A7%D8%AC%D9%86%D8%A8%D9%89/page/0/', 'showMovies')
MOVIE_HI = (URL_MAIN + '/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d9%87%d9%86%d8%af%d9%89/', 'showMovies')
KID_MOVIES = (URL_MAIN + '/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d9%83%d8%a7%d8%b1%d8%aa%d9%88%d9%86/', 'showMovies')
SERIE_ASIA = (URL_MAIN + '/category/مسلسلات-series/مسلسلات-اسيوية/', 'showSeries')
SERIE_HEND = (URL_MAIN + '/category/مسلسلات-series/مسلسلات-هندى/', 'showSeries')
SERIE_TR = (URL_MAIN + '/category/مسلسلات-series/مسلسلات-تركي/', 'showSeries')
SERIE_EN = (URL_MAIN + '/category/مسلسلات-series/مسلسلات-اجنبي/', 'showSeries')

RAMADAN_SERIES = (URL_MAIN + '/category/مسلسلات-series/مسلسلات-رمضان/', 'showSeries')

URL_SEARCH_MOVIES = (URL_MAIN + '/?s=%D9%81%D9%84%D9%85+', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '/?s=%D9%85%D8%B3%D9%84%D8%B3%D9%84+', 'showSeries')
FUNCTION_SEARCH = 'showMovies'
	
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'SEARCH_MOVIES', icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', 'SEARCH_SERIES', icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', RAMADAN_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'رمضان', icons + '/Ramadan.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', icons + '/Movies.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', icons + '/Hindi.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', icons + '/Kids.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', icons + '/TVShows.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أسيوية', icons + '/Asian.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', icons + '/Turkish.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات هندية', icons + '/Hindi.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/?s=%D9%81%D9%84%D9%85+'+sSearchText
        if 'مسلسل' in sUrl or 'موسم' in sUrl:
            showSeries(sUrl)
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  
    
def showSeriesSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/?s=%D9%85%D8%B3%D9%84%D8%B3%D9%84+'+sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return  

 
def showMovies(sSearch = ''):
    import requests
    oGui = cGui()
    if sSearch:
      sUrl = sSearch.replace(' ', '+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')



    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 # ([^<]+) .+? (.+?)
    sPattern = '<div class="BlockItem"><a href="([^<]+)">.+?data-src="([^"]+)".+?<h2>(.+?)</h2>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[2].replace("تحميل و فيلم","").replace("تحميل ومشاهدة","").replace("ومشاهدة","").replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("برنامج","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("مدبلج","[arabic]").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("بجودة عالية","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","").replace("للعربية","").replace("وتحميل","").replace("مباشر","").replace("تحميل","").replace("الاجنبى","").replace("ال ","").replace("الاجنبي","").replace("الغموض والدراما","").replace("التشويق والحركة","").replace("الدراما","").replace("بجودة","").replace("الحركة والمخيف","")
            siteUrl = aEntry[0]
            sThumb = aEntry[1]
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
               sYear = str(m.group(0))
               sTitle = sTitle.replace(sYear,'')

            
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addTV(SITE_IDENTIFIER, 'showServer', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

        progress_.VSclose(progress_)
 
    if not sSearch:

        oGui.setEndOfDirectory()  

 
def showSeries(sSearch = ''):
    import requests
    oGui = cGui()
    if sSearch:
      sUrl = sSearch.replace(' ', '+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')



    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 # ([^<]+) .+?
    sPattern = '<div class="BlockItem"><a href="([^<]+)">.+?data-src="([^"]+)".+?<h2>(.+?)</h2>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    itemsList = []
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[2].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("مسلسل","").replace("Web-dl","").replace("بجودة","").replace("اونلاين","").replace("بجوده","").replace("كامل","").replace("والأخيره","").replace("و الأخيرة","").replace("والأخيرة","").replace("والاخيرة","").replace("Full Episodes","").replace("وتحميل","").replace("شاهد","")
            siteUrl = aEntry[0]
            sThumb = aEntry[1]
            sTitle = sTitle.split('جميع حلقات :')[-1].replace("الموسم","S").replace("موسم","S").replace("S "," S")
            sDesc = ''
            sYear = ''
            sTitle = sTitle.replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").split('الحلقة')[0].replace("العاشر","10").replace("الحادي عشر","11").replace("الثاني عشر","12").replace("الثالث عشر","13").replace("الرابع عشر","14").replace("الخامس عشر","15").replace("السادس عشر","16").replace("السابع عشر","17").replace("الثامن عشر","18").replace("التاسع عشر","19").replace("العشرون","20").replace("الحادي و العشرون","21").replace("الثاني و العشرون","22").replace("الثالث و العشرون","23").replace("الرابع والعشرون","24").replace("الخامس و العشرون","25").replace("السادس والعشرون","26").replace("السابع والعشرون","27").replace("الثامن والعشرون","28").replace("التاسع والعشرون","29").replace("الموسم الثلاثون","30").replace("الحادي و الثلاثون","31").replace("الثاني والثلاثون","32").replace("الاول","1").replace("الثاني","2").replace("الثانى","2").replace("الثالث","3").replace("الثالث","3").replace("الرابع","4").replace("الخامس","5").replace("السادس","6").replace("السابع","7").replace("الثامن","8").replace("التاسع","9").replace(" : ", "")
            
            if sTitle not in itemsList:
                itemsList.append(sTitle)

                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sYear', sYear)
                oOutputParameterHandler.addParameter('sDesc', sDesc)

                oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
        progress_.VSclose(progress_)            
        oGui.setEndOfDirectory()  


def showSeasons():
	oGui = cGui()
    
	oInputParameterHandler = cInputParameterHandler()
	sUrl = oInputParameterHandler.getValue('siteUrl')
	sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
	sThumb = oInputParameterHandler.getValue('sThumb')
 
	oRequestHandler = cRequestHandler(sUrl)
	sHtmlContent = oRequestHandler.request()


    # .+? ([^<]+)
	sPattern = '<a class="ipc-metadata.+?href="([^"]+)" aria-label="([^"]+)'

	oParser = cParser()
	aResult = oParser.parse(sHtmlContent, sPattern)
		
	if aResult[0]:
		oOutputParameterHandler = cOutputParameterHandler()
		for aEntry in aResult[1]:
 
			sTitle = aEntry[1].replace("الموسم"," S").replace("موسم","S").replace("الأول"," S1").replace("S "," S")
			siteUrl = aEntry[0]
			sThumb = ''
			sDesc = ''
			
			oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
			oOutputParameterHandler.addParameter('sThumb', sThumb)
			oGui.addSeason(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

	else:

    # (.+?) .+? ([^<]+)
		sPattern = '<a href="([^"]+)" title="([^"]+).+?<div class="ipc-inline-list__item">(.+?)</div>'

		oParser = cParser()
		aResult = oParser.parse(sHtmlContent, sPattern)
    
		if aResult[0] is True:
			oOutputParameterHandler = cOutputParameterHandler() 
			for aEntry in aResult[1]:
                             sEp = aEntry[1].replace("حلقة ","E")
                             sEp = sEp.replace(" ","")
                             sTitle = sMovieTitle+' '+sEp
                             siteUrl = aEntry[0]
                             sThumb = sThumb
                             sDesc = ''
                             sYear = ''

                             oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                             oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                             oOutputParameterHandler.addParameter('sThumb', sThumb)
            

 
                             oGui.addEpisode(SITE_IDENTIFIER, 'showServer', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

	oGui.setEndOfDirectory()
    
def showEps():
    import requests
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')



    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
     # (.+?) ([^<]+) .+?
    sStart = '<h2 class="title.+?">أجزاء المسلسل</h2>'
    sEnd = '<div id="isdiv" style></div>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    # (.+?) .+? ([^<]+)
    sPattern = '<a href="([^"]+)" title="([^"]+).+?<div class="ipc-inline-list__item">(.+?)</div>' 

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
 
            sEp = aEntry[1].replace("حلقة ","E")
            sEp = sEp.replace(" ","")
            sTitle = sMovieTitle+' '+sEp
            siteUrl = aEntry[0]
            sThumb = sThumb
            sDesc = ''
            sYear = ''
			


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showServer', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
               
       
    oGui.setEndOfDirectory() 
 
	
def showServer():
    oGui = cGui()
    import requests

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()

  # ([^<]+) .+?

    data = {'watch':'1'}
    s = requests.Session()
    r = s.post(sUrl,data = data)
    sHtmlContent = r.content


    sPattern = '<div class="ListDownloads">.+?href="(.+?)"' 
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
               for aEntry in aResult[1]:
        
                   url = aEntry
                   url = url.replace("moshahda","ffsff")
                   sTitle = " "
                   sThumb = sThumb
                   if url.startswith('//'):
                      url = 'http:' + url
								            
                   sHosterUrl = url
                   if 'nowvid' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
                   if 'userload' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                   if 'moshahda' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                   if 'mystream' in sHosterUrl:
                       sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN  
                 
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                      sDisplayTitle = sTitle
                      oHoster.setDisplayName(sDisplayTitle)
                      oHoster.setFileName(sMovieTitle)
                      cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)


    oParser = cParser()   
    sPattern = '<link rel="shortlink" href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    
    if aResult[0]:
        sId = aResult[1][0]
        sId = sId.split("p=")[1]
     # (.+?) ([^<]+) .+?
    oParser = cParser()
    sPattern = 'data-server="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)


   
    if aResult[0]:
        for aEntry in aResult[1]:

            sTitle = 'server '
            siteUrl = URL_MAIN + 'wp-content/themes/cimaking/server.php?action=GetServer&ts=1&p='+sId+'&i='+aEntry+'&type=Last'
            oRequestHandler = cRequestHandler(siteUrl)
            sHtmlContent = oRequestHandler.request()
            sPattern = '<iframe src="(.+?)" scrolling'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                for aEntry in aResult[1]:
            
                    url = aEntry
                    sTitle = " "
                    if url.startswith('//'):
                       url = 'http:' + url
            
                    sHosterUrl = url
                    if 'userload' in sHosterUrl:
                        sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                    if 'moshahda' in sHosterUrl:
                        sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                    if 'mystream' in sHosterUrl:
                        sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                    if 'watchservice' in sHosterUrl:
                        oRequestHandler = cRequestHandler(sHosterUrl)                        
                        sHtmlContent = oRequestHandler.request()
                        sPattern = 'src="([^"]+)'
                        oParser = cParser()
                        aResult = oParser.parse(sHtmlContent, sPattern)

                        if aResult[0]:
                            for aEntry in aResult[1]:            
                                sHosterUrl = aEntry
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if oHoster:
                       sDisplayTitle = sTitle
                       oHoster.setDisplayName(sDisplayTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
       
      
    oGui.setEndOfDirectory()  

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<link rel="canonical" href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:
            sLink = aEntry.split('/page')[0]
            sPage = aEntry.split('/page/')[-1].replace('/','')
            sNext = '2'
            if '2' in sPage:
                        sNext = '3'
            if '3' in sPage:
                        sNext = '4'
            if '4' in sPage:
                        sNext = '5'
            if '5' in sPage:
                        sNext = '6'
            if '6' in sPage:
                        sNext = '7'

            NewLink = sLink+'/page/'+sNext+'/'
        return NewLink

    return False