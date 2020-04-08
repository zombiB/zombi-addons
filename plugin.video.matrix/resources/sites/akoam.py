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
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.player import cPlayer
import xbmcgui
import urllib2,urllib,re
import unicodedata
 
SITE_IDENTIFIER = 'akoam'
SITE_NAME = 'akoam'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'https://we.akoam.net'


MOVIE_PACK = ('https://w5.akoam.net/cat/186/%D8%B3%D9%84%D8%A7%D8%B3%D9%84-%D8%A7%D9%84%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%A7%D9%84%D8%A7%D8%AC%D9%86%D8%A8%D9%8A%D8%A9', 'showSeries')

MOVIE_EN = ('https://we.akoam.net/cat/156/%D8%A7%D9%84%D8%A3%D9%81%D9%84%D8%A7%D9%85-%D8%A7%D9%84%D8%A7%D8%AC%D9%86%D8%A8%D9%8A%D8%A9', 'showMovies')

KID_MOVIES = ('https://web.akoam.net/cat/179/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%A7%D9%84%D8%A7%D9%86%D9%85%D9%8A-%D8%A7%D9%84%D9%85%D8%AF%D8%A8%D9%84%D8%AC%D8%A9', 'showMovies')
MOVIE_AR = ('https://w2.akoam.net/cat/155/%D8%A7%D9%84%D8%A3%D9%81%D9%84%D8%A7%D9%85-%D8%A7%D9%84%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9', 'showMovies')

MOVIE_HI = ('https://w2.akoam.net/cat/168/%D8%A7%D9%84%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%A7%D9%84%D9%87%D9%86%D8%AF%D9%8A%D8%A9', 'showMovies')

REPLAYTV_NEWS = ('https://w2.akoam.net/cat/81/%D8%A7%D9%84%D8%A8%D8%B1%D8%A7%D9%85%D8%AC-%D8%A7%D9%84%D8%AA%D9%84%D9%81%D8%B2%D9%8A%D9%88%D9%86%D9%8A%D8%A9', 'showSeries')
SERIE_AR = ('https://w2.akoam.net/cat/80/%D8%A7%D9%84%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%A7%D9%84%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9', 'showSeries')
SERIE_EN = ('https://w2.akoam.net/cat/166/%D8%A7%D9%84%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%A7%D9%84%D8%A7%D8%AC%D9%86%D8%A8%D9%8A%D8%A9', 'showSeries')

ANIM_NEWS = ('https://w2.akoam.net/cat/83/%D8%A7%D9%84%D8%A7%D9%86%D9%85%D9%8A', 'showMovies')
SERIE_ASIA = ('https://w2.akoam.net/cat/185/%D8%A7%D9%84%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%A7%D9%84%D8%A7%D8%B3%D9%8A%D9%88%D9%8A%D8%A9', 'showSeries')
SERIE_TR = ('https://w2.akoam.net/cat/190/%D8%A7%D9%84%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%A7%D9%84%D9%85%D8%AF%D8%A8%D9%84%D8%AC%D8%A9', 'showSeries')
SERIE_GENRES = (True, 'showGenres')

DOC_NEWS = ('https://w2.akoam.net/cat/94/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D9%88%D8%AB%D8%A7%D8%A6%D9%82%D9%8A%D8%A9', 'showMovies')
URL_SEARCH = ('https://w2.akoam.net/search/', 'showMoviesSearch')
URL_SEARCH_MOVIES = ('https://w2.akoam.net/search/', 'showMoviesSearch')
URL_SEARCH_SERIES = ('https://w2.akoam.net/search/', 'showMoviesSearch')
FUNCTION_SEARCH = 'showSearch'
 
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
        sUrl = 'https://w2.akoam.net/search/'+sSearchText
        showMovies(sUrl)
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
      # (.+?) ([^<]+) .+?

    sPattern = '<div class="tags_box"><a href="([^<]+)"><div class="tag_box_image" style=([^<]+)></div><h1>([^<]+)</h1>'

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
            sTitle = sTitle.replace("مشاهدة","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","")
 
 
            siteUrl = aEntry[0]
            sInfo = ""
            sThumbnail = str(aEntry[1]).replace("'background-image: url(","").replace(");'","")



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

