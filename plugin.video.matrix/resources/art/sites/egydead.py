#-*- coding: utf-8 -*-
#zombi https://github.com/zombiB/zombi-addons/
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, isMatrix, VSlog, siteManager, addon
from resources.lib.parser import cParser
import re
 
ADDON = addon()
icons = ADDON.getSetting('defaultIcons')

SITE_IDENTIFIER = 'egydead'
SITE_NAME = 'Egydead'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (URL_MAIN+'/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%a7%d8%ac%d9%86%d8%a8%d9%8a/', 'showMovies')
MOVIE_PACK = ('https://w3.egydead.live/assembly/', 'showPack')
MOVIE_DUBBED = (URL_MAIN+'/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%a7%d8%ac%d9%86%d8%a8%d9%8a%d8%a9-%d9%85%d8%af%d8%a8%d9%84%d8%ac%d8%a9/', 'showMovies')
MOVIE_TURK = (URL_MAIN+'/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%aa%d8%b1%d9%83%d9%8a%d8%a9/', 'showMovies')
MOVIE_AR = (URL_MAIN + '/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%b9%d8%b1%d8%a8%d9%8a/', 'showMovies')
MOVIE_ASIAN = (URL_MAIN+'/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%a7%d8%b3%d9%8a%d9%88%d9%8a%d8%a9/', 'showMovies')
KID_MOVIES = (URL_MAIN+'/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d9%83%d8%b1%d8%aa%d9%88%d9%86/', 'showMovies')
KID_CARTOON = (URL_MAIN+'/series-category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d9%83%d8%b1%d8%aa%d9%88%d9%86/', 'showSeries')
SERIE_LATIN = (URL_MAIN+'/series-category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d9%84%d8%a7%d8%aa%d9%8a%d9%86%d9%8a%d8%a9/', 'showSeries')
SERIE_EN = (URL_MAIN+'/series-category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%a7%d8%ac%d9%86%d8%a8%d9%8a/', 'showSeries')
SERIE_AR = (URL_MAIN+'/series-category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%b9%d8%b1%d8%a8%d9%8a/', 'showSeries')
SERIE_TR = (URL_MAIN+'/series-category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%aa%d8%b1%d9%83%d9%8a%d8%a9/', 'showSeries')
SERIE_ASIA = (URL_MAIN+'/series-category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%a7%d8%b3%d9%8a%d9%88%d9%8a%d8%a9/', 'showSeries')

DOC_SERIES = (URL_MAIN+'/series-category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d9%88%d8%ab%d8%a7%d8%a6%d9%82%d9%8a%d8%a9/', 'showSeries')
SERIE_DUBBED = (URL_MAIN+'/series-category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%a7%d8%ac%d9%86%d8%a8%d9%8a%d8%a9-%d9%85%d8%af%d8%a8%d9%84%d8%ac%d8%a9/', 'showSeries')
DOC_NEWS = (URL_MAIN+'/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d9%88%d8%ab%d8%a7%d8%a6%d9%82%d9%8a%d8%a9/', 'showMovies')
ANIM_MOVIES = (URL_MAIN+'/series-category/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%a7%d9%86%d9%85%d9%8a/', 'showMovies')
ANIM_NEWS = (URL_MAIN+'/series-category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%a7%d9%86%d9%85%d9%8a/', 'showSeries')
REPLAYTV_PLAY = (URL_MAIN+'/category/%d9%85%d8%b3%d8%b1%d8%ad%d9%8a%d8%a7%d8%aa/', 'showMovies')
REPLAYTV_NEWS = (URL_MAIN+'/category/%d8%b9%d8%b1%d9%88%d8%b6-%d9%88%d8%ad%d9%81%d9%84%d8%a7%d8%aa/', 'showMovies')
SPORT_FOOT = (URL_MAIN+'/tag/%d9%83%d8%a7%d8%b3-%d8%a7%d9%84%d8%b9%d8%a7%d9%84%d9%85-2022/', 'showMovies')

