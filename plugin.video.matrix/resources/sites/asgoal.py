#-*- coding: utf-8 -*-
#zombi https://github.com/zombiB/zombi-addons/
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress ,VSlog, siteManager
from resources.lib.parser import cParser
import re
 
SITE_IDENTIFIER = 'asgoal'
SITE_NAME = 'asgoal'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

SPORT_LIVE = ('https://www.as-goal.com/mm/', 'showMovies')

FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Search', 'search.png', oOutputParameterHandler)
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_LIVE[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'بث مباشر', 'sport.png', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText != False:
        sUrl = ''+sSearchText
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
    oParser = cParser()
    sStart = '<div id="Today" class='
    sEnd = '</footer>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
 
# ([^<]+) .+? (.+?)

    sPattern = '<a href="(.+?)".+?rel="(.+?)">.+?<img alt="(.+?)" title.+?<img alt="(.+?)" title='



    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle =  aEntry[2]+' - ' +aEntry[3] 
            sThumbnail = ""
            siteUrl = aEntry[0]
            if siteUrl.startswith('//'):
                siteUrl = 'http:' + aEntry[0]
            sInfo = aEntry[1]+' GMT+2'
			
			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            oGui.addMisc(SITE_IDENTIFIER, 'showLive', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
    if not sSearch:
        oGui.setEndOfDirectory()
  
def showLive():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    # (.+?) # ([^<]+) .+? 
    sPattern = 'setURL([^<]+)">([^<]+)</button>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    #print aResult
   
    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
 
            sTitle = aEntry[1]
            siteUrl = aEntry[0].replace("('","").replace("')","")
            sInfo = ""
            import requests    
            oRequestHandler = cRequestHandler(siteUrl)
            hdr = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0','Accept-Encoding' : 'gzip','referer' : 'https://live.as-goal.tv/'}
            St=requests.Session()
            sHtmlContent = St.get(siteUrl,headers=hdr)
            sHtmlContent = sHtmlContent.content
            oParser = cParser()
    # (.+?) # ([^<]+) .+? 
            sPattern = "source: '(.+?)',"
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] is True:
               for aEntry in aResult[1]:
                   url = aEntry
                   sHosterUrl = url.replace("https://tv.as-goal.site/zurl.html?src=","")
                   sMovieTitle = sMovieTitle
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster != False:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
            sPattern = 'source:"(.+?)",'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] is True:
               for aEntry in aResult[1]:
                   url = aEntry
                   sHosterUrl = url.replace("https://tv.as-goal.site/zurl.html?src=","")
                   sMovieTitle = sMovieTitle
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster != False:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

    # (.+?) # ([^<]+) .+? 
            sPattern = 'src="(.+?)"'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] is True:
               for aEntry in aResult[1]:
                   url = aEntry
                   sHosterUrl = url.replace("https://tv.as-goal.site/zurl.html?src=","")
                   sMovieTitle = sMovieTitle
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster != False:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
    # (.+?) # ([^<]+) .+? 
            sPattern = 'file:"(.+?)",'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] is True:
               for aEntry in aResult[1]:
                   url = aEntry
                   sHosterUrl = url.replace("https://tv.as-goal.site/zurl.html?src=","")
                   sMovieTitle = sMovieTitle
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster != False:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

 # (.+?) # ([^<]+) .+? 

            sPattern = 'onclick="([^<]+)" >.+?>([^<]+)</strong>'
            aResult = oParser.parse(sHtmlContent, sPattern)

            if aResult[0] is True:
               for aEntry in aResult[1]:
                   url = aEntry[0].replace("('",'').replace("')","").replace("update_frame","")
                   url = url.split('?link=', 1)[1]
                   if url.startswith('//'):
                      url = 'http:' + url
                   if '/embed/' in url:
                      oRequestHandler = cRequestHandler(url)
                      oParser = cParser()
                      sPattern =  'src="(.+?)" scrolling="no">'
                      aResult = oParser.parse(url,sPattern)
                      if aResult[0] is True:
                          url = aResult[1][0]
                          sHosterUrl = url.replace("https://tv.as-goal.site/zurl.html?src=","")
                          sMovieTitle = str(aEntry[1])
                          oHoster = cHosterGui().checkHoster(sHosterUrl)
                          if oHoster != False:
                              oHoster.setDisplayName(sMovieTitle)
                              oHoster.setFileName(sMovieTitle)
                              cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

 # (.+?) # ([^<]+) .+? 

            sPattern = 'src="(.+?)" width="(.+?)"'
            aResult = oParser.parse(sHtmlContent, sPattern)

            if aResult[0] is True:
               for aEntry in aResult[1]:
                   url = aEntry[0]
                   if url.startswith('//'):
                      url = 'http:' + url
                   if 'xyz' in url:
                       oRequestHandler = cRequestHandler(url)
                       oRequestHandler.setRequestType(1)
                       oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0')
                       oRequestHandler.addHeaderEntry('referer', 'https://ch.as-goal.tv/')
                       sHtmlContent2 = oRequestHandler.request();
                       oParser = cParser()
                       sPattern =  '(http[^<]+m3u8)'
                       aResult = oParser.parse(sHtmlContent2,sPattern)
                       if aResult[0] is True:
                           url = aResult[1][0]+ '|User-Agent=' + 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0' +'&Referer=' + "https://memotec.xyz/"
 
                           sHosterUrl = url.replace("https://tv.as-goal.site/zurl.html?src=","") 
                           sMovieTitle = sMovieTitle
            

                           oHoster = cHosterGui().checkHoster(sHosterUrl)
                           if oHoster != False:
                               oHoster.setDisplayName(sMovieTitle)
                               oHoster.setFileName(sMovieTitle)
                               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

                
    oGui.setEndOfDirectory()