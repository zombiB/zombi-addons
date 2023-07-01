# -*- coding: utf-8 -*-
#############################################################
# Yonn1981 https://github.com/Yonn1981/Repo
#############################################################

import requests,re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog, siteManager

SITE_IDENTIFIER = 'egybest'
SITE_NAME = 'EgyBest'
SITE_DESC = 'arabic vod'
  
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

RAMADAN_SERIES = (URL_MAIN + '/category/مسلسلات/مسلسلات-رمضان-2023/', 'showSeries')

MOVIE_EN = (URL_MAIN + 'movies?lang=الإنجليزية', 'showMovies')
MOVIE_AR = (URL_MAIN + 'movies?lang=العربية', 'showMovies')
MOVIE_HI = (URL_MAIN + 'movies?lang=الهندية', 'showMovies')
MOVIE_ASIAN = (URL_MAIN + 'movies?lang=الكورية', 'showMovies')
MOVIE_TURK = (URL_MAIN + 'movies?lang=التركية', 'showMovies')
KID_MOVIES = (URL_MAIN + 'movies?genre=14', 'showMovies')

SERIE_EN = (URL_MAIN + 'series?lang=الإنجليزية', 'showSeries')
SERIE_TR = (URL_MAIN + 'series?lang=التركية', 'showSeries')
SERIE_AR = (URL_MAIN + 'series?lang=العربية', 'showSeries')
SERIE_ASIA = (URL_MAIN + 'series?lang=الكورية', 'showSeries')

ANIM_NEWS = (URL_MAIN + 'series?genre=40', 'showSeries')
ANIM_MOVIES = (URL_MAIN + 'movies?genre=40', 'showMovies')

URL_SEARCH = (URL_MAIN + 'search?query=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + 'search?query=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'search?query=', 'showSeries')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'SEARCH MOVIES', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', 'SEARCH SERIES', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', 'film.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عربية', 'film.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أسيوية', 'film.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية', 'film.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', 'film.png', oOutputParameterHandler) 
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', 'crtoon.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', 'mslsl.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات عربية', 'mslsl.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أسيوية', 'mslsl.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', 'mslsl.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'افلام انمي', 'anime.png', oOutputParameterHandler)
  
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات إنمي', 'anime.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

	
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + 'search?query='+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSearchSeries():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + 'search?query='+sSearchText
        showSeries(sUrl)
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
 # ([^<]+) .+?

    sPattern = '<a class="block" href="([^"]+)".+?data-src="([^"]+)".+?title="([^"]+)'

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

            if 'serie/' in aEntry[0]:
                continue 

            sTitle = aEntry[2].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            siteUrl = aEntry[0]
            sThumb = aEntry[1]
            if sThumb.startswith('//'):
                sThumb = "https:"+aEntry[1]
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
			
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPageM(sHtmlContent, sUrl)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

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

    sPattern = '<a class="block" href="([^"]+)".+?src="([^"]+)".+?title="([^"]+)'

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

            if 'movie/' in aEntry[0]:
                continue 
            
            sTitle = aEntry[2].replace("مشاهدة","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            sTitle = sTitle.replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("موسم","S").replace("S ","S").split('الحلقة')[0]
            siteUrl = aEntry[0]
            sThumb = aEntry[1]
            if sThumb.startswith('//'):
                sThumb = "https:"+aEntry[1]
            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPageS(sHtmlContent, sUrl)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        oGui.setEndOfDirectory()

def showSeasons():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
     # (.+?) ([^<]+) .+?
    sStart = '<h2 class="main-title clearfix">المواسم</h2>'
    sEnd = '</article>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a class="block" href="([^"]+)".+?data-src="([^"]+)".+?title="([^"]+)'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
 
            sTitle =  aEntry[2].replace("مشاهدة","").replace("الأخيرة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("الاخيرة","").replace("مترجم","").replace(" الحادي عشر","11").replace(" الثاني عشر","12").replace(" الثالث عشر","13").replace(" الرابع عشر","14").replace(" الخامس عشر","15").replace(" السادس عشر","16").replace(" السابع عشر","17").replace(" الثامن عشر","18").replace(" التاسع عشر","19").replace(" العشرون","20").replace(" الحادي و العشرون","21").replace(" الثاني و العشرون","22").replace(" الثالث و العشرون","23").replace(" الرابع والعشرون","24").replace(" الخامس و العشرون","25").replace(" السادس والعشرون","26").replace(" السابع والعشرون","27").replace(" الثامن والعشرون","28").replace(" التاسع والعشرون","29").replace(" الثلاثون","30").replace(" الحادي و الثلاثون","31").replace(" الثاني والثلاثون","32").replace(" الاول","1").replace(" الثاني","2").replace(" الثانى","2").replace(" الثالث","3").replace(" الرابع","4").replace(" الخامس","5").replace(" السادس","6").replace(" السابع","7").replace(" الثامن","8").replace(" التاسع","9").replace(" العاشر","10").replace("الموسم","S")
            siteUrl = aEntry[0]
            sThumb = aEntry[1]
            sDesc = ''
            if sThumb.startswith('//'):
                sThumb = "https:"+aEntry[1]
			


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
       
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
     # (.+?) ([^<]+) .+?
    sStart = '<h2 class="main-title clearfix">الحلقات</h2>'
    sEnd = '</article>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="([^"]+)">(.+?)</a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
 
            sTitle = aEntry[1].replace("الموسم","S").replace("(الاخيرة)","").split('الحلقة')[-1].replace("ى","").replace("ة","").replace("E ","E").replace(' - ', '')
            sTitle = ' E'+sTitle
            sTitle = sMovieTitle+sTitle
            siteUrl = aEntry[0].encode('utf-8').decode('utf-8')
            sThumb = sThumb
            sDesc = ''
			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler) 


    sPattern = '<a class="block" href="([^"]+)".+?data-src="([^"]+)".+?title="([^"]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
 
            sTitle = aEntry[2].replace("الموسم","S").replace("(الاخيرة)","").split('الحلقة')[-1].replace("ى","").replace("ة","").replace("E ","E").replace(' - ', '')
            sTitle = ' E'+sTitle
            sTitle = sMovieTitle+sTitle
            siteUrl = aEntry[0].encode('utf-8').decode('utf-8')
            sThumb = aEntry[1]
            sDesc = ''
			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler) 
      
    oGui.setEndOfDirectory()

 
 
