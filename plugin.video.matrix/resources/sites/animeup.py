# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import VSlog, siteManager, addon
from resources.lib.parser import cParser
from bs4 import BeautifulSoup

ADDON = addon()
icons = ADDON.getSetting('defaultIcons')

SITE_IDENTIFIER = 'animeup'
SITE_NAME = 'Anime4up'
SITE_DESC = 'arabic vod'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)


ANIM_NEWS = (URL_MAIN + '/anime-type/tv2/', 'showSeries')
ANIM_MOVIES = (URL_MAIN + '/anime-type/movie-3/', 'showMovies')
ANIM_SUB = (URL_MAIN + '/anime-category/%d8%a7%d9%84%d8%a7%d9%86%d9%85%d9%8a-%d8%a7%d9%84%d9%85%d8%aa%d8%b1%d8%ac%d9%85/', 'showSeries')
ANIM_DUBBED = (URL_MAIN + '/anime-category/%d8%a7%d9%84%d8%a7%d9%86%d9%85%d9%8a-%d8%a7%d9%84%d9%85%d8%af%d8%a8%d9%84%d8%ac/', 'showSeries')

URL_SEARCH = (URL_MAIN + '/?search_param=animes&s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '/?search_param=animes&s=', 'showMovies')
URL_SEARCH_ANIMS = (URL_MAIN + '/?search_param=animes&s=', 'showSeries')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'SEARCH_MOVIES', icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', 'SEARCH_SERIES', icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'افلام الانمي', icons + '/Anime.png', oOutputParameterHandler)
  
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات إنمي', icons + '/Anime.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_DUBBED[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'انمي مدبلج', icons + '/Dubbed.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_SUB[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'انمي مترجم', icons + '/Subtitled.png', oOutputParameterHandler)
            
    oGui.setEndOfDirectory()
             
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/?search_param=animes&s='+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
		
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/?search_param=animes&s='+sSearchText
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
    #VSlog(sUrl)
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 # ([^<]+) .+? (.+?)
    sPattern = '<img class="img-responsive" src="([^<]+)" alt="([^<]+)" />.+?href="([^<]+)" class="overlay"></a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
 
            sTitle = aEntry[1].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","").replace("مدبلج","").replace("مدبلجة","").replace("مدبلجه","").replace("الفلم","").replace("الفيلم","").replace("فلم","").replace("فيلم","").replace("مسلسل","").replace("للعربية","")
            
            siteUrl = aEntry[2]
            #VSlog(siteUrl)
            s1Thumb = aEntry[0]
            sThumb = re.sub(r'\?resize=.*\s*','',s1Thumb)
            sYear = ""
            sDesc = ""


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()

def toDict(lst):
   res_dict = {}
   for i in range(0, len(lst), 2):
       res_dict[lst[i]] = lst[i + 1]
   return res_dict
   
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
    sPattern = '<img class=\"img-responsive\" src=\"(.+?)\" alt=\"(.+?)\".*?\s*?<a href=\"(.+?)\" class.*?\s?.*?\s.*?anime-status/complete/\">(.+?)</a>.*\s*.*\s*.*\s*.*?\s*?.*?data-content=\"(.+?)\">'
    # oParser = cParser()
    # aResult = oParser.parse(sHtmlContent, sPattern)
    matches = re.findall(sPattern, sHtmlContent)
    aResult = [True,matches]
    ##VSlog(aResult)
    ##VSlog(sHtmlContent)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
 
            sTitle = aEntry[1].replace("الجزء","الموسم").replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الموسم","S").replace("موسم","S").replace("S ","S").replace("مدبلج","").replace("مدبلجة","").replace("مدبلجه","").replace("الفلم","").replace("الفيلم","").replace("فلم","").replace("فيلم","").replace("مسلسل","").replace("للعربية","")
            
            siteUrl = aEntry[2]
            s1Thumb = aEntry[0]
            sThumb = re.sub(r'\?resize=.*\s*','',s1Thumb)
            sReleased = aEntry[3]
            sYear = ""
            sDesc = aEntry[4]

            if 'لم يعرض' not in sReleased:
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sYear', sYear)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                
                oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
                

 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)
 
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
     # (.+?) ([^<]+) .+?
    sPattern = '<h3><a href=\"([^<]+)\">([^<]+)</a></h3>.*?\s*?.*?\s*?.*?src=\"(.+?)\" alt'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
 
            sTitle = aEntry[1].replace("الحلقة "," E").replace("حلقة "," E").replace("الأخيرة","")
            sTitle = sMovieTitle+sTitle
            siteUrl = aEntry[0]
            s1Thumb = aEntry[2]
            sThumb = re.sub(r'\?resize=.*\s*','',s1Thumb)
            sDesc = ""
			

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
		
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<a class="next page-numbers" href="([^<]+)">'
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0]:
        
        return aResult[1][0]

    return False

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    VSlog(sUrl)
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()       


    # (.+?) .+? ([^<]+)
               

    # sPattern = 'data-ep-url="([^<]+)">'
    # oParser = cParser()
    # aResult = oParser.parse(sHtmlContent, sPattern)

	
    # if aResult[0]:
            # oOutputParameterHandler = cOutputParameterHandler() 
            # for aEntry in aResult[1]:
        
                # url = aEntry
                # if url.startswith('//'):
                    # url = 'https:' + url
				
					
            
                # sHosterUrl = url 
                # if 'userload' in sHosterUrl:
                    # sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                # if 'moshahda' in sHosterUrl:
                    # sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                # if 'mystream' in sHosterUrl:
                    # sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
                # oHoster = cHosterGui().checkHoster(sHosterUrl)
                # if oHoster:
                    # sDisplayTitle = sMovieTitle
                    # oHoster.setDisplayName(sDisplayTitle)
                    # oHoster.setFileName(sMovieTitle)
                    # cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    # sPattern = '<a href="(.+?)" target="_blank"><i class="fa fa-star"></i><span>.+?</span><span>(.+?)</span></a>' 
    # aResult = re.findall(sPattern, sHtmlContent)
    # VSlog(aResult)
    
    # if aResult:
        # for aEntry in aResult:
            
            # url = aEntry[0]
            # sTitle = sMovieTitle+'('+aEntry[1]+')'
            
            # sHosterUrl = url
            # if '?download_' in sHosterUrl:
                # sHosterUrl = sHosterUrl.replace("moshahda","ffsff")
                # sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            # if 'moshahda' in sHosterUrl:
                # sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            # if 'mystream' in sHosterUrl:
                # sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
            # oHoster = cHosterGui().checkHoster(sHosterUrl)
            # if oHoster:
                # oHoster.setDisplayName(sTitle)
                # oHoster.setFileName(sMovieTitle)
                # cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
                
    soup = BeautifulSoup(sHtmlContent, "html.parser")
    Qualities = soup.findAll("ul",{"class":"quality-list"})

    
    aResult = []
    QualityDict = {"SD" : "480P", "HD": "720p", "FHD": "1080p"}
    for link in Qualities:
        #VSlog (link)
        
        QL = link.li.text.replace("الجودة المتوسطة","").replace("الجودة العالية","").replace("الجودة الخارقة","").strip()
        #VSlog(QL)
        sPattern = 'class=\"btn btn-default\" href=\"([^<]+)\" target.+?>([^<]+)</a>' 
        aResult = re.findall(sPattern, str(link))
        #VSlog(aResult)     
	
        if aResult:
            for aEntry in aResult:
                
                url = aEntry[0]
                sTitle = '('+aEntry[1]+')'
                sDisplayName = ('%s  [COLOR coral]%s[/COLOR]') % (sMovieTitle, QualityDict[QL])
                
                sHosterUrl = url
                if '?download_' in sHosterUrl:
                    sHosterUrl = sHosterUrl.replace("moshahda","ffsff")
                    sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
                if 'moshahda' in sHosterUrl:
                    sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
                if 'mystream' in sHosterUrl:
                    sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN 
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sDisplayName)
                    oHoster.setFileName(sTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, icons + '/resolution/' + QualityDict[QL] + ".png")
                
    oGui.setEndOfDirectory()	