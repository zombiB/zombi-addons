# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re
from urllib import request
from resources.lib.config import cConfig
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog, siteManager
from resources.lib.util import cUtil, Unquote


	
SITE_IDENTIFIER = 'dramacafe'
SITE_NAME = 'Dramacafe'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)


MOVIE_AR = (URL_MAIN + 'category.php?cat=aflam-araby1', 'showMovies')
MOVIE_EN = (URL_MAIN + 'category.php?cat=aflam-agnaby', 'showMovies')
MOVIE_HI = (URL_MAIN + 'category.php?cat=aflam-hindi', 'showMovies')
MOVIE_ASIAN = (URL_MAIN + 'category.php?cat=asian-movies', 'showMovies')
MOVIE_TURK = (URL_MAIN + 'category.php?cat=Turkish-Movies', 'showMovies')
MOVIE_DUBBED = (URL_MAIN + 'category.php?cat=Dubbed-Movies', 'showMovies')
KID_MOVIES = (URL_MAIN + 'category.php?cat=aflam-cartoon', 'showMovies')
RAMADAN_SERIES = (URL_MAIN + 'category.php?cat=1ramdan-2022', 'showSeries')
SERIE_EN = (URL_MAIN + 'category.php?cat=moslslat-agnaby', 'showSeries')
SERIE_AR = (URL_MAIN + 'category.php?cat=moslslat-arabia', 'showSeries')
SERIE_HEND = (URL_MAIN + 'category.php?cat=moslslat-hindia', 'showSeries')
SERIE_ASIA = (URL_MAIN + 'category.php?cat=moslslat-asia', 'showSeries')
SERIE_TR = (URL_MAIN + 'category.php?cat=moslslat-turkya', 'showSeries')
SERIE_DUBBED = (URL_MAIN + 'category.php?cat=moslslat-modablaja', 'showSeries')
REPLAYTV_NEWS = (URL_MAIN + 'category.php?cat=tv-programs', 'showSeries')




URL_SEARCH = (URL_MAIN + 'search.php?keywords=', 'showSeries')
URL_SEARCH_MOVIES = (URL_MAIN + 'search.php?keywords=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'search.php?keywords=', 'showSerie')

FUNCTION_SEARCH = 'showSeries'
	
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Search Movies', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', 'Search Series', 'search.png', oOutputParameterHandler)

    
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', RAMADAN_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'رمضان', 'rmdn.png', oOutputParameterHandler)
    
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
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', 'crtoon.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', 'film.png', oOutputParameterHandler)
    
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

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات هندية', 'mslsl.png', oOutputParameterHandler)

    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_DUBBED[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات مدبلجة', 'mslsl.png', oOutputParameterHandler)  

    
   
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'برامج تلفزيونية', 'brmg.png', oOutputParameterHandler)
	
    
    oGui.setEndOfDirectory()


 

 
 
def showSearch():
    oGui = cGui() 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + 'search.php?keywords=فيلم+'+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSearchSeries():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + 'search.php?keywords=مسلسل+'+sSearchText
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
    sPattern = '<div class="thumbnail">.+?<a href="([^<]+)" title="([^<]+)">.+?<img src="([^<]+)" alt='

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0] :
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1].replace("مشاهدة","").replace("بجوده","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("برنامج","").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            siteUrl = aEntry[0]
            sThumb = aEntry[2]
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
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
 # ([^<]+) .+? (.+?)
    sPattern = '<div class="thumbnail">.+?<a href="([^<]+)" title="([^<]+)">.+?<img src="([^<]+)" alt='

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0] :
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("برنامج","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","").replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع و العشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الثالث و الثلاثون","S33").replace("الموسم الأول","S1").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9")
            siteUrl = aEntry[0]
            
            sThumb = aEntry[2]
            
            sTitle = sTitle.split('الحلقة')[0]
            sDesc = ''


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
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
    sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = "<a.+?class='+?' title='.+?' href='([^<]+)'><li><em>([^<]+)</em>"
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if aResult[0] :
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
 
            
            
            sTitle = sMovieTitle+'E'+aEntry[1]
            siteUrl = URL_MAIN+aEntry[0]
            
            sThumb = sThumb
            sDesc = ''
			


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
           
    oGui.setEndOfDirectory()
	

def __checkForNextPage(sHtmlContent):
    sPattern = '<a href="([^<]+)"><i class="fa fa-arrow-left"></i></a>'	 
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0] :
        return aResult[1][0]

    return False


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

   
    oParser = cParser()
    sId2 = ''

    sPattern = '<a href="(.+?)" target="_blank" rel="nofollow" class="controls-play-pause-big" data-control="play-pause" playing="paused"></a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        sId2 = aResult[1][0]
    #Recuperation infos
    html = ''
     # (.+?) ([^<]+) .+?
    sPattern = 'data-embed="(.+?)">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        for aEntry in aResult[1]:
            
            headers = {'Host': 'z.dramacafe-tv.com:82',
							'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
							'Accept': '*/*',
							'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
							'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
							'X-Requested-With': 'XMLHttpRequest',
							'Referer': sUrl,
							'Connection': 'keep-alive'}
            sId = aEntry.replace("('","").replace("')","").replace('"<iframe src=','')
            data = {'serverEmbed':sId,'.embedded':html,'Ajax':'1'}
            s = requests.Session()			
            r = s.post(URL_MAIN+'/ajax/getPlayer',data = data)
            sHtmlContent1 = r.content.decode('utf8',errors='ignore')  
            VSlog(sHtmlContent1)   
            sPattern = "src='(.+?)'"
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent1, sPattern)
            if aResult[0] :
                    url = aResult[1][0]
                    sTitle = sMovieTitle
                    if url.startswith('//'):
                       url = 'http:' + url
            
                    sHosterUrl = url 
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if oHoster:
                       oHoster.setDisplayName(sTitle)
                       oHoster.setFileName(sTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)  
				

                
    oGui.setEndOfDirectory()
                
   

