# -*- coding: utf-8 -*-

import re
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.util import cUtil
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog, siteManager, addon
from resources.lib import random_ua

UA = random_ua.get_ua()

SITE_IDENTIFIER = 'aflamfree'
SITE_NAME = 'Aflamfree'
SITE_DESC = 'arabic vod'	 
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_EN = (f'{URL_MAIN}category/افلام-اجنبية/', 'showMovies')
MOVIE_AR = (f'{URL_MAIN}category/افلام-عربية', 'showMovies')
MOVIE_ASIAN = (f'{URL_MAIN}category/افلام-اسيويه/', 'showMovies')
MOVIE_HI = (f'{URL_MAIN}category/افلام-هنديه/', 'showMovies')
MOVIE_TURK = (f'{URL_MAIN}category/افلام-تركية/', 'showMovies')
MOVIE_DUBBED = (f'{URL_MAIN}category/افلام-مدبلجة/', 'showMovies')
KID_MOVIES = (f'{URL_MAIN}category/افلام-كارتون/', 'showMovies')
MOVIE_ANNEES = (True, 'showYears')

URL_SEARCH = (f'{URL_MAIN}?s=', 'showMovies')
URL_SEARCH_MOVIES = (f'{URL_MAIN}?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
	oGui = cGui()
	addons = addon()

	oOutputParameterHandler = cOutputParameterHandler()
	oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH[0])
	oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), '1/Search.png', oOutputParameterHandler)

	oOutputParameterHandler.addParameter('siteUrl', MOVIE_EN[0])
	oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أجنبية', '1/Movies.png', oOutputParameterHandler)
   
	oOutputParameterHandler.addParameter('siteUrl', MOVIE_AR[0])
	oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام عربية', '1/Arabic.png', oOutputParameterHandler)
 
	oOutputParameterHandler.addParameter('siteUrl', MOVIE_ASIAN[0])
	oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام أسيوية', '1/Asian.png', oOutputParameterHandler)

	oOutputParameterHandler.addParameter('siteUrl', MOVIE_TURK[0])
	oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام تركية', '1/Turkish.png', oOutputParameterHandler)

	oOutputParameterHandler.addParameter('siteUrl', MOVIE_HI[0])
	oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام هندية', '1/Hindi.png', oOutputParameterHandler)
    
	oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
	oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', '1/1/Anime.png', oOutputParameterHandler)

	oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
	oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'أفلام (بالسنوات)', '1/Calendar.png', oOutputParameterHandler)

	oGui.setEndOfDirectory()

def showYears():
    import datetime
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(range(1921, int(datetime.datetime.now().year) + 1)):
        sYear = str(i)
        oOutputParameterHandler.addParameter('siteUrl', f'{URL_MAIN}release-year/' + sYear)  # / inutile
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sYear, '1/Calendar.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()
	
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText is not False:
        sUrl = f'{URL_MAIN}?s={sSearchText}'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showPack():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a href="([^<]+)">([^<]+)</a></li>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if 'المزيد' in aEntry[1] or 'اشترك' in aEntry[1]:
                continue
            sTitle = aEntry[1]
            sTitle = re.sub(r"[^\w\s]", "", sTitle)
            sThumb = ''
            siteUrl = aEntry[0]
            if siteUrl.startswith('/'):
                siteUrl = f'{URL_MAIN}{siteUrl}'

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
			
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, sThumb, oOutputParameterHandler)
 
    oGui.setEndOfDirectory()
			
