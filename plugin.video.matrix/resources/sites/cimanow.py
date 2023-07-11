# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/
#############################################################
# Yonn1981 https://github.com/Yonn1981/Repo
#############################################################
# big thx to Rgysoft for this code
# From this url https://gitlab.com/Rgysoft/iptv-host-e2iplayer/-/blob/master/IPTVPlayer/tsiplayer/host_faselhd.py
#############################################################
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser

import re
import base64

ADDON = addon()
icons = ADDON.getSetting('defaultIcons')

SITE_IDENTIFIER = 'cimanow'
SITE_NAME = 'Cimanow'
SITE_DESC = 'arabic vod'

UA = 'ipad'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (URL_MAIN + '/category/افلام-اجنبية/', 'showMovies')
MOVIE_AR = (URL_MAIN + '/category/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9/', 'showMovies')

MOVIE_HI = (URL_MAIN + '/category/%d8%a7%d9%84%d8%a7%d9%81%d9%84%d8%a7%d9%85/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d9%87%d9%86%d8%af%d9%8a%d8%a9/', 'showMovies')

MOVIE_TURK = (URL_MAIN + '/category/%d8%a7%d9%84%d8%a7%d9%81%d9%84%d8%a7%d9%85/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%aa%d8%b1%d9%83%d9%8a%d8%a9/', 'showMovies')
KID_MOVIES = (URL_MAIN + '/category/افلام-انيميشن/', 'showMovies')
SERIE_TR = (URL_MAIN + '/category/%d8%a7%d9%84%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%aa%d8%b1%d9%83%d9%8a%d8%a9/', 'showSeries')

RAMADAN_SERIES = (URL_MAIN + '/category/رمضان-2023/', 'showSeries')
SERIE_EN = (URL_MAIN + '/category/%d8%a7%d9%84%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%a7%d8%ac%d9%86%d8%a8%d9%8a%d8%a9/', 'showSeries')
SERIE_AR = (URL_MAIN + '/category/%d8%a7%d9%84%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%b9%d8%b1%d8%a8%d9%8a%d8%a9/', 'showSeries')
ANIM_NEWS = (URL_MAIN + '/category/مسلسلات-انيميشن/', 'showSeries')

DOC_NEWS = (URL_MAIN + '/?s=%D9%88%D8%AB%D8%A7%D8%A6%D9%82%D9%8A', 'showMovies')