def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ["مسلسلات مدبلجة","https://w5.akoam.net/cat/190/%D8%A7%D9%84%D9%85%D8%B3%D9%84%D8%B3%D9%84%D8%A7%D8%AA-%D8%A7%D9%84%D9%85%D8%AF%D8%A8%D9%84%D8%AC%D8%A9"] )

    
	            
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'genres.png', oOutputParameterHandler)
       
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
      # (.+?) ([^<]+) .+?

    sPattern = '<div class="subject_box shape"><a href="([^<]+)"><img src="([^<]+)" alt="اسم الموضوع"><div class="subject_title "><h3>([^<]+)</h3><span class="desc">([^<]+)</span></div>'

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
            sTitle = sTitle.replace("مشاهدة","").replace("مترجمة","").replace("مترجم","").replace("الفيلم الوثائقي","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","")
            annee = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
				annee = str(m.group(0))
				sTitle = sTitle.replace(annee,'')
            if annee:
				sTitle = sTitle  
 
 
            siteUrl = aEntry[0]
            sInfo = ""
            sThumbnail = str(aEntry[1])



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


def showLink():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()



    #print sUrl
   
    oParser = cParser()
    
    #Recuperation infos
    sNote = ''

    sPattern = '<div class="sub_desc"><span style="color:#FFD700">.+?</span>([^<]+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        sNote = aResult[1][0]
     # (.+?) ([^<]+)
    sPattern = "class='sub_file_title'>([^<]+)<i>([^<]+)</i> "
    sPattern = sPattern +  '|' + "target='_blank' href='([^<]+)'>([^<]+)</a></div>"


    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
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
                oGui.addText(SITE_IDENTIFIER,'[COLOR yellow]'+sQua+'-[/COLOR]'+ '[COLOR coral]'+sSize+'[/COLOR]')
                   
        
            if aEntry[2]:
                sTitle = aEntry[3]
                siteUrl = aEntry[2]
                sInfo = sNote.decode("utf8")
                sInfo = cUtil().unescape(sInfo).encode("utf8")
                sInfo = '[COLOR yellow]'+sInfo+'[/COLOR]'
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
		if 'akoam'  in siteUrl:
			oGui.addMisc(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
		if '/video/'  in siteUrl:
			oGui.addMisc(SITE_IDENTIFIER, 'showHosters2', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        progress_.VSclose(progress_)
    # (.+?) .+?
    sPattern = '<a href="https://akwam.net/movie/(.+?)" target="_blank"><span style="color'
    
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
 
            sTitle = " يرجي الانتقال إلي التصميم الجديد من هنا"
            siteUrl = "https://akwam.net/movie/"+str(aEntry)
            sThumbnail = str(sThumbnail)
            sInfo = ""
 
            #print sUrl
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            

 
            oGui.addMisc(SITE_IDENTIFIER, 'showSeasons2', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
 
        progress_.VSclose(progress_)
       
    oGui.setEndOfDirectory()
def showLinks():
    oGui = cGui()
    import requests,re,urllib2,json
    sgn=requests.Session()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

   
    oParser = cParser()
    headers = {'Host': 'w2.akoam.net',
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
     'Accept': 'application/json, text/javascript, */*; q=0.01',
     'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
     'Accept-Encoding': 'gzip, deflate',
     'X-Requested-With': 'XMLHttpRequest',
     'Referer': sUrl}

    r = sgn.get(sUrl)
    href = (r.headers)['Set-Cookie']
    href = urllib2.unquote(href).replace('golink=','').split('; expires')[0]
    route = json.loads(href)
    route =  route["route"]
    route =  route.encode("utf-8")




	
	
    if route: 
		m3url = route
		m3url = m3url.replace("/download/","/watching/")
		oRequest = cRequestHandler(m3url)
		sHtmlContent = oRequest.request()
		if '/watching/'  in m3url:
    # ([^<]+) .+?
               
			
			sPattern = 'file: "(.+?)",'
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
						if url.startswith('//'):
							url = 'http:' + url
            
						sHosterUrl = url 
						oHoster = cHosterGui().checkHoster(sHosterUrl)
						if (oHoster != False):
							sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
							oHoster.setDisplayName(sDisplayTitle)
							oHoster.setFileName(sMovieTitle)
							cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				

					progress_.VSclose(progress_)
		if '/video/'  in m3url:
    # ([^<]+) .+?
               

			sPattern = 'SRC="([^<]+)" FRAMEBORDER.+?</IFRAME>'
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
						if url.startswith('//'):
							url = 'http:' + url
            
						sHosterUrl = url 
						oHoster = cHosterGui().checkHoster(sHosterUrl)
						if (oHoster != False):
							sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
							oHoster.setDisplayName(sDisplayTitle)
							oHoster.setFileName(sMovieTitle)
							cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				

					progress_.VSclose(progress_) 
        

       
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
    sPattern = '<div class="subject_box shape"><a href="([^<]+)"><img src="([^<]+)" alt="اسم الموضوع"><div class="subject_title "><h3>([^<]+)</h3><span class="desc">([^<]+)</span></div>'

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
            sTitle = sTitle.replace("مشاهدة","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","")
 
 
            siteUrl = aEntry[0]
            sInfo = ""
            sThumbnail = str(aEntry[1])
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            oGui.addMovie(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
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
    sPattern = "</li><li class='pagination_next'><a href='([^<]+)' class='ako-arrow ako-left-arrow'></a>"
	
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
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()
    
    #Recuperation infos
    sNote = ''

    sPattern = '<div class="sub_desc"><span style="color:#FFD700">.+?</span>([^<]+)<br />'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        sNote = aResult[1][0]
    # .+? ([^<]+)
    sPattern = '<a href="([^<]+)" target="_blank"><span style="color:#.+?">([^<]+)</span></a><br />'
    
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
 
            sTitle = aEntry[1].decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            sTitle = '[COLOR cyan]'+sTitle+'[/COLOR]'
            siteUrl = str(aEntry[0])
            sThumbnail = sThumbnail
            sInfo = ""
 
            #print sUrl
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            

 
            oGui.addTV(SITE_IDENTIFIER, 'showSeasons', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
 
        progress_.VSclose(progress_)
     # (.+?) ([^<]+)
    sPattern = "class='sub_file_title'>([^<]+)<i>([^<]+)</i> "
    sPattern = sPattern +  '|' + "target='_blank' href='([^<]+)'>([^<]+)</a></div>"


    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
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
                oGui.addText(SITE_IDENTIFIER,'[COLOR yellow]'+sQua+'-[/COLOR]'+ '[COLOR coral]'+sSize+'[/COLOR]')
                   
        
            if aEntry[2]:
                sTitle = aEntry[3]
                siteUrl = aEntry[2]
                sInfo = sNote.decode("utf8")
                sInfo = cUtil().unescape(sInfo).encode("utf8")
                sInfo = '[COLOR yellow]'+sInfo+'[/COLOR]'
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
                oGui.addTV(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
       
    oGui.setEndOfDirectory()

  
def showSeasons2():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()
    # .+? ([^<]+)
    sPattern = '<a href="http([^<]+).com/watch/(.+?)"'
    
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
 
            sTitle = aEntry[1].decode("utf8")
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            sTitle = '[COLOR cyan]'+sTitle+'[/COLOR]'
            siteUrl = 'http'+aEntry[0]+'.com/watch/' + str(aEntry[1])
            sThumbnail = sThumbnail
            sInfo = siteUrl
 
            #print sUrl
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            

 
            oGui.addMisc(SITE_IDENTIFIER, 'showSeasons3', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
 
        progress_.VSclose(progress_)
       
    oGui.setEndOfDirectory()

  
def showSeasons3():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()
    # .+? ([^<]+)
    sPattern = '<a href="([^<]+)".+?class="download-link"'
    
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
 
            sTitle = "link"
            sTitle = cUtil().unescape(sTitle).encode("utf8")
            sTitle = '[COLOR yellow]'+sTitle+'[/COLOR]'
            siteUrl = str(aEntry)
            sThumbnail = sThumbnail
            sInfo = siteUrl
 
            #print sUrl
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            

 
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
 
        progress_.VSclose(progress_)
       
    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    # .+? ([^<]+) (.+?)
               

    sPattern = 'src="(.+?)".+?type='
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
				if url.startswith('//'):
					url = 'http:' + url
            
				sHosterUrl = url 
				oHoster = cHosterGui().checkHoster(sHosterUrl)
				if (oHoster != False):
					sDisplayTitle = cUtil().DecoTitle(sTitle)
					oHoster.setDisplayName(sDisplayTitle)
					oHoster.setFileName(sMovieTitle)
					cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
				

			progress_.VSclose(progress_) 
                
    oGui.setEndOfDirectory()