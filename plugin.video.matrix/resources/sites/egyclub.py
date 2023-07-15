#-*- coding: utf-8 -*-
#zombi https://github.com/zombiB/zombi-addons/
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser
from resources.lib.util import Quote
from bs4 import BeautifulSoup
import re
import requests

ADDON = addon()
icons = ADDON.getSetting('defaultIcons')

SITE_IDENTIFIER = 'egyclub'
SITE_NAME = 'Egyclub'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
MOVIE_EN = ('https://www.egy-club.com/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%a7%d8%ac%d9%86%d8%a8%d9%8a', 'showMovies', 2)
MOVIE_HI = ('https://www.egy-club.com/category/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D9%87%D9%86%D8%AF%D9%8A', 'showMovies', 6)

MOVIE_TURK = ('https://www.egy-club.com/category/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%AA%D8%B1%D9%83%D9%8A', 'showMovies')
KID_MOVIES = ('https://www.egy-club.com/category/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%A7%D9%86%D9%8A%D9%85%D9%8A%D8%B4%D9%86', 'showMovies')

MOVIE_CLASSIC = ('https://www.egy-club.com/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d9%83%d9%84%d8%a7%d8%b3%d9%8a%d9%83%d9%8a%d8%a9-%d8%b9%d8%a7%d9%84%d9%85%d9%8a%d8%a9', 'showMovies')
SERIE_EN = ('https://www.egy-club.com/allseries/', 'showSeries')
DOC_NEWS = ('https://www.egy-club.com/category/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d9%88%d8%ab%d8%a7%d8%a6%d9%82%d9%8a%d8%a9', 'showMovies')


