#-*- coding: utf-8 -*-
# Venom.
# https://github.com/Kodi-bein/venom-xbmc-addons
#

from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.contextElement import cContextElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.player import cPlayer
from resources.lib.db import cDb
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.util import cUtil
import xbmc

class cHosterGui:

    SITE_NAME = 'cHosterGui'

    # step 1 - bGetRedirectUrl in ein extra optionsObject verpacken
    def showHoster(self, oGui, oHoster, sMediaUrl, sThumbnail, bGetRedirectUrl = False):
        
        #oInputParameterHandler = cInputParameterHandler()
        #aParams = oInputParameterHandler.getAllParameter()
        
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(self.SITE_NAME)
        #oGuiElement.setFunction('showHosterMenu')
        oGuiElement.setFunction('play')
        oGuiElement.setTitle(oHoster.getDisplayName())
        #oGuiElement.setThumbnail(sThumbnail)
        # if (oInputParameterHandler.exist('sMeta')):
            # sMeta = oInputParameterHandler.getValue('sMeta')
            # oGuiElement.setMeta(int(sMeta))
            
        oGuiElement.setFileName(oHoster.getFileName())
        oGuiElement.getInfoLabel()
        oGuiElement.setCat(4)
        #oGuiElement.setThumbnail(xbmc.getInfoLabel('ListItem.Art(thumb)'))
        if sThumbnail:
            oGuiElement.setThumbnail(sThumbnail)
            
        #oGuiElement.setMeta(1)
        oGuiElement.setIcon('host.png')
               
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMediaUrl', sMediaUrl)
        #oOutputParameterHandler.addParameter('sThumbnail', oGuiElement.getThumbnail())

        oOutputParameterHandler.addParameter('sHosterIdentifier', oHoster.getPluginIdentifier())
        oOutputParameterHandler.addParameter('bGetRedirectUrl', bGetRedirectUrl)
        oOutputParameterHandler.addParameter('sFileName', oHoster.getFileName())

        oOutputParameterHandler.addParameter('sTitle', oHoster.getDisplayName())
        oOutputParameterHandler.addParameter('sId', 'cHosterGui')
        oOutputParameterHandler.addParameter('siteUrl', sMediaUrl)
        #oOutputParameterHandler.addParameter('sFav', 'play')
        #oOutputParameterHandler.addParameter('sCat', '4')

        
        #context playlit menu
        oContext = cContextElement()
        oContext.setFile('cHosterGui')
        oContext.setSiteName(self.SITE_NAME)
        oContext.setFunction('addToPlaylist')
        oContext.setTitle(cConfig().getlanguage(30201))
        oContext.setOutputParameterHandler(oOutputParameterHandler)
        oGuiElement.addContextItem(oContext)
        
        
        
        #context FAV menu
        oGui.createContexMenuFav(oGuiElement, oOutputParameterHandler)
        
      
        #bug
        oGui.addHost(oGuiElement, oOutputParameterHandler)
         
        #oGui.addFolder(oGuiElement, oOutputParameterHandler)


        
        
    def checkHoster(self, sHosterUrl):
    
        #securitee
        if (not sHosterUrl):
            return False
        
        #Petit nettoyage
        sHosterUrl = sHosterUrl.split('|')[0]
        
        #Recuperation du host
        sHostName = sHosterUrl.split('/')[2]
            
        #L'user a active l'url resolver ?
        if cConfig().getSetting('UserUrlResolver') == 'true':
            import urlresolver
            hmf = urlresolver.HostedMediaFile(url=sHosterUrl)
            if hmf.valid_url():
                tmp = cHosterHandler().getHoster('resolver')
                RH = sHosterUrl.split('/')[2]
                RH = RH.replace('www.','')
                tmp.setRealHost( RH[:3].upper() )
                return tmp

        #Gestion classique
    
        if (('youtube' in sHostName) or ('youtu.be' in sHostName)):
            return cHosterHandler().getHoster('youtube')
        if (('dailymotion' in sHostName) or (('dai.ly' in sHostName))):
            return cHosterHandler().getHoster('dailymotion') 
            
        #Si aucun hebergeur connu on teste les liens directs
        if (sHosterUrl[-4:] in '.mp4.avi.flv.m3u8'):
            return cHosterHandler().getHoster('lien_direct')
            
        return False
        
    def play(self):
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()

        sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')
        sFileName = oInputParameterHandler.getValue('sFileName')
        #sThumbnail = oInputParameterHandler.getValue('sThumbnail')

        if (bGetRedirectUrl == 'True'):            
            sMediaUrl = self.__getRedirectUrl(sMediaUrl)

        cConfig().log("Hoster - play " + sMediaUrl)

        oHoster = cHosterHandler().getHoster(sHosterIdentifier)
        oHoster.setFileName(sFileName)

        sHosterName = oHoster.getDisplayName()
        cConfig().showInfo(sHosterName, 'Resolve')
        
        #oHoster.setUrl(sMediaUrl)
        #aLink = oHoster.getMediaLink()
        #return
        
        try:
        
            oHoster.setUrl(sMediaUrl)
            aLink = oHoster.getMediaLink()

            if (aLink[0] == True):
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(self.SITE_NAME)
                oGuiElement.setMediaUrl(aLink[1])
                oGuiElement.setTitle(oHoster.getFileName())
                oGuiElement.getInfoLabel()
                
                oPlayer = cPlayer()
                oPlayer.run(oGuiElement, oHoster.getFileName(), aLink[1])
                
                # oGuiElement = cGuiElement()
                # oGuiElement.setSiteName(self.SITE_NAME)
                # oGuiElement.setMediaUrl(aLink[1])
                # oGuiElement.setTitle(oHoster.getFileName())
                # oGuiElement.getInfoLabel()
                
                # oPlayer = cPlayer()
                # oPlayer.clearPlayList()
                # oPlayer.addItemToPlaylist(oGuiElement)
                # oPlayer.startPlayer()
                return
            else:
                #cConfig().showInfo(sHosterName, 'Fichier introuvable')
                cConfig().error("File not found")
                return

        except:
            #cConfig().showInfo(sHosterName, 'Fichier introuvable')
            cConfig().error("File not found")
            return

        oGui.setEndOfDirectory()

    def addToPlaylist(self):
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()

        sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')
        sFileName = oInputParameterHandler.getValue('sFileName')
        

        if (bGetRedirectUrl == 'True'):
            sMediaUrl = self.__getRedirectUrl(sMediaUrl)

        cConfig().log("Hoster - play " + sMediaUrl)
        oHoster = cHosterHandler().getHoster(sHosterIdentifier)
        oHoster.setFileName(sFileName)

        #try:

        oHoster.setUrl(sMediaUrl)
        aLink = oHoster.getMediaLink()

        if (aLink[0] == True):
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(self.SITE_NAME)
            oGuiElement.setMediaUrl(aLink[1])
            oGuiElement.setTitle(oHoster.getFileName())

            oPlayer = cPlayer()
            oPlayer.addItemToPlaylist(oGuiElement)
            oGui.showInfo('Playlist', str(oHoster.getFileName()), 5);
            return

        #except:
        # cConfig().log("could not load plugin " + sHosterFileName)

        oGui.setEndOfDirectory()

    

    def __getRedirectUrl(self, sUrl):
        oRequest = cRequestHandler(sUrl)
        oRequest.request()
        return oRequest.getRealUrl()

        

       