def __checkForNextPageM(sHtmlContent, sUrl):
    sPattern = '<a href="([^<]+)" class="btn btn-primary btn-lg btn-block'
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0]:
        return sUrl+'&'+aResult[1][0]

    return False

def __checkForNextPageS(sHtmlContent, sUrl):
    sPattern = '<a href="([^<]+)" class="btn btn-primary btn-lg btn-block'
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0]:
        return sUrl+'&'+aResult[1][0]

    return False

def showHosters():
    oGui = cGui()
    import base64
    import requests


    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    if "الحلقة" in sUrl:
        rUrl1 = sUrl.split("/")[7]
        rUrl = sUrl.replace(rUrl1, '')
    else:
        rUrl1 = sUrl.split("/")[5]
        rUrl = sUrl.replace(rUrl1, '')

    
    oRequestHandler = cRequestHandler(sUrl)
    St=requests.Session()
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<iframe.+?src="([^"]+)'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
                    for aEntry in aResult[1]:
                        if "embed/" in aEntry:
                            url = aEntry
                            sHosterUrl = url
                            if "youtube" in sHosterUrl:
                                sTitle = 'Trailer'
                            else:
                                sTitle = sMovieTitle
                            oHoster = cHosterGui().checkHoster(sHosterUrl)
                            if oHoster:
                                sDisplayTitle = sTitle
                                oHoster.setDisplayName(sDisplayTitle)
                                oHoster.setFileName(sMovieTitle)
                                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
                                
                        if "stream/" in aEntry:
                            aurl = aEntry

                            cook = oRequestHandler.GetCookies()
                            hdr = {'Sec-Fetch-Mode' : 'navigate','Cookie' : cook,'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.58','Referer' : rUrl}
                            sHtmlContent = St.get(aurl,headers=hdr)
                            sHtmlContent = sHtmlContent.content
                            
                            sPattern = '<source src="([^"]+)".+?size="([^"]+)'
                            oParser = cParser()
                            aResult = oParser.parse(sHtmlContent, sPattern)
                            VSlog(aResult)
                            if aResult[0]:
                                for aEntry in aResult[1]:
            
                                    url = aEntry[0]
                                    qual = aEntry[1]
                                    sHosterUrl = url

                                    sTitle = ('%s  [COLOR coral](%sp)[/COLOR]') % (sMovieTitle, qual)
                                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                                    if oHoster:
                                        sDisplayTitle = sTitle
                                        oHoster.setDisplayName(sDisplayTitle)
                                        oHoster.setFileName(sMovieTitle)
                                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()