#-*- coding: utf-8 -*-
#zombi https://github.com/zombiB/zombi-addons/
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, isMatrix
from resources.lib.parser import cParser
import re
 
SITE_IDENTIFIER = 'brstej'
SITE_NAME = 'brstej'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'https://r.brstej.tv'
RAMADAN_SERIES = (URL_MAIN + '/category1.php?cat=rmdan2021', 'showSeries')
SERIE_TR = ('https://p.brstej.com:2053/category1.php?cat=turkeyseress', 'showSeries')
SERIE_HEND = ('https://p.brstej.com:2053/category1.php?cat=indeasreses2021', 'showSerie')
SERIE_EN = ('https://p.brstej.com:2053/category1.php?cat=english', 'showSeries')
SERIE_AR = ('https://p.brstej.com:2053/category1.php?cat=arabic-seriesss', 'showSeries')
MOVIE_EN = ('https://p.brstej.com:2053/category1.php?cat=aflamajnby', 'showMovies')
MOVIE_AR = ('https://p.brstej.com:2053/category1.php?cat=aflam2021', 'showMovies')
MOVIE_HI = ('https://p.brstej.com:2053/category1.php?cat=hindi-movies', 'showMovies')
MOVIE_TURK= ('https://p.brstej.com:2053/category1.php?cat=turkish-movies', 'showMovies')
KID_MOVIES = ('https://p.brstej.com:2053/category1.php?cat=anime', 'showMovies')
ANIM_NEWS = ('https://p.brstej.com:2053/category1.php?cat=anmei', 'showSeries')
SERIE_ASIA = ('https://p.brstej.com:2053/category1.php?cat=asia', 'showSerie')
REPLAYTV_NEWS = ('https://p.brstej.com:2053/category1.php?cat=tv100', 'showMovies')

URL_SEARCH = ('https://p.brstej.com:2053/search.php?keywords=', 'showMovies')
URL_SEARCH_SERIES = ('https://p.brstej.com:2053/search.php?video-id=&keywords=', 'showSeries')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'SEARCH_MOVIES', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', 'SEARCH_SERIES', 'search.png', oOutputParameterHandler)

            
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = 'https://p.brstej.com:2053/search.php?keywords='+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = 'https://p.brstej.com:2053/search.php?video-id=&keywords='+sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showMovies(sSearch = ''):
    import requests
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    if isMatrix(): 
       sHtmlContent = str(sHtmlContent.encode('latin-1',errors='ignore'),'utf-8',errors='ignore')
 # ([^<]+) .+?
    sPattern = '<img alt="([^<]+)" src="([^<]+)" style=.+?<h3><a href="([^<]+)" title'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = str(aEntry[0]).replace("مشاهدة","").replace("مترجمة","").replace("مسلسل","").replace("انمي","").replace("كاملة","").replace("كامل","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("اونلاين","").replace("بجودة","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("مدبلج للعربية","مدبلج").replace("مدبلج","[مدبلج]")
            siteUrl = str(aEntry[2])
            sThumb = str(aEntry[1])
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')
            sDisplayTitle = ('%s (%s)') % (sTitle, sYear)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sMovieTitle2', sDisplayTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()

def showSeries(sSearch = ''):
    import requests
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    if isMatrix(): 
       sHtmlContent = str(sHtmlContent.encode('latin-1',errors='ignore'),'utf-8',errors='ignore')
 # ([^<]+) .+? (.+?)
    sPattern = '<img alt="([^<]+)" src="([^<]+)" style=.+?<h3><a href="([^<]+)" title'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = str(aEntry[0]).replace("مشاهدة","").replace("مترجمة","").replace("مسلسل","").replace("انمي","").replace("كاملة","").replace("كامل","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("اونلاين","").replace("بجودة","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("مدبلج للعربية","مدبلج").replace("مدبلج","[مدبلج]").split('الحلقة')[0]
            siteUrl = str(aEntry[2])
            sThumb = str(aEntry[1])
            sDesc = ''


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sMovieTitle2', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
  # ([^<]+) .+?

    oParser = cParser()
    if 'class="pagination pagination-sm pagination-arrows' in sHtmlContent:
        sStart = '<ul class="pagination pagination-sm pagination-arrows">'
        sEnd = '<div class="col-md-3">'
        sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

        sPattern = '<li class=""><a href="([^<]+)">([^<]+)</a>'
        aResult = oParser.parse(sHtmlContent, sPattern)
	
	
        if (aResult[0] == True):
            total = len(aResult[1])
            progress_ = progress().VScreate(SITE_NAME)
            for aEntry in aResult[1]:
                progress_.VSupdate(progress_, total)
                if progress_.iscanceled():
                   break
 
                sTitle = aEntry[1]
            
                sTitle =  "PAGE " + sTitle
                sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
                siteUrl = URL_MAIN+'/'+str(aEntry[0])
                sThumbnail = ""
                sInfo = ""


                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			
                oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, '', oOutputParameterHandler)

            progress_.VSclose(progress_)
 
    if not sSearch:
        oGui.setEndOfDirectory()
			
def showSeasons():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sMovieTitle2 = oInputParameterHandler.getValue('sMovieTitle2')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')


    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    if isMatrix(): 
       sHtmlContent = str(sHtmlContent.encode('latin-1',errors='ignore'),'utf-8',errors='ignore')
   
    oParser = cParser()
     # (.+?) ([^<]+) .+?
    sPattern = 'href="([^<]+)"><em>([^<]+)</em><span>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 


            sTitle = sMovieTitle2+' E'+aEntry[1]
            siteUrl = URL_MAIN+str(aEntry[0]).replace("watch.php","view.php")
            sThumb = sThumbnail
            sDesc = ""

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler) 
        
        progress_.VSclose(progress_)
    # (.+?)
               
       
    oGui.setEndOfDirectory() 
 
def showHosters():
    import requests
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    # (.+?) .+?          

    sPattern = "data-embed-url='(.+?)'>"
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
            if 'userload' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                sDisplayTitle = sTitle
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
			               
    oGui.setEndOfDirectory()  
# (.+?) .+? ([^<]+)
def __checkForNextPage(sHtmlContent):
    sPattern = '<a href="([^<]+)">&raquo;</a>'
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if (aResult[0] == True):
        #print aResult[1][0]
        return URL_MAIN+'/'+aResult[1][0]

    return False