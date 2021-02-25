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
 
SITE_IDENTIFIER = 'mycima'
SITE_NAME = 'mycima'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'https://mycima.to'

MOVIE_CLASSIC = ('https://mycima.plus/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85/arabic-movies-%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%b9%d8%b1%d8%a8%d9%8a/list/old/', 'showMovies')
MOVIE_EN = ('https://mycima.plus/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85/4-movies-english-%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%a7%d8%ac%d9%86%d8%a8%d9%8a/', 'showMovies')

MOVIE_AR = ('https://mycima.plus/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85/arabic-movies-%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%b9%d8%b1%d8%a8%d9%8a/', 'showMovies')
MOVIE_TURK = ('https://mycima.plus/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%aa%d8%b1%d9%83%d9%89-turkish-films/', 'showMovies')
MOVIE_HI = ('https://mycima.plus/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d9%87%d9%86%d8%af%d9%8a-indian-movies/', 'showMovies')
KID_MOVIES = ('https://mycima.plus/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d9%83%d8%b1%d8%aa%d9%88%d9%86/', 'showMovies')
SERIE_AR = ('https://mycima.plus/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%b9%d8%b1%d8%a8%d9%8a%d8%a9-arabic-series/', 'showSeries')
SERIE_EN = ('https://mycima.plus/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa/series-english-%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%a7%d8%ac%d9%86%d8%a8%d9%8a/', 'showSeries')
SERIE_HEND = ('https://mycima.plus/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa/1-series-indian-%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d9%87%d9%86%d8%af%d9%8a%d8%a9/', 'showSeries')
ANIM_NEWS = ('https://mycima.plus/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d9%83%d8%b1%d8%aa%d9%88%d9%86/', 'showSeries')
SERIE_ASIA = ('https://mycima.plus/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%a7%d8%b3%d9%8a%d9%88%d9%8a%d8%a9//', 'showSeries')
SERIE_TR = ('https://mycima.plus/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%aa%d8%b1%d9%83%d9%8a%d9%87-turkish-series/', 'showSeries')
DOC_SERIES = ('https://mycima.plus/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d9%88%d8%ab%d8%a7%d8%a6%d9%82%d9%8a%d8%a9-documentary-series/', 'showSeries')
DOC_NEWS = ('https://mycima.plus/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d9%88%d8%ab%d8%a7%d8%a6%d9%82%d9%8a%d8%a9-documentary-films/', 'showMovies')
URL_SEARCH = ('https://mycima.to/search/', 'showSeries')
URL_SEARCH_SERIES = ('https://mycima.io/search/', 'showSeries')
URL_SEARCH_MOVIES = ('https://mycima.io/search/', 'showMovies')
FUNCTION_SEARCH = 'showSearch'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'SEARCH_MOVIES', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', 'SEARCH_SERIES', 'search.png', oOutputParameterHandler)
    

            
    oGui.setEndOfDirectory()
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = 'https://mycima.io/search/'+sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = 'https://mycima.io/search/'+sSearchText
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
    sPattern = '<div class="Thumb--GridItem"><a href="([^<]+)" title="([^<]+)"><.+?background-image:url([^<]+);">.+?class="year">(.+?)</span>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if "فيلم" not in aEntry[1]:
				continue
 
            sTitle = aEntry[1]
            sTitle = sTitle.decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            sTitle = sTitle.replace("مشاهدة","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","")
 
 
            siteUrl = aEntry[0]
            sInfo = ""
            sThumbnail = str(aEntry[2]).replace("(","").replace(")","")
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
				sYear = str(m.group(0))
				sTitle = sTitle.replace(sYear,'')
            sDisplayTitle = ('%s (%s)') % (sTitle, sYear)



            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
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
    # (.+?) .+? ([^<]+)   
    sPattern = '<div class="Thumb--GridItem"><a href="([^<]+)" title="([^<]+)"><span class="BG--GridItem" data-lazy-style="background-image:url([^<]+);"><div class=.+?<span class="year">([^<]+)</span>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if "فيلم"  in aEntry[1]:
				continue
 
            siteUrl = aEntry[0]
            sTitle = aEntry[1]+aEntry[3]
            sTitle = sTitle.decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            sTitle = sTitle.replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("مترجمة","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("مشاهدة وتحميل","").replace("اون لاين","")
            sThumbnail = str(aEntry[2]).replace("(","").replace(")","")
            sDisplayTitle = sTitle
            sDisplayTitle2 = sTitle.split('موسم')[0]
            sDisplayTitle2 = sDisplayTitle2.split('مدبلج')[0]
            sInfo = ''
            sDisplayTitle = sDisplayTitle.replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم العاشر","S10").replace("الموسم","S").replace("S ","S").replace("موسم","S").replace("S ","S").split('حلقة')[0]

			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle2)
            oOutputParameterHandler.addParameter('sMovieTitle2', sDisplayTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sDisplayTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
  # ([^<]+) .+?

    sPattern = '<li><a class="page-numbers" href="([^<]+)">([^<]+)</a></li>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1].decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            sTitle =  "PAGE " + sTitle
            sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
            siteUrl = str(aEntry[0])
            sThumbnail = ""
            sInfo = ""


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
			
            oGui.addTV(SITE_IDENTIFIER, 'showSeries', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
      # (.+?) ([^<]+) .+?
 
def __checkForNextPage(sHtmlContent):
    sPattern = '<li><a class="next page-numbers" href="(.+?)">'
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if (aResult[0] == True):
        #print aResult[1][0]
        return aResult[1][0]

    return False
  
def showSeasons():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sMovieTitle2 = oInputParameterHandler.getValue('sMovieTitle2')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')



    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    sHtmlContent = oRequestHandler.request()
    # (.+?) .+? ([^<]+)   
    sPattern = '<a class="hoverable activable.+?href="([^<]+)"><div class="Thumb"><span><i class="fa fa-play"></i></span></div><episodeArea><episodeTitle>([^<]+)</episodeTitle></episodeArea></a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    


    #print aResult
   
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = str(sMovieTitle2)+aEntry[1].replace("الحلقة "," E")
            siteUrl = str(aEntry[0])
            sThumbnail = sThumbnail
            sInfo = ""
 
            #print sUrl
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            

 
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
 
        progress_.VSclose(progress_)
    sPattern = '<a class="hoverable activable" href="([^<]+)">([^<]+)</a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    


    #print aResult
   
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = str(sMovieTitle)+aEntry[1].replace("موسم "," S")
            siteUrl = str(aEntry[0])
            sThumbnail = sThumbnail
            sInfo = ""
 
            #print sUrl
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sMovieTitle2', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            

 
            oGui.addEpisode(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
 
        progress_.VSclose(progress_)
    # .+? ([^<]+)
    sPattern = '<a title="([^<]+)" href="([^<]+)"><div class="Quality".+?</span></div><span>([^<]+)</span>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
  

    #print aResult
   
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[0].decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            siteUrl = str(aEntry[1])
            sThumbnail = aEntry[2]
            sInfo = aEntry[2]
 
            #print sUrl
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            

 
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
 
        progress_.VSclose(progress_)
       
    oGui.setEndOfDirectory() 
  
def showEps():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sMovieTitle2 = oInputParameterHandler.getValue('sMovieTitle2')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')



    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    sHtmlContent = oRequestHandler.request()
    # (.+?) .+? ([^<]+)   
    sPattern = '<a class="hoverable activable.+?href="([^<]+)"><div class="Thumb"><span><i class="fa fa-play"></i></span></div><episodeArea><episodeTitle>([^<]+)</episodeTitle></episodeArea></a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    


    #print aResult
   
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = str(sMovieTitle2)+aEntry[1].replace("الحلقة ","E")
            siteUrl = str(aEntry[0])
            sThumbnail = sThumbnail
            sInfo = ""
 
            #print sUrl
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            

 
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
    # .+? ([^<]+)
    sPattern = '<a title="([^<]+)" href="([^<]+)"><div class="Quality".+?</span></div><span>([^<]+)</span>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
  

    #print aResult
   
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[0].decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            siteUrl = str(aEntry[1])
            sThumbnail = aEntry[2]
            sInfo = aEntry[2]
 
            #print sUrl
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            

 
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
 
        progress_.VSclose(progress_)
       
    oGui.setEndOfDirectory() 


def showEpisodes():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')



    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    sHtmlContent = oRequestHandler.request()
     # .+? ([^<]+)
    sPattern = '<a href="([^<]+)"><div class="MycimaBlockafter"></div><img data-src="([^<]+)" width=".+?" height=".+?" alt="([^<]+)" /><figcaption>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 


            sTitle = aEntry[2].decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            siteUrl = str(aEntry[0])
            sThumbnail = str(aEntry[1])
            sInfo = ""
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
       
    oGui.setEndOfDirectory()
	 
def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')



    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    sHtmlContent = oRequestHandler.request()

    # ([^<]+) .+?
               

    sPattern = '<btn data-url="([^<]+)" class="hoverable activable">'
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
				url = url.replace("uppom","ddsdd")
				sTitle =  ""
				if url.startswith('//'):
					url = 'http:' + url
				
					
            
				sHosterUrl = url 
				oHoster = cHosterGui().checkHoster(sHosterUrl)
				if (oHoster != False):
					oHoster.setDisplayName(sMovieTitle)
					oHoster.setFileName(sMovieTitle)
					cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				

			progress_.VSclose(progress_)  

    # ([^<]+) .+?

    sPattern = 'class="hoverable activable" href="([^<]+)"><quality>([^<]+)</quality><resolution><i class=".+?"></i>([^<]+)</resolution>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if (aResult[0] == True):
			total = len(aResult[1])
			progress_ = progress().VScreate(SITE_NAME)
			for aEntry in aResult[1]:
				progress_.VSupdate(progress_, total)
				if progress_.iscanceled():
					break
            
				url = str(aEntry[0])
				url = url.replace("uppom","ddsdd")
				sTitle = sMovieTitle+' ['+str(aEntry[2])+str(aEntry[1])+'] '
				if url.startswith('//'):
					url = 'http:' + url
				
					
            
				sHosterUrl = url 
				oHoster = cHosterGui().checkHoster(sHosterUrl)
				if (oHoster != False):
					oHoster.setDisplayName(sTitle)
					oHoster.setFileName(sMovieTitle)
					cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				

			progress_.VSclose(progress_)  
                
    oGui.setEndOfDirectory()