def showMovies(sSearch = ''):
    oGui = cGui()

    if sSearch:
      sUrl = sSearch
    else:   
      oInputParameterHandler = cInputParameterHandler()
      sUrl = oInputParameterHandler.getValue('siteUrl')
      sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    if sSearch:
        psearch = sUrl.split('?s=')[1]
        oRequestHandler = cRequestHandler(f'{URL_MAIN}wp-content/themes/topcinma/Ajaxt/Searching.php')
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
        oRequestHandler.addParameters('search', psearch)
        oRequestHandler.setRequestType(1)
        sHtmlContent = oRequestHandler.request()

        sPattern = '<div class="SearchThumb">\s*<a href="([^"]+)".+?src="([^"]+)".+?alt="([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            total = len(aResult[1])
            progress_ = progress().VScreate(SITE_NAME)
            oOutputParameterHandler = cOutputParameterHandler()
            for aEntry in aResult[1]:
                progress_.VSupdate(progress_, total)
                if progress_.iscanceled():
                    break
                
                sTitle = cUtil().CleanMovieName(aEntry[2]).replace(' و ','')
                siteUrl = f'{aEntry[0]}/watch'
                sThumb = re.sub(r'-\d+x\d{0,3}','', aEntry[1])  
                sDesc = ''
                sYear = ''
                m = re.search('([0-9]{4})', sTitle)
                if m:
                    sYear = str(m.group(0))

                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sYear', sYear)
                oOutputParameterHandler.addParameter('sDesc', sDesc)

                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
            progress_.VSclose(progress_)

    else:
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
    
        sPattern = '<div class="Small--Box">\s*<a href="([^"]+)" title="([^"]+)".+?data-src="([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            total = len(aResult[1])
            progress_ = progress().VScreate(SITE_NAME)
            oOutputParameterHandler = cOutputParameterHandler()
            for aEntry in aResult[1]:
                progress_.VSupdate(progress_, total)
                if progress_.iscanceled():
                    break
                
                sTitle = cUtil().CleanMovieName(aEntry[1]).replace(' و','')
                siteUrl = aEntry[0]
                sThumb = re.sub(r'-\d+x\d{0,3}','', aEntry[2])  
                sDesc = ''
                sYear = ''
                m = re.search('([0-9]{4})', sTitle)
                if m:
                    sYear = str(m.group(0))

                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sYear', sYear)
                oOutputParameterHandler.addParameter('sDesc', sDesc)

                if 'assemblies' in siteUrl :			
                    oGui.addMovie(SITE_IDENTIFIER, 'showassemblies', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
                else:
                    siteUrl = aEntry[0]+'/watch'
                    oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                    oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
            progress_.VSclose(progress_)

    if not sSearch:
        sPattern = '<li><a class="page-numbers" href="([^<]+)">([^<]+)</a></li>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler()
            for aEntry in aResult[1]:
    
                sTitle = f'[COLOR red]Page: {aEntry[1]}[/COLOR]'
                siteUrl = aEntry[0]

                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                
                oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'next.png', oOutputParameterHandler)
 
        oGui.setEndOfDirectory()

def showassemblies():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    sStart = '<section class="tabContents">'
    sEnd = '</section>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<div class="Small--Box">.+?href="([^"]+)" title="([^"]+)".+?data-src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = (cUtil().CleanMovieName(aEntry[1])).replace('الحلقة ','E').replace('حلقة ','E')
            sTitle = cUtil().ConvertSeasons(sTitle)
            siteUrl = aEntry[0]+'/watch'
            sThumb = re.sub(r'-\d+x\d{0,3}','', aEntry[2])
            sDesc = ''
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')
            
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
        
    sPattern = '<li><a class="page-numbers" href="([^<]+)">([^<]+)</a></li>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
 
            sTitle = f'[COLOR red]Page: {aEntry[1]}[/COLOR]'
            siteUrl = aEntry[0]

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
			
            oGui.addDir(SITE_IDENTIFIER, 'showassemblies', sTitle, 'next.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()
  
def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'data-watch="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            sHosterUrl = aEntry
            if any(sHost in sHosterUrl for sHost in ['vidtube', 'vidhidepro', 'updown', 'ma2d', 'katomen']):
                sHosterUrl = f'{sHosterUrl}|Referer={URL_MAIN}'

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    else:
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]الموقع لم يضع الروابط.[/COLOR]')

    oGui.setEndOfDirectory()