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
 
SITE_IDENTIFIER = 'okanime'
SITE_NAME = 'okanime'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'https://www.okanime.com'




ANIM_MOVIES = ('https://www.okanime.com/movies', 'showMovies')
ANIM_NEWS = ('https://www.okanime.com/partials/filter_animes?utf8=%E2%9C%93&aired_year_to=&aired_year_from=&rating_to=&rating_from=&episode_number_to=&episode_number_from=&direction=&sort=published_at&status=&search=&anime_type=&pg=&season=&studio_list=&director=&original_work=&start_from=&genre_list', 'showSeries')



URL_SEARCH = ('/?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    

            
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = '?s='+sSearchText
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
 
# ([^<]+) .+?
    sPattern = '<img class="img-responsive cover-5-span" alt="([^<]+)" src="([^<]+)" /><div class="rating-'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[0].decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
 
            sThumbnail = URL_MAIN+aEntry[0]
 
            siteUrl = URL_MAIN+aEntry[1]
 
            siteUrl = siteUrl.replace('/review','')
            sInfo = aEntry[0]



            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            oGui.addMovie(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
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
# ([^<]+) .+?
    sPattern = '<a href="([^<]+)">.+?data-src="([^<]+)".+?<span class="video-title">([^<]+)</span>.+?<span class="video-subtitle">([^<]+)</span>'

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
 
            sThumbnail = aEntry[1]
            if sThumbnail.startswith('/'):
                sThumbnail = URL_MAIN + sThumbnail
                sThumbnail = sThumbnail.replace('.webp','')
 
            siteUrl = URL_MAIN + aEntry[0]
 
            siteUrl = siteUrl
            sInfo = aEntry[3]



            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            oGui.addMovie(SITE_IDENTIFIER, 'showEps', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()

 
def __checkForNextPageMovie(sHtmlContent):
    sPattern = '<a href="([^<]+)" class="pagination-next">التالي</a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        aResult = 'https'+aResult[1][0]
        return aResult

    return False
def __checkForNextPage(sHtmlContent):
    sPattern = '<a rel="next" href="(.+?)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        aResult = URL_MAIN + aResult[1][0]
        return aResult

    return False
	
def showEps():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
            
    sPattern =  '<a class="btn btn-lg2 btn-watch" href="([^<]+)">' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if (aResult[0] == True):
        m3url = URL_MAIN + aResult[1][0] 
        oRequest = cRequestHandler(m3url)
        sHtmlContent = oRequest.request()
         # ([^<]+) .+?  (.+?) 
    sPattern = '<a class="episode" href="([^<]+)"><li>.+?episode_number.+?>([^<]+)</span>'
  
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent.replace('\n',''))
    #fh.close()

    #print aResult
   
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1]
 
            siteUrl = URL_MAIN + aEntry[0]
            sInfo = ""

 
            #print sUrl
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            

 
            oGui.addMovie(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
 
        progress_.VSclose(progress_)
       
    oGui.setEndOfDirectory()
        
	
def showLink():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
	
# ([^<]+) .+?

    sPattern = '>([^<]+)</div><h3>([^<]+)</h3>'
    sPattern = sPattern + '|' + '<a href="([^<]+)"><li.+?>(.+?)</li>'
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


 

            sQua = aEntry[1]
            sSize = aEntry[0]
            
            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER,'[COLOR yellow]'+sQua+'[/COLOR]'+'[COLOR coral] '+sSize+' [/COLOR]')
                   
        
            if aEntry[2]:
                sTitle = ""
                siteUrl = aEntry[2]
                sInfo = sMovieTitle
                sHosterUrl = siteUrl
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
					oHoster.setDisplayName(sTitle)
					oHoster.setFileName(sMovieTitle)
					cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

        progress_.VSclose(progress_) 
    # (.+?)
    sPattern = ' class="load_player.+?href="([^<]+)">(.+?)</a></li>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent.replace('\n',''))
    #fh.close()

    #print aResult
   
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[1]
 
            siteUrl = URL_MAIN + aEntry[0]
            sInfo = " "
 
            #print sUrl
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            

 
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
 
        progress_.VSclose(progress_)
       


    oGui.setEndOfDirectory()
	 
def showHosters():
    oGui = cGui()
    import requests
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    sInfo = oInputParameterHandler.getValue('sInfo')

    #print sHtmlContent 

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

   
    oParser = cParser()
    
    #Recuperation infos
    sId = ''
     # (.+?) ([^<]+) .+?
    sPattern = '{"url":"(.+?)","server_notice"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
			total = len(aResult[1])
			progress_ = progress().VScreate(SITE_NAME)
			for aEntry in aResult[1]:
				progress_.VSupdate(progress_, total)
				if progress_.iscanceled():
					break
            
				headers = {'Host': 'www.okanime.com',
							'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
							'encoding': 'utf-8',
							'Sec-Fetch-Site': 'same-origin',
							'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
							'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
							'X-Requested-With': 'XMLHttpRequest',
							'Referer': 'https://www.okanime.com/',
							'Connection': 'keep-alive'}

				nume = aEntry.split('//www.okanime.com/cdn/anti-dmca/embed/?id=')[1]
				data = {'id':nume}
				print "numedata"
				print data
				s = requests.Session()
				
				r = s.post('https://www.okanime.com/cdn/anti-dmca/embed/?id='+nume, headers=headers,data = data)
				sHtmlContent += r.content 
				print sHtmlContent        

    sPattern = "src = '(.+?)'"
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
				if 'fajer.video' in url:
					url = url.split('id=')[1]
					url = "https://fajer.video/hls/"+url+"/"+url+".playlist.m3u8"
				if 'thevideo.me' in url:
					sTitle = " (thevideo.me)"
				if 'flashx' in url:
					sTitle = " (flashx)"
				if 'ok.ru' in url:
					sTitle = " (ok.ru)"
				if 'streamcherry' in url:
					sTitle = " (streamcherry)"
				if 'cloudvideo' in url:
					sTitle = " (cloudvideo)"
				if 'vcstream' in url:
					sTitle = " (vcstream)"
				if 'userscloud' in url:
					sTitle = " (userscloud)"
				if 'clicknupload' in url:
					sTitle = " (clicknupload)"
				if url.startswith('//'):
					url = 'http:' + url
            
				sHosterUrl = url 
				oHoster = cHosterGui().checkHoster(sHosterUrl)
				if (oHoster != False):
					sDisplayTitle = sTitle
					oHoster.setDisplayName(sDisplayTitle)
					oHoster.setFileName(sMovieTitle)
					cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				

			progress_.VSclose(progress_) 
       
    oGui.setEndOfDirectory()
	
def showHosterss():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    oParser = cParser()
            
    sPattern =  '{"url":"(.+?)","server_notice"' 
    aResult = oParser.parse(sHtmlContent,sPattern)
    if (aResult[0] == True):
        m3url = "https:"+aResult[1][0] 
         # ([^<]+) .+?  (.+?)  

  

    oRequestHandler = cRequestHandler(m3url)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36')
    oRequestHandler.addHeaderEntry('Referer', 'https://www.okanime.com/')
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate, br')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7,ar;q=0.6,lb;q=0.5,da;q=0.4')
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3')
    oRequestHandler.addHeaderEntry('Connection', 'keep-alive')
    sHtmlContent = oRequestHandler.request()
 
    sPattern = "src = '(.+?)'"
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
            sTitle = ""
            if url.startswith('https://drive.google.com'):
                url = url.replace('uc?id=','file/d/') 
            if url.startswith('https://drive.google.com'):
                url = url.replace('&export=download','/preview')
            
                 
            
            sHosterUrl = url
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				

        progress_.VSclose(progress_) 
                
    oGui.setEndOfDirectory()