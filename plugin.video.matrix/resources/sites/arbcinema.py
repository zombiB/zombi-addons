#-*- coding: utf-8 -*-
#zombi https://github.com/zombiB/zombi-addons/
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog, isMatrix
import re
 
SITE_IDENTIFIER = 'arbcinema'
SITE_NAME = 'arbcinema'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'https://in.arbcinema.com'


MOVIE_EN = (URL_MAIN + '/cat_film/%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%a7%d8%ac%d9%86%d8%a8%d9%8a-%d9%85%d8%aa%d8%b1%d8%ac%d9%85%d8%a9/', 'showMovies')
KID_MOVIES = (URL_MAIN + '/type/%d9%83%d8%b1%d8%aa%d9%88%d9%86/', 'showMovies')
MOVIE_ASIAN = (URL_MAIN + '/country/%d9%85%d8%b4%d8%a7%d9%87%d8%af%d8%a9-%d8%a7%d9%81%d9%84%d8%a7%d9%85-%d8%a7%d8%b3%d9%8a%d9%88%d9%8a%d8%a9-%d9%85%d8%aa%d8%b1%d8%ac%d9%85%d8%a9/', 'showMovies')


URL_SEARCH = (URL_MAIN + '/?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '/?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0' 
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
        sUrl = URL_MAIN + '/?s='+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ["مشاهدة اقوى 100 فيلم 2018","https://on.arbcinema.com/type/%D9%85%D8%B4%D8%A7%D9%87%D8%AF%D8%A9-%D8%A7%D9%82%D9%88%D9%89-100-%D9%81%D9%8A%D9%84%D9%85-2018/"] )

    
	            
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSerie', sTitle, 'genres.png', oOutputParameterHandler)
       
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
    if isMatrix(): 
       sHtmlContent = str(sHtmlContent.encode('latin-1',errors='ignore'),'utf-8',errors='ignore')
  # ([^<]+) .+?

    sPattern = '<li class="col-md-3"><a href="([^<]+)">.+?<img src="([^<]+)" itemprop="image">  <div class="mov-details-overlay">.+?<h4 class="move-title">([^<]+)</h4>.+?<div class="card-text">.+?<p>([^<]+)</p>.+?</div>.+?<div class="mov-typ">([^<]+)</div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[2].replace("مشاهدة","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("كامل","").replace("برنامج","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","")
            siteUrl = str(aEntry[0])
            sThumb = str(aEntry[1])
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
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addMovie(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()

 
def showSerie(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request() 
  # ([^<]+) .+?

    sPattern = '<li class="col-md-3"><a href="([^<]+)">.+?<div class="number_episode">([^<]+)</div>.+?<img src="([^<]+)" itemprop="image">  <div class="mov-details-overlay">.+?<h4 class="move-title">([^<]+)</h4>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()  
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[3]
            sTitle = sTitle.replace("مشاهدة","").replace("برنامج","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","")
            siteUrl = str(aEntry[0])+'?watch=1'
            sThumb = str(aEntry[2])
            sDesc = aEntry[1]


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSerie', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
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
   # ([^<]+) .+?
    sPattern = '<a href="([^<]+)">([^<]+)</a></td>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
 
            sTitle = aEntry[1]
            siteUrl = str(aEntry[0])
            sThumb = str(sThumb)
            sDesc = ''
			


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
    
def showLink():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()
    
    #Recuperation infos
    sNote = ''

    sPattern = 'قصة الفيلم:([^<]+)<br>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        sNote = aResult[1][0]
    # (.+?) .+? ([^<]+)
    sPattern = '<input type="hidden" name="([^<]+)" value="1">'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
   
    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
 
            sTitle = aEntry
            siteUrl = sUrl
            sThumb = sThumb
            sDesc = sNote
 
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            if 'download' in sTitle:
                oGui.addLink(SITE_IDENTIFIER, 'showServer', sTitle, sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addLink(SITE_IDENTIFIER, 'showServer2', sTitle, sThumb, sDesc, oOutputParameterHandler)
 
    oGui.setEndOfDirectory() 
	 
def showServer():
    oGui = cGui()
    import requests
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')


    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

   
    oParser = cParser()
    
    #Recuperation infos
    sId = ''

    sPattern = 'postid-(.+?)">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        sId = aResult[1][0]

    
  # ([^<]+) .+?
    headers = {'Host': 'ok.arbcinema.com',
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
     'Accept': '*/*',
     'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
     'X-Requested-With': 'XMLHttpRequest',
     'Connection': 'keep-alive'}
    data = sId
    data = {'id':data,'key':'0','type':'normal'}
    s = requests.Session()
    r = s.post('https://ok.arbcinema.com/wp-content/themes/takweed/functions/inc/single/server.php', headers=headers, data = data)
    sHtmlContent = r.content.decode('utf8') 
    
    # (.+?) .+? ([^<]+)        	
    sPattern = '<a href="([^<]+)" rel'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

	
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            url = str(aEntry)
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
            if (oHoster != False):
               oHoster.setDisplayName(sMovieTitle)
               oHoster.setFileName(sMovieTitle)
               cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
				
       
    oGui.setEndOfDirectory()	 
def showServer2():
    oGui = cGui()
    import requests
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')


    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

   
    oParser = cParser()
    
    #Recuperation infos
    sId = ''
     # (.+?) ([^<]+) .+?
    sPattern = 'postid-(.+?)">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        sId = aResult[1][0]

    #print sId
    
        headers = {'Host': 'ok.arbcinema.com',
					'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
					'Accept': '*/*',
					'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
					'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
					'X-Requested-With': 'XMLHttpRequest',
					'Referer': sUrl,
					'Connection': 'keep-alive'}
        data = {'watch':'1'}
        s = requests.Session()
        r = s.post(sUrl,data = data)
        sHtmlContent = r.content.decode('utf8')  

        sPattern2 = '<li data-name="([^<]+)" data-type="free"'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern2)
        if (aResult[0] == True):
           for aEntry in aResult[1]:
               nume = aEntry
               headers = {'Host': 'ok.arbcinema.com',
							'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36',
							'Accept': '*/*',
							'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
							'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
							'X-Requested-With': 'XMLHttpRequest',
							'Connection': 'keep-alive'}
               data = {'id':sId,'name':nume,'type':'free'}
               s = requests.Session()
               r = s.post( 'https://ok.arbcinema.com/wp-content/themes/takweed/functions/inc/single/server.php', headers=headers, data = data)
               sHtmlContent = r.content.decode('utf8')         

               sPattern3 = '<IFRAME.+?SRC="(.+?)".+?FRAMEBORDER='

               oParser = cParser()
               aResult = oParser.parse(sHtmlContent, sPattern3)
               if (aResult[0] == True):
                  for aEntry in aResult[1]:
            
                      url = str(aEntry)
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
                      if (oHoster != False):
                         sDisplayTitle = sTitle
                         oHoster.setDisplayName(sDisplayTitle)
                         oHoster.setFileName(sMovieTitle)
                         cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb) 

       
    oGui.setEndOfDirectory()
 
 
def __checkForNextPage(sHtmlContent):
    sPattern = "<a href='([^<]+)'>&rsaquo;</a>"
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if (aResult[0] == True):
        #print aResult[1][0]
        return aResult[1][0]

    return False