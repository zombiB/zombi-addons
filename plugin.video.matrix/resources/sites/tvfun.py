# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/

import base64
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager
from resources.lib.parser import cParser
 
SITE_IDENTIFIER = 'tvfun'
SITE_NAME = 'tvfun'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
try:
    import requests
    url = URL_MAIN
    session = requests.Session()  # so connections are recycled
    resp = session.head(url, allow_redirects=True)
    URL_MAIN = resp.url.split('/')[2]
    URL_MAIN = 'https://' + URL_MAIN
    VSlog(URL_MAIN)
except:
    pass 
RAMADAN_SERIES = (URL_MAIN + '/ts/mosalsalat-ramadan-2022/', 'showSeries')
SERIE_TR = (URL_MAIN + '/cat/mosalsalat-torkia-FJ/', 'showSeries')
SERIE_DUBBED = (URL_MAIN + '/ts,mosalsalat--modablaja/', 'showSeries')
SERIE_HEND = (URL_MAIN + '/cat/mosalsalat-hindia-DI/', 'showSeries')
SERIE_AR = (URL_MAIN + '/cat/mosalsalat-3arabia-YJ/', 'showSeries')
SERIE_ASIA = (URL_MAIN + '/cat/mosalsalat-korea/', 'showSeries')
SERIE_LATIN = (URL_MAIN + '/cat/mosalsalat-latinia/', 'showSeries')
REPLAYTV_NEWS = (URL_MAIN + '/cat/programme-tv/', 'showSeries')

URL_SEARCH = (URL_MAIN + '/q/', 'showSeriesSearch')
FUNCTION_SEARCH = 'showSeriesSearch'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Search Series', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات عربية', 'mslsl.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ASIA[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات أسيوية', 'mslsl.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', 'mslsl.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات هندية', 'mslsl.png', oOutputParameterHandler)  

    oOutputParameterHandler.addParameter('siteUrl', SERIE_LATIN [0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات لاتنية', 'mslsl.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_DUBBED [0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات مدبلجة', 'mslsl.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', RAMADAN_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات رمضان', 'mslsl.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', 'https://a.tvfun.me/mosalsalat-maghribia/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات مغربية', 'mslsl.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', 'https://a.tvfun.me/ts,mosalsalat-tarkiya/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تاريخية', 'mslsl.png', oOutputParameterHandler)
        
    oOutputParameterHandler.addParameter('siteUrl', 'https://a.tvfun.me/ts,mosalsalat-mexicia/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات مكسيكية', 'mslsl.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', 'https://a.tvfun.me/dessin-animee/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'انمي', 'anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'https://a.tvfun.me/ts,baramij-tarfihiya/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'برامج ترفيهية', 'brmg.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', 'https://a.tvfun.me/ts,hidden-camera/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'الكاميرا الخفية', 'brmg.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'برامج تلفزيونية', 'brmg.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText is not False:
        sUrl = URL_MAIN + '/q/' +sSearchText
        showSeriesSearch(sUrl)
        oGui.setEndOfDirectory()
        return
  
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

    sPattern = '<div class="serie-thumb"><a href="(.+?)" title="(.+?)"><img src="(.+?)" sizes='
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1].replace("مشاهدة وتحميل","").replace("اون لاين","")
            siteUrl = aEntry[0]
            if siteUrl.startswith('//'):
                siteUrl = 'http:' + siteUrl
            if URL_MAIN not in siteUrl:
                siteUrl = URL_MAIN + siteUrl
            sThumb = aEntry[2]
            sDesc = ''
            sYear = ''


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    sPattern = '<ul class="pagination">(.+?)class="headline">'  
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern) 
     

    if aResult[0] is True:
        sHtmlContent4 = aResult[1][0]
  # ([^<]+) .+?

    sPattern = '<li><a href="([^<]+)">([^<]+)</a></li>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent4, sPattern)
	
	
    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1]
            
            sTitle =  "PAGE " + sTitle
            sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
            siteUrl = aEntry[0]
            if siteUrl.startswith('/'):
                siteUrl = URL_MAIN + siteUrl
            if siteUrl.startswith('//'):
                siteUrl = 'http:' + siteUrl
            sThumb = ""
            sDesc = ""


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, '', oOutputParameterHandler)

        progress_.VSclose(progress_)
 

 
    if not sSearch:
        oGui.setEndOfDirectory()
  