URL_SEARCH = (URL_MAIN+'/?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN+'/?s=%D9%81%D9%8A%D9%84%D9%85+', 'showMoviesSearch')
URL_SEARCH_SERIES = (URL_MAIN+'/?s=%D9%85%D8%B3%D9%84%D8%B3%D9%84+', 'showSearchSeries')
FUNCTION_SEARCH = 'showSearch'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'SEARCH_MOVIES', icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', 'SEARCH_SERIES', icons + '/Search.png', oOutputParameterHandler)
    oOutputParameterHandler = cOutputParameterHandler()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'افلام اجنبي', icons + '/Movies.png', oOutputParameterHandler)
  
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أسيوية', icons + '/Asian.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية', icons + '/Turkish.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام إنمي', icons + '/Anime.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'https://w.egydead.live/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%a7%d9%86%d9%85%d9%8a/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام إنمي2', icons + '/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', icons + '/Cartoon.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_DUBBED[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام مدبلجة', icons + '/Dubbed.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام وثائقية', icons + '/Documentary.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', icons + '/TVShowsEnglish.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات عربية', icons + '/Arabic.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أسيوية', icons + '/Asian.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', icons + '/Turkish.png', oOutputParameterHandler) 

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_LATIN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات لاتنية', icons + '/TVShows.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات إنمي', icons + '/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', KID_CARTOON[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات كرتون', icons + '/Cartoon.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات وثائقية', icons + '/Documentary.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_DUBBED[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات مدبلجة', icons + '/Dubbed.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'https://w.egydead.live/channel/netflix/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات Netfilx', icons + '/TVShows.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'برامج تلفزيونية',icons + '/Programs.png', oOutputParameterHandler)
	
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_PLAY[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'مسرحيات', icons + '/Theater.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'https://w.egydead.live/category/%d8%b9%d8%b1%d9%88%d8%b6-%d9%88%d8%ad%d9%81%d9%84%d8%a7%d8%aa/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries' ,'ستاند اب وحفلات',icons + '/Programs.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN+'/?s=%D9%81%D9%8A%D9%84%D9%85+'+sSearchText
        showMoviesSearch(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN+'/?s=%D9%85%D8%B3%D9%84%D8%B3%D9%84+'+sSearchText
        showSearchSeries(sUrl)
        oGui.setEndOfDirectory()
        return
   
def showMoviesSearch(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
      # (.+?) ([^<]+) .+?

    sPattern = '<li class="movieItem"><a href="([^<]+)" title="([^<]+)"><img src="([^<]+)">'
	

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
				
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","").replace("مدبلج","").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            siteUrl = aEntry[0]+'?View=1'
            sDesc = ""
            sThumb = aEntry[2]
            sYear = ''
            sDub = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')



            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle) 
            oOutputParameterHandler.addParameter('sYear', sYear) 
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMoviesSearch', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
def showSearchSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
      # (.+?) ([^<]+) .+?

    sPattern = '<li class="movieItem"><a href="([^<]+)" title="([^<]+)"><img src="([^<]+)">'
	

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
            if "حلقة" in aEntry[1]:
                continue
				
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("كاملة","").replace("كامل","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("والأخيرة","").replace("والاخيرة","").replace("الأخيرة","").replace("الاخيرة","")
            siteUrl = aEntry[0]
            sDesc = ""
            sThumb = aEntry[2]
            sYear = ''
            sDub = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')
            sDisplayTitle = sTitle.replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace(" الثانى","2").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الحلقة "," E").replace("الموسم","S").replace("S ","S")




            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb) 
            oOutputParameterHandler.addParameter('sYear', sYear) 
            if '/episode/'  in aEntry[0] :
                oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler) 
            elif '/serie/'  in aEntry[0] :
                oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler) 
            else: 
	            oGui.addTV(SITE_IDENTIFIER, 'showEps', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
        
  # ([^<]+) .+?

    sPattern = "<a href='([^<]+)' class='inactive'>([^<]+)</a>"

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
 
            sTitle = aEntry[1]
            
            sTitle =  "PAGE " + sTitle
            sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
            siteUrl = aEntry[0]


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, '', oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
      # (.+?) ([^<]+) .+?

    sPattern = '<li class="movieItem"><a href="([^<]+)" title="([^<]+)"><img src="([^<]+)">'

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
 
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","").replace("مدبلج","").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            siteUrl = aEntry[0]+'?View=1'
            sDesc = ''
            sThumb = aEntry[2]
            sYear = ''
            sDub = ''
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
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)
 
    if not sSearch:
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
      # (.+?) ([^<]+) .+?

    sPattern = '<li class="movieItem"><a href="([^<]+)" title="([^<]+)"><img src="([^<]+)">'

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
 
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","").replace("مدبلج","").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","").replace("مدبلجة","").replace("كامل","").replace("مدبلج للعربية","").replace("مدبلج","").replace("سلسلة افلام","").replace("سلسلة اجزاء","")
            siteUrl = aEntry[0]
            sDesc = ''
            sThumb = aEntry[2]



            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMoviePack(SITE_IDENTIFIER, 'showPacks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
			
def showPacks():
	oGui = cGui()
    
	oInputParameterHandler = cInputParameterHandler()
	sUrl = oInputParameterHandler.getValue('siteUrl')
	sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
	sThumb = oInputParameterHandler.getValue('sThumb')
 
	oRequestHandler = cRequestHandler(sUrl)
	sHtmlContent = oRequestHandler.request()

	oParser = cParser()
            
	sPattern =  '<h1 class="TitleMaster">(.+?)<div class="related-posts">' 
	aResult = oParser.parse(sHtmlContent,sPattern)
	if aResult[0]:
		sHtmlContent = aResult[1][0] 
 # ([^<]+) .+?
		sPattern = '<li class="movieItem"><a href="([^<]+)" title="([^<]+)"><img src="([^<]+)">'

		oParser = cParser()
		aResult = oParser.parse(sHtmlContent, sPattern)
	
	
		if aResult[0]:
			oOutputParameterHandler = cOutputParameterHandler()    
			for aEntry in aResult[1]:
 
				sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","").replace("مدبلج","").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
				siteUrl = aEntry[0]+'?View=1'
				sDesc = ''
				sThumb = aEntry[2]
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
    sPattern = '<li class="movieItem"><a href="([^<]+)" title="([^<]+)"><img src="([^<]+)">'

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
 

            sTitle = aEntry[1].replace("الجزء","الموسم").replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("كاملة","").replace("كامل","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("والأخيرة","").replace("والاخيرة","").replace("الأخيرة","").replace("الاخيرة","")
            siteUrl = aEntry[0]
            sDesc = ''
            sThumb = aEntry[2]
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')
            sDisplayTitle = sTitle.replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace(" الثانى","2").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الحلقة "," E").replace("الموسم","S").replace("S ","S")

			


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
            oOutputParameterHandler.addParameter('sDesc', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb) 
            oOutputParameterHandler.addParameter('sYear', sYear)
            if '/episode/'  in aEntry[0] :
                oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler) 
            elif '/serie/'  in aEntry[0] :
                oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler) 
            else: 
	            oGui.addTV(SITE_IDENTIFIER, 'showEps', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
        

        progress_.VSclose(progress_)

        
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
      # (.+?) ([^<]+) .+?
 
def __checkForNextPage(sHtmlContent):
    sPattern = '<a class="next page-numbers" href="([^<]+)">'
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0]:
        return aResult[1][0]

    return False
  
