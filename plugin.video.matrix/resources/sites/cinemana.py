# -*- coding: utf-8 -*-
#############################################################
# Yonn1981 https://github.com/Yonn1981/Repo
#############################################################

import re
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib.parser import cParser


ADDON = addon()
icons = ADDON.getSetting('defaultIcons')

SITE_IDENTIFIER = 'cinemana'
SITE_NAME = 'Cinemana'
SITE_DESC = 'arabic vod'

UA = 'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.48 Mobile Safari/537.36'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (URL_MAIN + '/movies/', 'showMovies')
MOVIE_AR = (URL_MAIN + '/page/arabic-movies/', 'showMovies')
SERIE_GENRES = (True, 'seriesGenres')
MOVIE_GENRES = (True, 'moviesGenres')

URL_SEARCH = (URL_MAIN + '/?s=', 'showSeries')
URL_SEARCH_MOVIES = (URL_MAIN + '/search/?search=%D9%81%D9%8A%D9%84%D9%85+', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '/search/?search=مسلسل+', 'showSeries')
FUNCTION_SEARCH = 'showSearch'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'SEARCH_MOVIES', icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', 'SEARCH_SERIES', icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية',icons + '/MoviesEnglish.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عربية',icons + '/Arabic.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'المسلسلات (الأنواع)', icons + '/TVShows.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'الأفلام (الأنواع)', icons + '/Movies.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/search/?search=مسلسل+'+sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/?s='+sSearchText+'&type=1'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def seriesGenres():
    oGui = cGui()

    liste = []
    liste.append(['اكشن', URL_MAIN + 'search/?search=مسلسل&genre=47'])
    liste.append(['انيميشن', URL_MAIN + 'search/?search=مسلسل&genre=309'])
    liste.append(['مغامرات', URL_MAIN + 'search/?search=مسلسل&genre=153'])
    liste.append(['تاريخي', URL_MAIN + 'search/?search=مسلسل&genre=25'])
    liste.append(['كوميديا', URL_MAIN + 'search/?search=مسلسل&genre=8'])
    liste.append(['موسيقى', URL_MAIN + 'search/?search=مسلسل&genre=131'])
    liste.append(['رياضي', URL_MAIN + 'search/?search=مسلسل&genre=17986'])
    liste.append(['دراما', URL_MAIN + 'search/?search=مسلسل&genre=27'])
    liste.append(['رعب', URL_MAIN + 'search/?search=مسلسل&genre=225'])
    liste.append(['عائلى', URL_MAIN + 'search/?search=مسلسل&genre=237'])
    liste.append(['فانتازيا', URL_MAIN + 'search/?search=مسلسل&genre=73'])
    liste.append(['حروب', URL_MAIN + 'search/?search=مسلسل&genre=79'])
    liste.append(['الجريمة', URL_MAIN + 'search/?search=مسلسل&genre=26'])
    liste.append(['رومانسى', URL_MAIN + 'search/?search=مسلسل&genre=37'])
    liste.append(['خيال علمى', URL_MAIN + 'search/?search=مسلسل&genre=91'])
    liste.append(['اثارة', URL_MAIN + 'search/?search=مسلسل&genre=36'])
    liste.append(['ﺗﺸﻮﻳﻖ ﻭﺇﺛﺎﺭﺓ', URL_MAIN + 'search/?search=مسلسل&genre=342'])
    liste.append(['وثائقى', URL_MAIN + 'search/?search=مسلسل&genre=195'])

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, icons + '/Genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def moviesGenres():
    oGui = cGui()

    liste = []
    liste.append(['اكشن', URL_MAIN + 'search/?search=فيلم&genre=47'])
    liste.append(['انيميشن', URL_MAIN + 'search/?search=فيلم&genre=309'])
    liste.append(['مغامرات', URL_MAIN + 'search/?search=فيلم&genre=153'])
    liste.append(['تاريخي', URL_MAIN + 'search/?search=فيلم&genre=25'])
    liste.append(['كوميديا', URL_MAIN + 'search/?search=فيلم&genre=8'])
    liste.append(['موسيقى', URL_MAIN + 'search/?search=فيلم&genre=131'])
    liste.append(['رياضي', URL_MAIN + 'search/?search=فيلم&genre=17986'])
    liste.append(['دراما', URL_MAIN + 'search/?search=فيلم&genre=27'])
    liste.append(['رعب', URL_MAIN + 'page/افلام-رعب/'])
    liste.append(['عائلى', URL_MAIN + 'search/?search=فيلم&genre=237'])
    liste.append(['فانتازيا', URL_MAIN + 'search/?search=فيلم&genre=73'])
    liste.append(['حروب', URL_MAIN + 'search/?search=فيلم&genre=79'])
    liste.append(['الجريمة', URL_MAIN + 'search/?search=فيلم&genre=26'])
    liste.append(['رومانسى', URL_MAIN + 'search/?search=فيلم&genre=37'])
    liste.append(['خيال علمى', URL_MAIN + 'search/?search=فيلم&genre=91'])
    liste.append(['اثارة', URL_MAIN + 'search/?search=فيلم&genre=36'])
    liste.append(['ﺗﺸﻮﻳﻖ ﻭﺇﺛﺎﺭﺓ', URL_MAIN + 'search/?search=فيلم&genre=342'])
    liste.append(['وثائقى', URL_MAIN + 'search/?search=فيلم&genre=195'])

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, icons + '/Genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()
      # (.+?) ([^<]+) .+?
    sPattern = '<div class="ItemBlock">.+?<a href="(.+?)".+?style="(.+?)"></div>.+?<h3>(.+?)</h3>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0] :
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            if "مسلسل"  in aEntry[2]:
                continue
 
            if "حلقة"  in aEntry[2]:
                continue
 
            
            sTitle = aEntry[2].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("مشاهده","").replace("برنامج","").replace("مترجمة","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("مشاهدة وتحميل","").replace("اون لاين","").replace("مشاهدة","").replace("مشاهده","").replace("مترجم","").replace("فيلم","").replace("اونلاين","").replace("اون لاين","").replace("برنامج","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("4K","").replace("All","").replace("BDRip","").replace("HDCAM","").replace("HDTC","").replace("HDTV","").replace("HD","").replace("720","").replace("HDCam","").replace("Full HD","").replace("1080","").replace("HC","").replace("Web-dl","").replace("انمي","")
 
 
            siteUrl = aEntry[0]
            sDesc = ""
            sThumb = aEntry[1].replace("background-image: url(","").replace(");","")
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

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', icons + '/next.png', oOutputParameterHandler)

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



    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()
    # (.+?) .+? ([^<]+)   
    sPattern = '<div class="ItemBlock">.+?<a href="(.+?)".+?style="(.+?)"></div>.+?<h3>(.+?)</h3>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0] :
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if "فلم"  in aEntry[2]:
                continue
            if "فيلم"  in aEntry[2]:
                continue
            if "movie"  in aEntry[2]:
                continue

            siteUrl = aEntry[0]
            
            sTitle = aEntry[2].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("مشاهده","").replace("برنامج","").replace("مترجمة","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("مشاهدة وتحميل","").replace("اون لاين","")
            sThumb = aEntry[1].replace("background-image: url(","").replace(");","")
            sDesc = ''
            sTitle = sTitle.split('موسم')[0].split('الحلقة')[0]
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')

			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', icons + '/next.png', oOutputParameterHandler)

        progress_.VSclose(progress_)
        
  # ([^<]+) .+? (.+?)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
      # (.+?) ([^<]+) .+?
	
def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'next page-numbers" href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return URL_MAIN + aResult[1][0]

    return False
	
def showEpisodes():
    import requests
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')



    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
     # (.+?) ([^<]+) .+?

    # (.+?) .+? ([^<]+)
    sPattern = '<a href="(.+?)" title=.+?class=.+?>(.+?)</a>' 

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
 
            sEp = aEntry[1].replace(" ","").replace("EP"," E")
            Ss = aEntry[1].replace(" ","").split("|")[0]
            sTitle = Ss+' '+sMovieTitle+' '+sEp
            sTitle = sTitle.replace("|","")
            siteUrl = aEntry[0]
            sThumb = sThumb
            sDesc = ''
            sYear = ''
			


            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory() 
	 
def showHosters():
    import requests
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    host = URL_MAIN.split('/')[2]


    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    # (.+?) ([^<]+)

    oParser = cParser()   
    sPattern = '<a data-like="likeCount" data-id="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if aResult[0]:
        sId = aResult[1][0]
        sId = sId
     # (.+?) ([^<]+) .+?
    oParser = cParser()
    sPattern = 'data-server="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

   
    if aResult[0]:
        for aEntry in aResult[1]:

            sTitle = 'server '
            siteUrl = URL_MAIN + 'wp-content/themes/EEE/Inc/Ajax/Single/Server.php'
            hdr = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0','referer' : URL_MAIN}
            params = {'post_id':sId,'server':aEntry}
            St=requests.Session()
            sdata = St.post(siteUrl,headers=hdr,data=params)
            sHtmlContent = sdata.content
            sPattern =  '<iframe.+?src="([^"]+)"'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                for aEntry in aResult[1]:
            
                    url = aEntry.split('\\')[0]
                    if url.startswith('//'):
                       url = 'http:' + url
            
                    sHosterUrl = url
                    if 'userload' in sHosterUrl:
                        sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN
                    if 'mystream' in sHosterUrl:
                        sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN   
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if oHoster:
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
				

                
    oGui.setEndOfDirectory()