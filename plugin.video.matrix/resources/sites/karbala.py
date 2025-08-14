# -*- coding: utf-8 -*-

import re	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import progress, VSlog, siteManager
from resources.lib.parser import cParser
 
SITE_IDENTIFIER = 'karbala'
SITE_NAME = 'Karbala TV'
SITE_DESC = 'arabic vod'
 
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

ISLAM_SHOWS = (f'{URL_MAIN}?partName=Lectures', 'showSeries')
ISLAM_QURAN = (f'{URL_MAIN}?partName=Quran', 'showSeries')
ISLAM_NASHEED = (f'{URL_MAIN}?partName=poems', 'showSeries')
ISLAM_GENRES = (URL_MAIN, 'showGenres')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ISLAM_QURAN[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'القرآن الكريم', 'quran.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ISLAM_SHOWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'دروس و محاضرات', '1/Programs.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ISLAM_NASHEED[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'قصائد و أناشيد', 'nsheed.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ISLAM_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showGenres', 'أقسام المكتبة المرئية', 'islm.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
		
def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []	
    liste.append( ['ادعية و زيارات',f'{URL_MAIN}?partName=Pra_Vis'] )
    liste.append( ['برامج دينية',f'{URL_MAIN}?partName=religious'] )
    liste.append( ['برامج حسينية',f'{URL_MAIN}?partName=hussien'] )
    liste.append( ['برامج ثقافية',f'{URL_MAIN}?partName=educational'] )
    liste.append( ['أفلام و مسلسلات',f'{URL_MAIN}?partName=series'] )
    liste.append( ['الاسرة و الطفل',f'{URL_MAIN}?partName=family'] )
 
    for sTitle,sUrl in liste:
 
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'islm.png', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()

def showSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
      oInputParameterHandler = cInputParameterHandler()
      sUrl = oInputParameterHandler.getValue('siteUrl')
      sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
      sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser() 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="col-md-3 taa">.+?href="([^"]+)".+?style="background-image:.+?["\']([^"\']+)["\'].+?<h3 class=".+?">(.+?)</h3>'
    aResult = oParser.parse(sHtmlContent, sPattern)	
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = aEntry[2]
            sYear = ''
            siteUrl = f'{URL_MAIN}{aEntry[0]}'
            sThumb = f'{URL_MAIN.split("/video")[0]}{aEntry[1]}'
            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()

def showEpisodes():
	oGui = cGui()
    
	oInputParameterHandler = cInputParameterHandler()
	sUrl = oInputParameterHandler.getValue('siteUrl')
	sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
	sThumb = oInputParameterHandler.getValue('sThumb')

	oParser = cParser()
	oRequestHandler = cRequestHandler(sUrl)
	sHtmlContent = oRequestHandler.request()

	sPattern = '<div class="col-md-3 taa">.+?href="([^"]+)" title="([^"]+)".+?background:url(.+?);'
	aResult = oParser.parse(sHtmlContent, sPattern)
	if aResult[0]:
		oOutputParameterHandler = cOutputParameterHandler()
		for aEntry in aResult[1]:
 
			sTitle = aEntry[1]
			siteUrl = f"{URL_MAIN.split('video')[0]}{aEntry[0]}"
			sThumb = f'{URL_MAIN.split("/video")[0]}{aEntry[2].replace("(","").replace(")","")}'
			sDesc = ""
			
			oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
			oOutputParameterHandler.addParameter('sThumb', sThumb)
			oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
	else:
		oGui.addText(SITE_IDENTIFIER,'[COLOR coral]'+'عذرا , لا يمكن تنفيذ هذا الطلب'+'[/COLOR]')
		sNextPage = __checkForNextPage(sHtmlContent)
		if sNextPage:
			oOutputParameterHandler = cOutputParameterHandler()
			oOutputParameterHandler.addParameter('siteUrl', sNextPage)
			oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

	oGui.setEndOfDirectory()
  
def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<b class="current".+?href="(.+?)"'	
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return URL_MAIN + aResult[1][0]

    return False

def showLinks():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
          
    sPattern = '<source src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:           
            sHosterUrl = f"{URL_MAIN.split('/video')[0]}{aEntry}"

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
		               
    oGui.setEndOfDirectory()

