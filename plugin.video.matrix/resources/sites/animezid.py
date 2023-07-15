# -*- coding: utf-8 -*-
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

SITE_IDENTIFIER = 'animezid'
SITE_NAME = 'Animezid'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

KID_MOVIES = (URL_MAIN + '/category.php?cat=movies', 'showMovies')
KID_CARTOON = (URL_MAIN + '/category.php?cat=series', 'showSeries')


URL_SEARCH = (URL_MAIN + '/search.php?keywords=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '/search.php?keywords=', 'showMoviesSearch')
URL_SEARCH_SERIES = (URL_MAIN + '/search.php?keywords=', 'showSeriesSearch')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Search Movies', icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', 'SEARCH SERIES', icons + '/Search.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', icons + '/Cartoon.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', KID_CARTOON[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات كرتون', icons + '/Cartoon.png', oOutputParameterHandler)
  
    oGui.setEndOfDirectory()
 
def showSearchSeries():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/search.php?keywords='+sSearchText
        showSeriesSearch(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/search.php?keywords='+sSearchText
        showSeriesSearch(sUrl)
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
    oParser = cParser()
    sStart = '<div id="movies" class="movies">'
    sEnd = '<div class="clearfix"></div>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
# ([^<]+) .+? (.+?)
    sPattern = '<a href="(.+?)" class=.+?data-src="(.+?)">.+?class="title">(.+?)</span>'

    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if "فيلم" not in aEntry[2]:
                continue
 

            sTitle = aEntry[2].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("برنامج","").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","")
            siteUrl = aEntry[0].replace('watch.php?','play.php?')
            sDesc = ''
            sThumb = aEntry[1]

			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler) 

        
        progress_.VSclose(progress_)
 
    if not sSearch:
        oGui.setEndOfDirectory() 
			
def showSeriesSearch(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
    sStart = '<div id="movies" class="movies">'
    sEnd = '<div class="clearfix"></div>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
# ([^<]+) .+? (.+?)
    sPattern = '<a href="(.+?)" class=.+?data-src="(.+?)">.+?class="title">(.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if "فيلم" in aEntry[2]:
                continue
 

            sTitle = aEntry[2].replace("مدبلجة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("والأخيرة","").replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("موسم","S").replace("الحلقة "," E")
            siteUrl = aEntry[0].replace('watch.php?','play.php?')
            sDesc = ''
            sThumb = aEntry[1]

			

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            if 'category.php' in siteUrl:
                oGui.addEpisode(SITE_IDENTIFIER, 'showEpisodes2', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc,  oOutputParameterHandler)

        
        progress_.VSclose(progress_)
 
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
    
    soup = BeautifulSoup(sHtmlContent, "html.parser")
            
    Sections = soup.findAll("div",{"id":"movies"})
    sHtmlContent2 = Sections[1]
    #VSlog(sHtmlContent)
    sPattern = '<a class=\"movie\" href=\"(.+?)\" title=\"(.+?)\">.*\s*.*\s*.*data-src=\"(.+?)\"/>'
    aResult = [True,re.findall(sPattern,str(sHtmlContent2))]
    #VSlog(aResult)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler() 

        for aEntry in aResult[1]:
            #VSlog(aEntry)
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            sTitle = aEntry[1].replace("!","").replace("'","").replace('"','').replace("&","")
            #VSlog("Adding" + sTitle)
            siteUrl = aEntry[0].replace('watch.php?','play.php?')
            #VSlog(siteUrl)
            sDesc = ''
            sThumb = aEntry[2]
            #VSlog(sThumb)
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler) 

    progress_.VSclose(progress_)
    
    sNextPage = __checkForNextPage(sHtmlContent)
    VSlog('nEXTpAGE' + str(sNextPage))
    if sNextPage:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sNextPage)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', icons + '/next.png', oOutputParameterHandler)
        
    oGui.setEndOfDirectory()

    

    
    
    # if not sSearch:
        # oGui.setEndOfDirectory()
    # oParser = cParser()
# # ([^<]+) .+? (.+?)
    # sPattern = 'href=\"(.+?)\".title=\"(.+?)\".+?\n.+?\n.+?data-src=\"(.+?)\".+?\n.+?\n.+?span>(.+?)</span>'
    # aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    # if aResult[0]:
        # total = len(aResult[1])
        # progress_ = progress().VScreate(SITE_NAME)
        # oOutputParameterHandler = cOutputParameterHandler() 
        # for aEntry in aResult[1]:
            # progress_.VSupdate(progress_, total)
            # if progress_.iscanceled():
                # break
 

            # sTitle = aEntry[1] 
            # siteUrl = aEntry[0]
            # sDesc = ''
            # sThumb = aEntry[2]

			
            # oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            # oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            # oOutputParameterHandler.addParameter('sThumb', sThumb)
            # oGui.addMisc(SITE_IDENTIFIER, 'showMoviesLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler) 

        
        # progress_.VSclose(progress_)
 
    # if not sSearch:
        # oGui.setEndOfDirectory() 

def showMoviesLinks(sSearch = ''):
    
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    

 # ([^<]+) .+?
    sPattern = '<a href="([^<]+)" class="movie" title="([^<]+)">.+?data-src="([^<]+)">'

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
 
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("برنامج","").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
            siteUrl = aEntry[0].replace('watch.php?','play.php?')
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
            oOutputParameterHandler.addParameter('sYear', sYear)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMoviesLinks', '[COLOR teal]Next >>>[/COLOR]', icons + '/next.png', oOutputParameterHandler)
 
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
    
    soup = BeautifulSoup(sHtmlContent, "html.parser")
            
    sHtmlContent = soup.findAll("div",{"id":"movies"})
    sHtmlContent = sHtmlContent[1]
    #VSlog(sHtmlContent)
    #oParser = cParser()
    # sStart = '<div class=\"clearfix\"></div>\n.+?<div id=\"movies\" class=\"movies\">'
    # sEnd = '<div class="row"></div>'
    # sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
# ([^<]+) .+? (.+?)
    sPattern = 'href=\"(.+?)\" title=\"(.+?)\">\n.+?\n.+data-src=\"(.+?)\"/>\n.+?title\">(.+?)\.+</span>'
    aResult = [True,re.findall(sPattern,str(sHtmlContent))]
    #oParser.parse(sHtmlContent, sPattern)
    #VSlog(aResult)
    itemList =[]
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        VSlog(aResult)
        for aEntry in aResult[1]:
            VSlog(aEntry)
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
        
            sTitle = aEntry[1]
            
            sTitle = sTitle.replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("برنامج","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","").replace("مدبلجة","").split("الموسم")[0]
            
            sDisplayTitle = sTitle.split("الحلقة")[0].split("الحلقه")[0].strip()
            siteUrl = aEntry[0]
            sDesc = ''
            sThumb = aEntry[2]

            if sDisplayTitle not in itemList:
                itemList.append(sDisplayTitle)
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addTV(SITE_IDENTIFIER, 'showSeriesLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler) 

        
        progress_.VSclose(progress_)
 
    #if not sSearch:
    oGui.setEndOfDirectory()
 
def showSeriesLinks():
    
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
    # sStart = '<div id="movies" class="movies">'
    # sEnd = '<div class="clearfix"></div>'
    # sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    soup = BeautifulSoup(sHtmlContent, "html.parser")
            
    sHtmlContent = soup.findAll("div",{"class":"Tab tab-seasons"})
    #VSlog(sHtmlContent)
  # ([^<]+) .+? (.+?)
    SeasonsPattern = 'data-serie=\"(.+?)\">(.+?)</li>'
    aResult = oParser.parse(sHtmlContent, SeasonsPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            sTitle =  aEntry[1]
            siteUrl = sUrl+'SEASON'+str(aEntry[0])
            sThumb = sThumb
            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
    
    # sPattern = '<a href="(.+?)" class=.+?data-src="(.+?)">.+?class="title">(.+?)</span>'
    # aResult = oParser.parse(sHtmlContent, sPattern)

    # itemList =[]
    # if aResult[0]:
        # oOutputParameterHandler = cOutputParameterHandler() 
        # for aEntry in aResult[1]:
            # #if 'ديزني' or 'افلام' or 'أفلام' or 'كرتون' or 'مسلسلات' or 'رمضان' or 'اطفال' not in aEntry[2]:
            # sTitle =  aEntry[2].replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").split("الحلقة")[0].strip()
            # siteUrl = aEntry[0]
            # sThumb = aEntry[1]
            # sDesc = ''
            

            # if sTitle not in itemList:
                # itemList.append(sTitle)
                # oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                # oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                # oOutputParameterHandler.addParameter('sThumb', sThumb)
                # oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()

 
def showEpisodes():
    
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    SeasonID = sUrl.split("SEASON")[1]
    sUrl = sUrl.split("SEASON")[0]
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    soup = BeautifulSoup(sHtmlContent, "html.parser")
            
    sHtmlContent = soup.findAll("div",{"data-serie":SeasonID})
    VSlog(sHtmlContent)
    
    oParser = cParser()
    # sStart = '<div id="movies" class="movies">'
    # sEnd = '<div class="clearfix"></div>'
    # sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

  # ([^<]+) .+? (.+?)
    sPattern = '<a href=\"(.+?)\">.+?<em>(.+?)</em>'
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
 
            sTitle =  'E' + aEntry[1]
            siteUrl = URL_MAIN + aEntry[0].replace('watch.php?','play.php?')
            sThumb = sThumb
            sDesc = ''
			

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            if 'category.php' in siteUrl:
                oGui.addEpisode(SITE_IDENTIFIER, 'showEpisodes2', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc,  oOutputParameterHandler)

    oGui.setEndOfDirectory()

 
def showEpisodes2():
    
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
    sStart = '<div id="movies" class="movies">'
    sEnd = '<div class="clearfix"></div>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
  # ([^<]+) .+?
    sPattern = '<a href="(.+?)" class="movie" title="(.+?)">.+?data-src="(.+?)">'
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
 
            sTitle =  aEntry[1].replace("مدبلجة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("والأخيرة","").replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("موسم","S").replace("الحلقة "," E")
            siteUrl = aEntry[0].replace('watch.php?','play.php?')
            sThumb = aEntry[2]
            sDesc = ""
			

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc,  oOutputParameterHandler)

    oGui.setEndOfDirectory()	
def __checkForNextPage(sHtmlContent):
    soup = BeautifulSoup(sHtmlContent, "html.parser")
            
    Sections = soup.find("ul",{"class":"pagination pagination-sm pagination-arrows"})
    
    currentpage = Sections.find("li",{"class":"active"}).a
    VSlog('currentpage: ' + str(currentpage.text))
    nextpages = Sections.findAll("li",{"class":""})
    
    if nextpages:
        for page in nextpages:
            #VSlog(page.a.text)
            #VSlog(page.a['href'])
            if '«' not in page.a.text:
                if int(page.a.text)-int(currentpage.text) ==1:
                    if int(page.a.text) > int(currentpage.text):
                        VSlog("Next Page: " + URL_MAIN+page.a['href'])
                        return URL_MAIN+page.a['href']
    
    return False
    # sPattern = '<li class=\"\">.*\s*<a href=\"(.+?)\">(\d*)</a>'
	
    # oParser = cParser()
    # aResult = oParser.parse(sHtmlContent, sPattern)
    # #VSlog(aResult[1][0])
    
    # if aResult[0]:
        # for res in aResult[1]:
            # if int(res[1])-currentpage ==1:
                # return URL_MAIN+'/'+res[1]

    # return False

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    #VSlog(sUrl)
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    #VSlog(sHtmlContent)
    # (.+?) .+? ([^<]+)
               

    sPattern = 'data-embed=\"(.+?)\">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if aResult[0]:
            for aEntry in aResult[1]:
        
                url = aEntry.replace("+","")
                #sTitle = re.findall('https://(.+?)\.[com|co|org|net|biz|nl|ps]',url)[0]
                if url.startswith('//'):
                   url = 'https:' + url
				
					
            
                sHosterUrl = url 
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
               

    sPattern = 'iframe.+?src=\"(.+?)\".+?target=\"_blank\"'
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if aResult[0]:
            for aEntry in aResult[1]:
        
                url = aEntry[0].replace("+","")
                #sTitle = re.findall('https://(.+?)\.[com|co|org|net|biz|nl|ps]',url)[0]
                if url.startswith('//'):
                   url = 'https:' + url
				
					
            
                sHosterUrl = url 
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
				
                
    oGui.setEndOfDirectory()