def showSeriesSearch(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch+"/"
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'class="headline">(.+?)class="head-title"> أخر الحلقات </h3>'  
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern) 
     

    if aResult[0] is True:
        sHtmlContent2 = aResult[1][0]
   # ([^<]+) .+? (.+?)
    sPattern = '<div class="video-thumb"><a href="(.+?)" title="(.+?)"><img src="(.+?)" sizes='
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent2, sPattern)
	
	
    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1].replace("الحلقة "," E").replace("حلقة "," E").replace("مشاهدة وتحميل","").replace("اون لاين","").replace("والاخيرة","")
            siteUrl = aEntry[0]
            if siteUrl.startswith('//'):
                siteUrl = 'http:' + siteUrl
            if URL_MAIN not in siteUrl:
                siteUrl = URL_MAIN + siteUrl
            sThumb = aEntry[2]
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)
        
        progress_.VSclose(progress_)
   #([^<]+) .+?
    sPattern = 'class="videocontainer"> <iframe src="([^<]+)" id="([^<]+)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = "playlist"
            siteUrl = 'https:'+aEntry[0]
            if siteUrl.startswith('/'):
                siteUrl = URL_MAIN + siteUrl
            if siteUrl.startswith('//'):
                siteUrl = 'http:' + siteUrl
            if URL_MAIN not in siteUrl:
                siteUrl = URL_MAIN + siteUrl
            sThumb = sThumb
            sDesc = ""
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
  #([^<]+) .+?

    sPattern = '<ul class="pagination">(.+?)class="headline">'  
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern) 
     

    if aResult[0] is True:
        sHtmlContent3 = aResult[1][0]
  # ([^<]+) .+?

        sPattern = '<li><a href="([^<]+)">([^<]+)</a></li>'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent3, sPattern)
	
	
        if aResult[0] is True:
            total = len(aResult[1])
            progress_ = progress().VScreate(SITE_NAME)
            for aEntry in aResult[1]:
                progress_.VSupdate(progress_, total)
                if progress_.iscanceled():
                    break
 
                sTitle = aEntry[1]
            
                sTitle =  "PAGE " + sTitle
                sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
                siteUrl = aEntry[0]
                sThumb = ""
                sDesc = ""


                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			
                oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
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

    sPattern = 'class="headline">(.+?)class="head-title"> أخر الحلقات </h3>'  
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern) 
     

    if aResult[0] is True:
        sHtmlContent = aResult[1][0]
   # ([^<]+) .+? (.+?)
    sPattern = '<div class="video-thumb"><a href="(.+?)" title="(.+?)"><img src="(.+?)" sizes='
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1].replace("الحلقة "," E").replace("حلقة "," E").replace("مدبلج للعربية","مدبلج").replace("مشاهدة وتحميل","").replace("اون لاين","")
            siteUrl = aEntry[0]
            if siteUrl.startswith('//'):
                siteUrl = 'http:' + siteUrl
            if URL_MAIN not in siteUrl:
                siteUrl = URL_MAIN + siteUrl
            sThumb = sThumb
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)
   #([^<]+) .+?
    sPattern = 'class="videocontainer"> <iframe src="([^<]+)" id="([^<]+)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = "playlist"
            siteUrl = 'https:'+aEntry[0]
            if siteUrl.startswith('//'):
                siteUrl = 'http:' + siteUrl
            if URL_MAIN not in siteUrl:
                siteUrl = URL_MAIN + siteUrl
            sThumb = sThumb
            sDesc = ""
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    sPattern = '<ul class="pagination">(.+?)class="headline">'  
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern) 
     

    if aResult[0] is True:
        sHtmlContent3 = aResult[1][0]
  # ([^<]+) .+?

        sPattern = '<li><a href="([^<]+)">([^<]+)</a></li>'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent3, sPattern)
	
	
        if aResult[0] is True:
            total = len(aResult[1])
            progress_ = progress().VScreate(SITE_NAME)
            for aEntry in aResult[1]:
                progress_.VSupdate(progress_, total)
                if progress_.iscanceled():
                    break
 
                sTitle = aEntry[1]
            
                sTitle =  "PAGE " + sTitle
                sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
                siteUrl = aEntry[0]
                sThumb = ""
                sDesc = ""


                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			
                oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 

       
    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    oParser = cParser()

    sPattern =  "PGlmcmFt(.+?)'"
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0] is True:
        for aEntry in aResult[1]:
            m3url = "PGlmcmFt" + aEntry
            sHtmlContent2 = base64.b64decode(m3url)
    # (.+?)    .+?    
            sPattern = 'src="(.+?)".+?allowfullscreen'
            aResult = oParser.parse(sHtmlContent2, sPattern)

            if aResult[0] is True:
               for aEntry in aResult[1]:
        
                   url = aEntry.replace("https://dai.ly/","https://www.dailymotion.com/video/")
                   sTitle = " " 
                   if url.startswith('//'):
                       url = 'http:' + url
            
                   sHosterUrl = url 
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster != False:
                       sDisplayTitle = sMovieTitle+sTitle
                       oHoster.setDisplayName(sDisplayTitle)
                       oHoster.setFileName(sDisplayTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
				

                
    oGui.setEndOfDirectory()