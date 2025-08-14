# -*- coding: utf-8 -*-

import requests
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

SITE_IDENTIFIER = 'smedia'
SITE_NAME = 'SalamMedia'
SITE_DESC = 'farsi vod'

URL_MAIN = ''   #'https://api.youtubemultidownloader.com/playlist'

MOVIE_IR = ('https://www.youtube.com/playlist?list=PL21RKgCL_dsy9O0BEDYAPaDmD32TjFSkm', 'showMovies')
SERIE_IR = ('https://www.youtube.com/@SalamMedia-Arabic/playlists', 'showSeriesList')
ISLAM_GENRES = ('https://www.youtube.com/@SalamMedia-Arabic/playlists', 'showGenres')

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

    oInputParameterHandler = cInputParameterHandler()
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
            if 'مسلسل' not in sTitle and 'الكهف' not in sTitle:
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
  