def showSeasons():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()

    sStart = '<div class="seasons-list">'
    sEnd = '<div class="related-posts">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    # .+? ([^<]+) (.+?)
    sPattern = '<li class="movieItem"><a href="([^<]+)" title="(.+?)"><img src="(.+?)">'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
   
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
 
            sTitle = aEntry[1].replace("الجزء","الموسم").replace("مترجمة","").replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("انمى","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("كامل","").replace("مشاهدة وتحميل","").replace("اون لاين","").replace("جميع حلقات","").replace("والأخيرة","").replace("والاخيرة","").replace("الأخيرة","").replace("الاخيرة","") 
            
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')
            sDisplayTitle = sTitle.replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace(" الثانى","2").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الحلقة "," E").replace("الموسم","S").replace("S ","S")
 
            oOutputParameterHandler.addParameter('siteUrl', aEntry[0])
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear) 
            

 
            oGui.addEpisode(SITE_IDENTIFIER, 'showEps', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
 
       
    oGui.setEndOfDirectory() 
  
def showEps():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    # .+? ([^<]+)
    sPattern = '<a href="([^<]+)" title="([^<]+)">([^<]+)</a>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
   
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
 
            sTitle = aEntry[1].replace("الجزء","الموسم").replace("مترجمة","").replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("انمى","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("كامل","").replace("مشاهدة وتحميل","").replace("اون لاين","").replace("جميع حلقات","").replace("والأخيرة","").replace("والاخيرة","").replace("الأخيرة","").replace("الاخيرة","") 
            
            siteUrl = aEntry[0]
            sThumb = sThumb
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')
            sDisplayTitle = sTitle.replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace(" الثانى","2").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الحلقة "," E").replace("الموسم","S").replace("S ","S")
 
            oOutputParameterHandler.addParameter('siteUrl', aEntry[0])
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear) 
            

 
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters2', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
 
       
    oGui.setEndOfDirectory() 
 
def showHosters2():
    oGui = cGui()
    import requests
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    #print sHtmlContent 

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    s = requests.Session()
    data = {'View':'1'}
    r = s.post(sUrl, data = data)
    sHtmlContent = r.content
    if isMatrix(): 
       sHtmlContent = sHtmlContent.decode('utf8',errors='ignore')
    

   
    oParser = cParser()
    # ([^<]+) (.+?)       

    sPattern = '<li data-link="(.+?)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if aResult[0]:
        for aEntry in aResult[1]:
            
            url = str(aEntry)
            sTitle =  sMovieTitle
            if url.startswith('//'):
               url = 'http:' + url
				
					
            
            sHosterUrl = url 
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
               oHoster.setFileName(sDisplayTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
				
    # ([^<]+) (.+?)         

    sPattern = 'class="ser-link" href="(.+?)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if aResult[0]:
        for aEntry in aResult[1]:
            
            url = str(aEntry)
            sTitle =  sMovieTitle
            if url.startswith('//'):
               url = 'http:' + url
				
					
            
            sHosterUrl = url
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
               oHoster.setFileName(sDisplayTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
 
                
    oGui.setEndOfDirectory()
 
def showHosters():
    oGui = cGui()
    import requests
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    #print sHtmlContent 

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    s = requests.Session()
    data = {'View':'1'}
    r = s.post(sUrl, data = data)
    sHtmlContent = r.content
    if isMatrix(): 
       sHtmlContent = sHtmlContent.decode('utf8',errors='ignore')
    

   
    oParser = cParser()
    # ([^<]+) (.+?)       

    sPattern = '<li data-link="(.+?)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if aResult[0]:
        for aEntry in aResult[1]:
            
            url = aEntry
            sTitle =  sMovieTitle
            if url.startswith('//'):
               url = 'http:' + url
				
					
            
            sHosterUrl = url 
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
               oHoster.setFileName(sDisplayTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
				
    # ([^<]+) (.+?)   .+?      

    sPattern = '<span class="ser-name">(.+?)</span>.+?class="ser-link" href="(.+?)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if aResult[0]:
        for aEntry in aResult[1]:
            
            url = aEntry[1]
            sTitle =  sMovieTitle+'('+aEntry[0]+')'
            if url.startswith('//'):
               url = 'http:' + url
				
					
            
            sHosterUrl = url
            if '?download_' in sHosterUrl:
                sHosterUrl = sHosterUrl.replace("moshahda","ffsff")
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
               oHoster.setFileName(sDisplayTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
				

    # .+? ([^<]+)
    sPattern = '<a href="([^<]+)" title="([^<]+)">([^<]+)</a>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

   
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
 
            sTitle = aEntry[1].replace("الجزء","الموسم").replace("مشاهدة","").replace("الأخيرة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("الاخيرة","").replace("مترجم","").replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("S ","S").replace("الحلقة "," E")
            siteUrl = aEntry[0]
            sThumb = sThumb
            sDesc = ''
 
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sTitle)
            

 
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
 
                
    oGui.setEndOfDirectory()
