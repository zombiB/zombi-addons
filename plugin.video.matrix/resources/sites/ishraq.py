# -*- coding: utf-8 -*-

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import VSlog, addon
from resources.lib.parser import cParser
from resources.lib.util import Unquote
from resources.lib import random_ua

UA = random_ua.get_pc_ua()

SITE_IDENTIFIER = 'ishraq'
SITE_NAME = 'Ishraq Production'
SITE_DESC = 'farsi vod'

URL_MAIN = '' #'https://api.youtubemultidownloader.com/playlist'

MOVIE_IR = ('https://www.youtube.com/playlist?list=PLLHL37krqjBSFg_3CxMWe6G-jmyi5K2sX', 'showMovies')
SERIE_IR = ('https://www.youtube.com/@ISHRAQ_Production/playlists', 'showSeriesList')
ISLAM_SHOWS = ('https://www.youtube.com/playlist?list=PLLHL37krqjBQacDyxTDHtQmaSBKRMFe0w', 'showSeries')
KID_MOVIES = ('https://www.youtube.com/playlist?list=PLLHL37krqjBQdeWMtYOCH1hAtfDSfJ0EQ', 'showMovies')
ISLAM_GENRES = ('https://www.youtube.com/@ISHRAQ_Production/playlists', 'showGenres')

URL_SEARCH = ('', 'showSeries')
URL_SEARCH_MOVIES = ('', 'showMovies')
URL_SEARCH_SERIES = ('', 'showSeries')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_IR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30078), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_IR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', addons.VSlang(30079), '1/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_IR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesList', 'مسلسلات ايرانية', 'iran.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_IR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'افلام ايرانية', 'iran.png', oOutputParameterHandler) 

    oOutputParameterHandler.addParameter('siteUrl', KID_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'أفلام كرتون', '1/1/Anime.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ISLAM_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showGenres', 'أقسام المكتبة المرئية', 'islm.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return

def showGenres():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('user-agent', UA)
    sHtmlContent = oRequestHandler.request().decode("unicode_escape")

    sStart = 'var ytInitialData = '
    sEnd = '</script>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'primaryThumbnail.+?.+?"thumbnailViewModel".+?"url":"([^"]+)".+?"lockupMetadataViewModel".+?"content":"([^"]+)".+?"url":"([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            
            sTitle = str(aEntry[1].encode('latin-1'),'utf-8')
            siteUrl = f'https://www.youtube.com{aEntry[2]}'
            sThumb = aEntry[0]
            sDesc = ''
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            
            oGui.addTV(SITE_IDENTIFIER, 'showSeries', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
 
    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oInputParameterHandler = cInputParameterHandler()

    if sSearch:
        sUrl = MOVIE_IR[0]
    else:    
        sUrl = oInputParameterHandler.getValue('siteUrl')

    if not sSearch:
        if 'PLLHL37krqjBSk7ugG5v3_DeB_mVWMEAOQ' not in sUrl:
            oOutputParameterHandler.addParameter('siteUrl', 'https://www.youtube.com/playlist?list=PLLHL37krqjBSk7ugG5v3_DeB_mVWMEAOQ')
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'افلام ايرانية قصيرة', '1/Movies.png', oOutputParameterHandler) 

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('user-agent', UA)
    sHtmlContent = oRequestHandler.request().decode("unicode_escape")

    sStart = 'var ytInitialData = '
    sEnd = '</script>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'playlistVideoRenderer.+?"videoId":"([^"]+)".+?"url":"([^"]+)".+?"text":"([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            
            sTitle = str(aEntry[2].encode('latin-1'),'utf-8')
            sTitle = sTitle.replace('المسلسل','').replace('مسلسل','').replace(' - مترجم للعربية','').replace('الفيلم','').replace('الإيراني','').replace('(','').replace(')','').replace('4K','')
            if 'مسلسل' in sTitle or 'Deleted' in sTitle or 'Private' in sTitle:
                continue
            if sSearch:
                if Unquote(sSearch) not in sTitle:
                    continue
            siteUrl = f'https://www.youtube.com/watch?v={aEntry[0]}'
            sThumb = aEntry[1]
            sDesc = ''
            
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMovie(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    if not sSearch:

        oGui.setEndOfDirectory()

def showSeriesList():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('user-agent', UA)
    sHtmlContent = oRequestHandler.request().decode("unicode_escape")

    sStart = 'var ytInitialData = '
    sEnd = '</script>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'primaryThumbnail.+?.+?"thumbnailViewModel".+?"url":"([^"]+)".+?"lockupMetadataViewModel".+?"content":"([^"]+)".+?"url":"([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            
            sTitle = str(aEntry[1].encode('latin-1'),'utf-8')
            if 'مسلسل' not in sTitle:
                continue
            sTitle = sTitle.replace('المسلسل','').replace('مسلسل','').replace(' - مترجم للعربية','').replace('الفيلم','').replace('الإيراني','').replace('(','').replace(')','').replace('4K','')
            siteUrl = f'https://www.youtube.com{aEntry[2]}'
            sThumb = aEntry[0]
            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            
            oGui.addTV(SITE_IDENTIFIER, 'showSeries', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

 
    oGui.setEndOfDirectory()

def showSeries(sSearch = ''):
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oInputParameterHandler = cInputParameterHandler()

    if sSearch:
        sUrl = SERIE_IR[0]
    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('user-agent', UA)
    sHtmlContent = oRequestHandler.request().decode("unicode_escape")

    sStart = 'var ytInitialData = '
    sEnd = '</script>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'playlistVideoRenderer.+?"videoId":"([^"]+)".+?"url":"([^"]+)".+?"text":"([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler() 
        for aEntry in aResult[1]:
            
            sTitle = str(aEntry[2].encode('latin-1'),'utf-8')
            sTitle = sTitle.replace('المسلسل','').replace('مسلسل','').replace('الحلقة','E').replace('|','')
            if 'Deleted' in sTitle or 'Private' in sTitle:
                continue
            if sSearch:
                if Unquote(sSearch) not in sTitle:
                    continue
            siteUrl = f'https://www.youtube.com/watch?v={aEntry[0]}'
            sThumb = aEntry[1]
            sDesc = ''
            
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            
            oGui.addTV(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    if not sSearch:
 
        oGui.setEndOfDirectory()
		 
def showLink():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    oHoster = cHosterGui().checkHoster(sUrl)
    if oHoster != False:
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sUrl, sThumb)

    oGui.setEndOfDirectory()       
  