REPLAYTV_NEWS = (URL_MAIN + '/category/%d8%a7%d9%84%d8%a8%d8%b1%d8%a7%d9%85%d8%ac-%d8%a7%d9%84%d8%aa%d9%84%d9%81%d8%b2%d9%8a%d9%88%d9%86%d9%8a%d8%a9/', 'showMovies')
URL_SEARCH = (URL_MAIN + '/?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '/?s=%D9%81%D9%8A%D9%84%D9%85+', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '/?s=%D9%85%D8%B3%D9%84%D8%B3%D9%84+', 'showSeries')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'SEARCH_MOVIES', icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', 'SEARCH_SERIES', icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', icons + '/MoviesEnglish.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عربية', icons + '/Arabic.png', oOutputParameterHandler)
 
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية', icons + '/Turkish.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', icons + '/Hindi.png', oOutputParameterHandler)
   
    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', icons + '/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أجنبية',icons + '/MoviesEnglish.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات عربية',icons + '/Arabic.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية',icons + '/Turkish.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات إنمي', icons + '/Cartoon.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام وثائقية', icons + '/Documentary.png', oOutputParameterHandler) 

    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'برامج تلفزيونية',icons + '/Programs.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/category/رمضان-2022/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'رمضان 2022', icons + '/Ramadan.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '?s=%D9%81%D9%8A%D9%84%D9%85+'+sSearchText
        showMovies(sUrl)
        VSlog(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '?s=%D9%85%D8%B3%D9%84%D8%B3%D9%84+'+sSearchText
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
      


    oParser = cParser()
    oRequest = cRequestHandler(sUrl)
    oRequest.addHeaderEntry('User-Agent', UA)
    data = oRequest.request()
    

     # (.+?) ([^<]+) .+?

    if 'adilbo' in data:
        t_script = re.findall('<script.*?;.*?\'(.*?);', data, re.S)
        t_int = re.findall('/g.....(.*?)\)', data, re.S)
        if t_script and t_int:
            script = t_script[0].replace("'",'')
            script = script.replace("+",'')
            script = script.replace("\n",'')
            sc = script.split('.')
            page = ''
            for elm in sc:
                c_elm = base64.b64decode(elm+'==').decode('utf-8')
                t_ch = re.findall('\d+', c_elm, re.S)
                if t_ch:
                    nb = int(t_ch[0])+int(t_int[0])
                    page = page + chr(nb)
            VSlog(page)
 
            sPattern = '<article aria-label="post"><a href="([^"]+).+?<li aria-label="year">(.+?)</li>.+?<li aria-label="title">([^<]+)<em>.+?data-src="(.+?)" width'

            oParser = cParser()
            aResult = oParser.parse(page, sPattern)
            if aResult[0]:
                total = len(aResult[1])
                progress_ = progress().VScreate(SITE_NAME)
                oOutputParameterHandler = cOutputParameterHandler()  
                for aEntry in aResult[1]:
                    progress_.VSupdate(progress_, total)
                    if progress_.iscanceled():
                        break
 
                    sTitle = aEntry[2].replace("مشاهدة","").replace("مسلسل","").replace("مسرحية","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("برنامج","").replace("فيلم","").replace("والأخيرة","").replace("مدبلج للعربية","مدبلج").replace("والاخيرة","").replace("كاملة","").replace("حلقات كاملة","").replace("اونلاين","").replace("مباشرة","").replace("انتاج ","").replace("جودة عالية","").replace("كامل","").replace("HD","").replace("السلسلة الوثائقية","").replace("الفيلم الوثائقي","").replace("اون لاين","")
                    sTitle = str(sTitle.encode('latin-1'),'utf-8')
                    siteUrl = aEntry[0] + '/watching/'
                    sThumb = str(aEntry[3].encode('latin-1'),'utf-8')
                    
                    if sThumb.startswith('//'):
                        sThumb = 'http:' + sThumb
                    sYear = aEntry[1]
                    sDesc = ''


                    oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oOutputParameterHandler.addParameter('sYear', sYear)
                    oOutputParameterHandler.addParameter('sDesc', sDesc)
			
                    oGui.addMovie(SITE_IDENTIFIER, 'showServer', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

                progress_.VSclose(progress_)
            
            

  # ([^<]+) .+?
            sStart = '</section>'
            sEnd = '</ul>'
            page = oParser.abParse(page, sStart, sEnd)

            sPattern = '<li><a href="(.+?)">(.+?)</a>'
            oParser = cParser()
            aResult = oParser.parse(page, sPattern)
	
	
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
                    sThumb = ""


                    oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
			
                    oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, '', oOutputParameterHandler)

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
 
    oRequest = cRequestHandler(sUrl)
    oRequest.addHeaderEntry('User-Agent', UA)
    data = oRequest.request()


     # (.+?) ([^<]+) .+?

    if 'adilbo' in data:
        t_script = re.findall('<script.*?;.*?\'(.*?);', data, re.S)
        t_int = re.findall('/g.....(.*?)\)', data, re.S)
        if t_script and t_int:
            script = t_script[0].replace("'",'')
            script = script.replace("+",'')
            script = script.replace("\n",'')
            sc = script.split('.')
            page = ''
            for elm in sc:
                c_elm = base64.b64decode(elm+'==').decode()
                t_ch = re.findall('\d+', c_elm, re.S)
                if t_ch:
                    nb = int(t_ch[0])+int(t_int[0])
                    page = page + chr(nb)
            VSlog(page)

            sPattern = '<article aria-label="post"><a href="([^<]+)">.+?<li aria-label="year">(.+?)</li>.+?<li aria-label="title">([^<]+)<em>.+?data-src="(.+?)" width'


            oParser = cParser()
            aResult = oParser.parse(page, sPattern)
	
	
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
 
                    sTitle = aEntry[2]
                    sTitle = str(sTitle.encode('latin-1'),'utf-8')
                    siteUrl = aEntry[0]
                    sThumb = str(aEntry[3].encode('latin-1'),'utf-8')
                    if sThumb.startswith('//'):
                        sThumb = 'http:' + sThumb
                    sDesc = ''
                    sYear = aEntry[1]



                    oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oOutputParameterHandler.addParameter('sYear', sYear)
                    oOutputParameterHandler.addParameter('sDesc', sDesc)
			
                    oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

                progress_.VSclose(progress_)

  # ([^<]+) .+?
            sStart = '</section>'
            sEnd = '</ul>'
            page = oParser.abParse(page, sStart, sEnd)

            sPattern = '<li><a href="(.+?)">(.+?)</a>'
            oParser = cParser()
            aResult = oParser.parse(page, sPattern)
	
	
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
                    sThumb = ""


                    oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
			
                    oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, '', oOutputParameterHandler)

                progress_.VSclose(progress_)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
def showSeasons():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
 
    # (.+?) .+?  ([^<]+)
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
    sStart = '<section aria-label="seasons">'
    sEnd = '<ul class="tabcontent" id="related">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    oRequest = cRequestHandler(sUrl)
    oRequest.addHeaderEntry('User-Agent', UA)
    data = oRequest.request()
    

     # (.+?) ([^<]+) .+?

    if 'adilbo' in data:
        t_script = re.findall('<script.*?;.*?\'(.*?);', data, re.S)
        t_int = re.findall('/g.....(.*?)\)', data, re.S)
        if t_script and t_int:
            script = t_script[0].replace("'",'')
            script = script.replace("+",'')
            script = script.replace("\n",'')
            sc = script.split('.')
            page = ''
            for elm in sc:
                c_elm = base64.b64decode(elm+'==').decode()
                t_ch = re.findall('\d+', c_elm, re.S)
                if t_ch:
                    nb = int(t_ch[0])+int(t_int[0])
                    page = page + chr(nb)
            VSlog(page)
            
            oParser = cParser()
            sStart = '<section aria-label="seasons">'
            sEnd = '<ul class="tabcontent" id="related">'
            page = oParser.abParse(page, sStart, sEnd)
            
            sPattern = '<a href="([^<]+)">([^<]+)<em>'
    
            oParser = cParser()
            aResult = oParser.parse(page, sPattern)
    
   
            if aResult[0]:
                oOutputParameterHandler = cOutputParameterHandler()  
                for aEntry in aResult[1]:

                    sSeason = str(aEntry[1].encode('latin-1'),'utf-8')
                    sTitle = sMovieTitle+sSeason.replace("الموسم"," S").replace("S ","S")
                    
                    siteUrl = aEntry[0]
                    sThumb = sThumb
                    sDesc = ""
 

                    oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
            

 
                    oGui.addSeason(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 
 
def showEps():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
    sStart = '<section aria-label="seasons">'
    sEnd = '<ul class="tabcontent" id="related">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    
    oRequest = cRequestHandler(sUrl)
    oRequest.addHeaderEntry('User-Agent', UA)
    data = oRequest.request()


     # (.+?) ([^<]+) .+?

    if 'adilbo' in data:
        t_script = re.findall('<script.*?;.*?\'(.*?);', data, re.S)
        t_int = re.findall('/g.....(.*?)\)', data, re.S)
        if t_script and t_int:
            script = t_script[0].replace("'",'')
            script = script.replace("+",'')
            script = script.replace("\n",'')
            sc = script.split('.')
            page = ''
            for elm in sc:
                c_elm = base64.b64decode(elm+'==').decode()
                t_ch = re.findall('\d+', c_elm, re.S)
                if t_ch:
                    nb = int(t_ch[0])+int(t_int[0])
                    page = page + chr(nb)
            VSlog(page)
            
            oParser = cParser()
            sStart = '<section aria-label="seasons">'
            sEnd = '<ul class="tabcontent" id="related">'
            page = oParser.abParse(page, sStart, sEnd)
            
            sPattern = '<li><a href="(.+?)"><img  src="(.+?)" alt="logo" />.+?<em>(.+?)</em>'

            oParser = cParser()
            aResult = oParser.parse(page, sPattern)
    

   
            if aResult[0]:
                oOutputParameterHandler = cOutputParameterHandler()  
                for aEntry in aResult[1]:

 
                    sTitle = sMovieTitle+' E'+aEntry[2]
                    
                    siteUrl = aEntry[0] + 'watching/'
                    sThumb = str(aEntry[1].encode('latin-1'),'utf-8')
                    sDesc = ""

                    oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
            

 
                    oGui.addEpisode(SITE_IDENTIFIER, 'showServer', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
 

       
    oGui.setEndOfDirectory() 

  
def showServer():
    import requests
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    host = URL_MAIN.split('/')[2]
    VSlog(host)
 
    oRequestHandler = cRequestHandler(sUrl)
    cook = oRequestHandler.GetCookies()
    hdr = {'User-Agent' : 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Mobile Safari/537.36','Accept-Encoding' : 'gzip','cookie' : cook,'host' : host,'referer' : URL_MAIN}
    St=requests.Session()
    sHtmlContent = St.get(sUrl,headers=hdr)
    sHtmlContent = sHtmlContent.content.decode('utf8')  
    oParser = cParser()


    oRequest = cRequestHandler(sUrl)
    data = oRequest.request()


     # (.+?) ([^<]+) .+?

    if 'adilbo' in data:
        t_script = re.findall('<script.*?;.*?\'(.*?);', data, re.S)
        t_int = re.findall('/g.....(.*?)\)', data, re.S)
        if t_script and t_int:
            script = t_script[0].replace("'",'')
            script = script.replace("+",'')
            script = script.replace("\n",'')
            sc = script.split('.')
            page = ''
            for elm in sc:
                c_elm = base64.b64decode(elm+'==').decode()
                t_ch = re.findall('\d+', c_elm, re.S)
                if t_ch:
                    nb = int(t_ch[0])+int(t_int[0])
                    page = page + chr(nb)


    # (.+?) .+? ([^<]+)        	
            sPattern = '<a href="([^"]+)"><i class.+?download.+?</i>(.+?)<p'
            oParser = cParser()
            aResult = oParser.parse(page, sPattern)

	
            if aResult[0]:
                for aEntry in aResult[1]:
            
                    url = aEntry[0]
                    sTitle = aEntry[1].replace('</i>',"")
                    sTitle = ('%s  [COLOR coral]%s[/COLOR]') % (sMovieTitle, sTitle)
                    url = url.replace("cimanow","rrsrr")
                    sThumb = sThumb
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
                        oHoster.setDisplayName(sTitle)
                        oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

            sPattern = '<iframe src="([^"]+)" scrolling'
            oParser = cParser()
            aResult = oParser.parse(page, sPattern)

	
            if aResult[0]:
                for aEntry in aResult[1]:
                    url = aEntry
                    sTitle = sMovieTitle
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
                        oHoster.setDisplayName(sTitle)
                        oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

            sPattern = '<a href="([^"]+)"><i class="fa fa-download">'
            oParser = cParser()
            aResult = oParser.parse(data, sPattern)

	
            if aResult[0]:
                for aEntry in aResult[1]:
                    url = aEntry
                    sTitle = sMovieTitle
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
                        oHoster.setDisplayName(sTitle)
                        oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    #Recuperation infos
            sId = ''
            sPattern = 'data-id="([^"]+)"'
            aResult = oParser.parse(page, sPattern)
    
            if (aResult[0]):
                sId = aResult[1][0]
     # (.+?) ([^<]+) .+?

            sPattern = 'data-index="([^"]+)"'
            aResult = oParser.parse(page, sPattern)
            #VSlog(aResult)

   
            if aResult[0]:
                for aEntry in aResult[1]:

                    sTitle = 'server '
                    siteUrl = URL_MAIN + '/wp-content/themes/Cima%20Now%20New/core.php?action=switch&index='+aEntry+'&id='+sId
                    hdr = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0','host' : host,'referer' : URL_MAIN}
                    params = {'action':'switch','index':aEntry,'id':sId}
                    St=requests.Session()
                    sHtmlContent = St.get(siteUrl,headers=hdr,params=params)
                    oRequestHandler = cRequestHandler(siteUrl)
                    sData = oRequestHandler.request()
                  
                    if 'adilbo' in sData:
                        t_script = re.findall('<script.*?;.*?\'(.*?);', sData, re.S)
                        t_int = re.findall('/g.....(.*?)\)', sData, re.S)
                        if t_script and t_int:
                            script = t_script[0].replace("'",'')
                            script = script.replace("+",'')
                            script = script.replace("\n",'')
                            sc = script.split('.')
                            spage = ''
                            for elm in sc:
                                c_elm = base64.b64decode(elm+'==').decode()
                                t_ch = re.findall('\d+', c_elm, re.S)
                                if t_ch:
                                    nb = int(t_ch[0])+int(t_int[0])
                                    spage = page + chr(nb)

                            sPattern = '<iframe src="(.+?)" scrolling'
                            oParser = cParser()
                            aResult = oParser.parse(spage, sPattern)
                            if aResult[0]:
                                for aEntry in aResult[1]:
            
                                    url = aEntry
                                    sTitle = sMovieTitle
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


                
    oGui.setEndOfDirectory()