URL_SEARCH = ('https://www.egy-club.com/?s=', 'showMovies')
URL_SEARCH_MOVIES = ('https://www.egy-club.com/?s=', 'showMovies')
URL_SEARCH_SERIES = ('https://www.egy-club.com/?s=%D9%85%D8%B3%D9%84%D8%B3%D9%84+', 'showSeries')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'SEARCH_MOVIES', icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', 'SEARCH_SERIES', icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', icons + '/MoviesEnglish.png', oOutputParameterHandler)
           
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', icons + '/Hindi.png', oOutputParameterHandler)
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية', icons + '/Turkish.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_CLASSIC[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كلاسيكية', icons + '/Movies.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية', icons + '/TVShowsEnglish.png', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = 'https://www.egy-club.com/?s='+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = 'https://www.egy-club.com/?s=%D9%85%D8%B3%D9%84%D8%B3%D9%84+'+sSearchText
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
    pN = 0
    
    if 'Custom' in sUrl:
        nParams = sUrl.replace("Custom","").split(",")
        VSlog(nParams)
        
        s = requests.Session()  
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
							'Referer': Quote(nParams[0])}
        dynamicurl = '/wp-content/themes/Final/Interface/Ajax/archive/block.php'

       # # --شوف وين لازم ينحح التيرم اي دي والسلج
        psearch = nParams[0].rsplit('category/')[1].replace('/','')
        VSlog("PN/Slug/termid : " + str([nParams[1],psearch,nParams[3]]))
        pN = int(nParams[1]) + 20
        data = {'category=':nParams[2] ,'termid':nParams[3], 'offset':pN}
        r = s.post(URL_MAIN + dynamicurl, headers=headers,data = data)
        sHtmlContent = r.content.decode('utf8',errors='ignore')
        #sHtmlContentfull = r.content.decode('utf8')
    else:
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        
        
    #VSlog(sHtmlContent)
 # (.+?) ([^<]+) .+?
    #sPattern = '<div class=\"BlockItem\">.+?<a href=\"(.+?)\".+?src=\"(.+?)\".*?TitleBlockMovieNormal..(.+?)</div'
    sPattern = '<div class=\"BlockItem\">.+?<a href=\"(.+?)\".+?src=\"(.+?)\".*?(TitleBlockMovieNormal InFilmBlock|TitleBlockMovieNormal)..(.+?)</div'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    #VSlog(aResult)
    
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            # if "فيلم" not in aEntry[2]:
                # continue
            
            sTitle = aEntry[3].replace("مشاهدة","").replace("اونلاين","").replace("مشاهده","").replace("مترجمة","").replace("مسلسل","").replace("انمي","").replace("مترجم","").replace("كاملة","").replace("جودة عالية","").replace("كامل","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("أون لاين","")
            #VSlog(sTitle)
            siteUrl = aEntry[0]
            #VSlog(siteUrl)
            sThumb = aEntry[1]
            #VSlog(sThumb)
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle) 
            oOutputParameterHandler.addParameter('sYear', sYear)                  
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            
            oGui.addMovie(SITE_IDENTIFIER, 'showServers', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
     
    #if not sSearch:
        #sNextPage = __checkForNextPage(sHtmlContent)
        #if sNextPage:
    pattern = "\"slug\":'(.+?)',.*\s*\"termid\":'(\d)',"
    oParser = cParser()
    sParam = oParser.parse(sHtmlContent, pattern)
    
    if sParam[0]:
        sParams = 'Custom' + sUrl+','+str(pN)+','+sParam[1][0][0]+','+sParam[1][0][1]

        oOutputParameterHandler = cOutputParameterHandler()
        #oOutputParameterHandler.addParameter('siteUrl', sUrl.split("page")[0]+'page' + str(pN))
        oOutputParameterHandler.addParameter('siteUrl', sParams)
        
        #VSlog("NEXT PAGE: " + str(sParams))
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', icons + '/next.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()
 
def __checkForNextPage(sHtmlContent):
    sPattern = 'class="next page-numbers" href="(.+?)">'
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if aResult[0]:
        
        return URL_MAIN+aResult[1][0]

    return False 
 
def showSeries(sSearch = ''):
    import requests
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    try:
        JUMP = int(sUrl.split('JUMP')[1])
    except:
        JUMP = 0
        
    dynamicurl ='/wp-content/themes/Final/Filters/Sections.php'
    s = requests.Session()  
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
                        'Referer': Quote(SERIE_EN[1])}

    # psearch = nParams[0].rsplit('category/')[1].replace('/','')
    # VSlog("PN/Slug/termid : " + str([nParams[1],psearch,nParams[3]]))
    # pN = int(nParams[1]) + 20
    data = {'offset':0+JUMP}
    r = s.post(URL_MAIN + dynamicurl, headers=headers,data = data)
    sHtmlContent = r.content.decode('utf8',errors='ignore')
    #oRequestHandler = cRequestHandler(sUrl)
    #sHtmlContent = oRequestHandler.request()
    
 # ([^<]+) .+? (.+?)
    sPattern = '<div class=\"BlockItem\">.+?<a href=\"(.+?)\".+?src=\"(.+?)\".*?(TitleBlockMovieNormal InFilmBlock|TitleBlockMovieNormal)..(.+?)</div'

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
            if "فيلم" in aEntry[1]:
                continue
 
            sTitle = aEntry[3].replace("مشاهدة","").replace("اونلاين","").replace("مترجمة","").replace("مسلسل","").replace("انمي","").replace("مترجم","").replace("كامل","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("كامل","").replace("والاخيرة","")
            siteUrl = aEntry[0]
            sThumb = aEntry[1]
            sDesc = ''
            sYear = ''
            sDisplayTitle = sTitle.replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace("الموسم الثاني","S2").replace("الموسم الثانى","S2").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الحلقة "," E").replace("حلقة "," E").replace("الموسم","S").replace("S ","S").replace("موسم","S").replace("S ","S")

            if sDisplayTitle not in itemList:
                itemList.append(sDisplayTitle)
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sYear', sYear)
                if sSearch:
                   oGui.addEpisode(SITE_IDENTIFIER, 'showServers', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
                if not sSearch:
                   oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        
 
 
    if not sSearch:
        # sNextPage = __checkForNextPage(sHtmlContent)
        # if sNextPage:
            # oOutputParameterHandler = cOutputParameterHandler()
            # oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            # oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', icons + '/next.png', oOutputParameterHandler)
            
        oOutputParameterHandler = cOutputParameterHandler()
        #oOutputParameterHandler.addParameter('siteUrl', sUrl.split("page")[0]+'page' + str(pN))
        oOutputParameterHandler.addParameter('siteUrl', sUrl.split('JUMP')[0]+'JUMP'+str(20))
        
        #VSlog("NEXT PAGE: " + str(sParams))
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', icons + '/next.png', oOutputParameterHandler)
        oGui.setEndOfDirectory() 
  
def showEpisodes():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    # .+? ([^<]+) (.+?)
    sPattern = '<div class="film_block"><a href="(.+?)" title="(.+?)"><div'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
   
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
 
            sTitle = aEntry[1].replace("الجزء","الموسم").replace("مترجمة","").replace("اونلاين","").replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("انمى","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("كامل","").replace("مشاهدة وتحميل","").replace("اون لاين","").replace("جميع حلقات","").replace("والأخيرة","").replace("والاخيرة","").replace("الأخيرة","").replace("الاخيرة","").replace("والاخيرة","")
            
            siteUrl = aEntry[0]
            sThumb = sThumb
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')
            sDisplayTitle = sTitle.replace("الموسم العاشر","S10").replace("الموسم الحادي عشر","S11").replace("الموسم الثاني عشر","S12").replace("الموسم الثالث عشر","S13").replace("الموسم الرابع عشر","S14").replace("الموسم الخامس عشر","S15").replace("الموسم السادس عشر","S16").replace("الموسم السابع عشر","S17").replace("الموسم الثامن عشر","S18").replace("الموسم التاسع عشر","S19").replace("الموسم العشرون","S20").replace("الموسم الحادي و العشرون","S21").replace("الموسم الثاني و العشرون","S22").replace("الموسم الثالث و العشرون","S23").replace("الموسم الرابع والعشرون","S24").replace("الموسم الخامس و العشرون","S25").replace("الموسم السادس والعشرون","S26").replace("الموسم السابع والعشرون","S27").replace("الموسم الثامن والعشرون","S28").replace("الموسم التاسع والعشرون","S29").replace("الموسم الثلاثون","S30").replace("الموسم الحادي و الثلاثون","S31").replace("الموسم الثاني والثلاثون","S32").replace("الموسم الاول","S1").replace(" الثانى","2").replace("الموسم الثاني","S2").replace("الموسم الثالث","S3").replace("الموسم الثالث","S3").replace("الموسم الرابع","S4").replace("الموسم الخامس","S5").replace("الموسم السادس","S6").replace("الموسم السابع","S7").replace("الموسم الثامن","S8").replace("الموسم التاسع","S9").replace("الحلقة "," E").replace("حلقة "," E").replace("الموسم","S").replace("S ","S")
 
            oOutputParameterHandler.addParameter('siteUrl', aEntry[0])
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear) 
            

 
            oGui.addEpisode(SITE_IDENTIFIER, 'showServers', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', '[COLOR teal]Next >>>[/COLOR]', icons + '/next.png', oOutputParameterHandler)
 
       
    oGui.setEndOfDirectory() 
 
def showServers():
    import requests
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    #VSlog(sHtmlContent)
    
    
    #Recuperation infos
    sId = ''
     # (.+?) ([^<]+) .+?
    
    oParser = cParser()
    sPattern = 'post&current_page_id=(.+?)&search_query'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
   
    if aResult[0]:
        sTitle = 'server '
        siteUrl = URL_MAIN + '/wp-content/themes/Final/Interface/Ajax/single/firstserver.php'
        hdr = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0','referer' : 'https://www.egy-club.com/'}
        params = {'id':aResult[1][0]}#,'i':aEntry[0]}
        St=requests.Session()
        sHtmlContent2 = St.post(siteUrl,headers=hdr,data=params)
        sHtmlContent2 = sHtmlContent2.content
        #VSlog(sHtmlContent2)
        sPattern = '<tr>.+?<td>(.+?)</td>.+?<a href=\"(.+?)\"'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent2, sPattern)
        VSlog(aResult)
        if aResult[0]:
            for aEntry in aResult[1]:
        
                url = aEntry9[1]
                sTitle = aEntry[0]#sMovieTitle
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
                   oHoster.setDisplayName(sMovieTitle)
                   oHoster.setFileName(sMovieTitle)
                   cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    # # (.+?) .+? ([^<]+)        	
    # sPattern = 'href="([^<]+)" rel="nofollow" class="download'
		
    # oParser = cParser()
    # aResult = oParser.parse(sHtmlContent, sPattern)

	
    # if aResult[0]:
        # for aEntry in aResult[1]:
            
            # url = aEntry
            # sTitle = ""
            # sThumb = sThumb
            # if url.startswith('//'):
               # url = 'http:' + url
				
				            
            # sHosterUrl = url 
            # if 'userload' in sHosterUrl:
                # sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            # if 'moshahda' in sHosterUrl:
                # sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
            # if 'mystream' in sHosterUrl:
                # sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN  
            # oHoster = cHosterGui().checkHoster(sHosterUrl)
            # if oHoster:
               # oHoster.setDisplayName(sMovieTitle)
               # oHoster.setFileName(sMovieTitle)
               # cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
				
                
                
    oGui.setEndOfDirectory()