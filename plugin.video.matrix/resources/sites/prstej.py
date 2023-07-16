# zombi https://github.com/zombiB/zombi-addons/

import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser
from bs4 import BeautifulSoup

ADDON = addon()
icons = ADDON.getSetting('defaultIcons')

SITE_IDENTIFIER = 'prstej'
SITE_NAME = 'Prstej'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_GN = (URL_MAIN + '/category102.php?cat=movies2023', 'showMovies')
RAMADAN_SERIES = (URL_MAIN + '/category102.php?cat=ramdan2023', 'showSeries')
MOVIE_AR = (URL_MAIN + '/category102.php?cat=aflam2023', 'showMovies')
SERIE_AR = (URL_MAIN + '/category102.php?cat=arab2023', 'showSeries')
SERIE_TR = (URL_MAIN + '/category102.php?cat=ty-2023', 'showSeries')
SERIE_GULF = (URL_MAIN + '/category102.php?cat=5a-2023', 'showSeries')
SERIE_EGY = (URL_MAIN + '/category102.php?cat=eg2024', 'showSeries')
SERIE_SY = (URL_MAIN + '/category102.php?cat=sy-2023', 'showSeries')
PROGRAMS = (URL_MAIN + '/category102.php?cat=tv2023', 'showSeries')

URL_SEARCH = (URL_MAIN + '/search.php?keywords=', 'showSeries')
URL_SEARCH_MOVIES = (URL_MAIN + '/search.php?keywords=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '/search.php?keywords=', 'showSeries')
FUNCTION_SEARCH = 'showSearch'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'SEARCH_MOVIES', icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', 'SEARCH_SERIES', icons + '/Search.png', oOutputParameterHandler)
       	
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام', icons + '/Movies.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عربية', icons + '/Arabic.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات عربية', icons + '/Arabic.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', icons + '/Turkish.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_EGY[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات مصرية', icons + '/Eygptian.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SY[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات شامية', icons + '/Syrian.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', PROGRAMS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'برامج', icons + '/Turkish.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', RAMADAN_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات رمضان', icons + '/Ramadan.png', oOutputParameterHandler)
	
    oGui.setEndOfDirectory()
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/search.php?keywords='+sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/search.php?keywords='+sSearchText
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
      # (.+?) ([^<]+) .+?
    sPattern = '</span><a href="([^<]+)" title="([^<]+)">.+?data-echo="([^<]+)" class="img-responsive">'

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
 
            if "مسلسل"  in aEntry[1]:
                continue
 
            if "حلقة"  in aEntry[1]:
                continue
 
            
            sTitle = aEntry[1].replace("مشاهدة","").replace("مشاهده","").replace("مترجم","").replace("فيلم","").replace("اونلاين","").replace("اون لاين","").replace("برنامج","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("انمي","")
 
 
            siteUrl = aEntry[0].replace("watch.php","play.php")
            sDesc = ""
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
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        

        progress_.VSclose(progress_)
 
    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', icons + '/next.png', oOutputParameterHandler)
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
    
    # (.+?) .+? ([^<]+)   
    sPattern = '<div class=\"pm-video-thumb\">.+?<a href=\"(.+?)\" title=\"(.+?)\">.+?data-echo=\"(.+?)\"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    itemList = []
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            siteUrl = aEntry[0]
            
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("مشاهده","").replace("برنامج","").replace("مترجمة","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("مشاهدة وتحميل","").replace("اون لاين","")
            sThumb = aEntry[2]
            sDesc = ''
            sTitle = sTitle.split('موسم')[0].split('الحلقة')[0]
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')

            if sTitle not in itemList:
                itemList.append(sTitle)
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sYear', sYear)
                oOutputParameterHandler.addParameter('sThumb', sThumb)

                oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
 
        

        progress_.VSclose(progress_)
        
  # ([^<]+) .+? (.+?)
 
    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', icons + '/next.png', oOutputParameterHandler)
        oGui.setEndOfDirectory()
 
      # (.+?) ([^<]+) .+?
	
def __checkForNextPage(sHtmlContent):
    soup = BeautifulSoup(sHtmlContent, "html.parser")
            
    pagesCont = soup.find("ul",{"class":"pagination pagination-sm pagination-arrows"})
    VSlog(pagesCont)
    pages = pagesCont.findAll("li")
    
    for page in pages:
        if '»' in page.a.text:
            VSlog(page)
            nextP = URL_MAIN + page.a['href']
            VSlog('Next Page : ' + nextP)
            return nextP
        else:
            VSlog("Next Page couldn't be fouund")
    return False
    # sPattern = '<a href=\"([^<]+)\">&raquo;</a>'
	
    # oParser = cParser()
    # aResult = oParser.parse(sHtmlContent, sPattern)
    # #VSlog(aResult)
 
    # if aResult[0]:
        # VSlog(URL_MAIN+aResult[1][0])
        # return URL_MAIN+aResult[1][0]
    # else:
        # VSlog("Next Page couldn't be fouund")
    # return False
	
def showEpisodes():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 # ([^<]+) .+? (.+?)

    sPattern = '<div class="SeasonsEpisodes" style="display:none;" data-serie="(.+?)">(.+?)</div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            sSeason = "S"+aEntry[0]
            sHtmlContent = aEntry[1]
 # ([^<]+) .+?

            sPattern = 'href="(.+?)" title.+?<em>(.+?)</em><span>'

            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
	
	
            if aResult[0]:
                oOutputParameterHandler = cOutputParameterHandler()  
                for aEntry in aResult[1]:
 
                    siteUrl = URL_MAIN +aEntry[0]
                    siteUrl = siteUrl.replace("watch.php","play.php")
                    sTitle = sMovieTitle+' '+sSeason
                    sTitle = sTitle+" E"+aEntry[1]
                    sThumb = sThumb
                    sDesc = ""
			


                    oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)
        
       
    oGui.setEndOfDirectory() 
	 
def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')



    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # ([^<]+) .+?
               

    sPattern = "data-embed-url='([^<]+)'>"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if aResult[0]:
        for aEntry in aResult[1]:
            
            sHosterUrl = aEntry
            sTitle =  ""
            if sHosterUrl.startswith('//'):
                sHosterUrl = 'http:' + sHosterUrl
            if 'userload' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'moshahda' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            if 'mystream' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN   
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
               

    sPattern = "data-embed='([^<]+)' data"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if aResult[0]:
        for aEntry in aResult[1]:
            
            sHosterUrl = aEntry
            sTitle =  ""
            if sHosterUrl.startswith('//'):
                sHosterUrl = 'http:' + sHosterUrl
            if 'userload' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            if 'moshahda' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            if 'mystream' in sHosterUrl:
                sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN   
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
				

                
    oGui.setEndOfDirectory()
