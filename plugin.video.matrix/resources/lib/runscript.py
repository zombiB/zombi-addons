# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import json
import xbmcvfs
import xbmc
import xbmcgui
import sys

import urllib.request as urllib2
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import addon, dialog, VSlog, window, VSPath, siteManager

try:
    from sqlite3 import dbapi2 as sqlite
    VSlog('SQLITE 3 as DB engine')
except:
    from pysqlite2 import dbapi2 as sqlite
    VSlog('SQLITE 2 as DB engine')

SITE_IDENTIFIER = 'runscript'
SITE_NAME = 'runscript'

class cClear:

    DIALOG = dialog()
    ADDON = addon()

    def __init__(self):
        self.main(sys.argv[1])

    def main(self, env):

        if (env == 'resolveurl'):
            addon('script.module.resolveurl').openSettings()
            return

        elif (env == 'metahandler'):
            addon('script.module.metahandler').openSettings()
            return

        elif (env == 'changelog_old'):
            sUrl = 'https://raw.githubusercontent.com/matrix/Dist/master/repo/plugin.video.matrix/changelog.txt'
            try:
                oRequest = urllib2.Request(sUrl)
                oResponse = urllib2.urlopen(oRequest)

                # En python 3 on doit décoder la reponse
                if xbmc.getInfoLabel('system.buildversion')[0:2] >= '19':
                    sContent = oResponse.read().decode('utf-8')
                else:
                    sContent = oResponse.read()

                self.TextBoxes('matrix Changelog', sContent)
            except:
                self.DIALOG.VSerror("%s, %s" % (self.ADDON.VSlang(30205), sUrl))
            return

        elif (env == 'changelog'):

            sUrl = 'https://api.github.com/repos/matrix/Dist/commits'
            try:
                oRequest = urllib2.Request(sUrl)
                oResponse = urllib2.urlopen(oRequest)

                if xbmc.getInfoLabel('system.buildversion')[0:2] >= '19':
                    sContent = oResponse.read().decode('utf-8')
                else:
                    sContent = oResponse.read()

                result = json.loads(sContent)
                detailitems = []

                for item in result:
                    login = item['author']['login']
                    try:
                        desc = item['commit']['message']
                    except:
                        desc = 'None'
            
                    detailitems.append(desc)

                    cClear.TextBoxes(self, f'[B][COLOR gold]{login}[/COLOR][/B]', "\n\n".join(map(str, detailitems)))
            except:
                self.DIALOG.VSerror("%s, %s" % (self.ADDON.VSlang(30205), sUrl))
            return

        elif (env == 'soutient'):
            sUrl = 'https://raw.githubusercontent.com/matrix/Dist/master/repo/plugin.video.matrix/soutient.txt'
            try:
                oRequest = urllib2.Request(sUrl)
                oResponse = urllib2.urlopen(oRequest)

                # En python 3 on doit décoder la reponse
                if xbmc.getInfoLabel('system.buildversion')[0:2] >= '19':
                    sContent = oResponse.read().decode('utf-8')
                else:
                    sContent = oResponse.read()

                self.TextBoxes('matrix Soutient', sContent)
            except:
                self.DIALOG.VSerror("%s, %s" % (self.ADDON.VSlang(30205), sUrl))
            return

        elif (env == 'addon'):  # Vider le cache des métadonnées
            if self.DIALOG.VSyesno(self.ADDON.VSlang(30456)):
                cached_Cache = "special://home/userdata/addon_data/plugin.video.matrix/video_cache.db"
                # important seul xbmcvfs peux lire le special
                try:
                    cached_Cache = VSPath(cached_Cache).decode("utf-8")
                except AttributeError:
                    cached_Cache = VSPath(cached_Cache)

                try:
                    db = sqlite.connect(cached_Cache)
                    dbcur = db.cursor()
                    dbcur.execute('DELETE FROM movie')
                    dbcur.execute('DELETE FROM tvshow')
                    dbcur.execute('DELETE FROM season')
                    dbcur.execute('DELETE FROM episode')
                    db.commit()
                    dbcur.close()
                    db.close()
                    self.DIALOG.VSinfo(self.ADDON.VSlang(30090))
                except:
                    self.DIALOG.VSerror(self.ADDON.VSlang(30091))
            return

        elif (env == 'clean'):
            liste = ['Search history', 'Marque-Pages', 'Now Playing',
                     'Readings', 'Tagged views', 'Downloads']
            ret = self.DIALOG.VSselect(liste, self.ADDON.VSlang(30110))
            cached_DB = "special://home/userdata/addon_data/plugin.video.matrix/matrix.db"
            # important seul xbmcvfs peux lire le special
            try:
                cached_DB = VSPath(cached_DB).decode("utf-8")
            except AttributeError:
                cached_DB = VSPath(cached_DB)

            sql_drop = ""

            if ret > -1:

                if ret == 0:
                    sql_drop = 'DELETE FROM history'
                elif ret == 1:
                    sql_drop = 'DELETE FROM favorite'
                elif ret == 2:
                    sql_drop = 'DELETE FROM viewing'
                elif ret == 3:
                    sql_drop = 'DELETE FROM resume'
                elif ret == 4:
                    sql_drop = 'DELETE FROM watched'
                elif ret == 5:
                    sql_drop = 'DELETE FROM download'

                try:
                    db = sqlite.connect(cached_DB)
                    dbcur = db.cursor()
                    dbcur.execute(sql_drop)
                    db.commit()
                    dbcur.close()
                    db.close()
                    self.DIALOG.VSok(self.ADDON.VSlang(30090))
                except Exception as err:
                    self.DIALOG.VSerror(self.ADDON.VSlang(30091))
                    VSlog("Exception runscript sql_drop: {0}".format(err))
            return

        elif (env == 'xbmc'):
            if self.DIALOG.VSyesno(self.ADDON.VSlang(30456)):
                path = "special://temp/"
                try:
                    xbmcvfs.rmdir(path, True)
                    self.DIALOG.VSok(self.ADDON.VSlang(30092))
                except:
                    self.DIALOG.VSerror(self.ADDON.VSlang(30093))
            return

        elif (env == 'fi'):
            if self.DIALOG.VSyesno(self.ADDON.VSlang(30456)):
                path = "special://temp/archive_cache/"
                try:
                    xbmcvfs.rmdir(path, True)
                    self.DIALOG.VSok(self.ADDON.VSlang(30095))
                except:
                    self.DIALOG.VSerror(self.ADDON.VSlang(30096))
            return

        # activer toutes les sources
        elif (env == 'enableSources'):
            if self.DIALOG.VSyesno(self.ADDON.VSlang(30456)):
                sitesManager = siteManager()
                sitesManager.enableAll()
                sitesManager.save()
                self.DIALOG.VSinfo(self.ADDON.VSlang(30014))

            return

        # désactiver toutes les sources
        elif (env == 'disableSources' or env == 'disableSourcesSilent' ):
            if env == 'disableSources' and not self.DIALOG.VSyesno(self.ADDON.VSlang(30456)):
                return
            sitesManager = siteManager()
            sitesManager.disableAll()
            sitesManager.save()
            self.DIALOG.VSinfo(self.ADDON.VSlang(30014))

            return

        # Updates Sites
        elif (env == 'updatesites'):
            if self.DIALOG.VSyesno(self.ADDON.VSlang(30473)):
                import datetime
                addons = addon()
                time_now = datetime.datetime.now()
                sUrl = 'https://raw.githubusercontent.com/matrix/Dist/master/repo/plugin.video.matrix/resources/sites.json'
                oRequestHandler = cRequestHandler(sUrl)
                properties = oRequestHandler.request(jsonDecode=True)
                if properties == "":
                    return
                siteManager().setUserProps(properties)

                addons.setSetting('setting_time', str(time_now))

                self.DIALOG.VSinfo(self.ADDON.VSlang(30014))

            return

        # Updates Hosters
        elif (env == 'updatehosters'):
            addons = addon()
            sUrl = 'https://raw.githubusercontent.com/matrix/Dist/master/repo/plugin.video.matrix/resources/lib/gui/hoster.py'
            file_path = VSPath('special://home/addons/plugin.video.matrix/resources/lib/gui/hoster.py')
            if self.DIALOG.VSyesno(self.ADDON.VSlang(30456)):
                oRequestHandler = cRequestHandler(sUrl)
                sHosts = oRequestHandler.request()
                if sHosts == "":
                    return
                with open(file_path, 'w') as f:
                    f.write(sHosts)

                self.DIALOG.VSinfo(self.ADDON.VSlang(70021))

                return

        # aciver/désactiver les sources
        elif (env == 'search'):

            from resources.lib.handler.pluginHandler import cPluginHandler
            valid = '[COLOR green][x][/COLOR]'

            class XMLDialog(xbmcgui.WindowXMLDialog):

                ADDON = addon()
                sitesManager = siteManager()
                
                def __init__(self, *args, **kwargs):
                    xbmcgui.WindowXMLDialog.__init__(self)
                    pass

                def onInit(self):

                    self.container = self.getControl(6)
                    self.button = self.getControl(5)
                    self.getControl(3).setVisible(False)
                    self.getControl(1).setLabel(self.ADDON.VSlang(30094))
                    self.button.setLabel('OK')
                    listitems = []
                    oPluginHandler = cPluginHandler()
                    aPlugins = oPluginHandler.getAllPlugins()

                    #self.data = json.load(open(self.path))

                    for aPlugin in aPlugins:
                        # teste si deja dans le dsip
                        sPluginName = aPlugin[1]
                        isActive = self.sitesManager.isActive(sPluginName)
                        icon = "special://home/addons/plugin.video.matrix/resources/art/sites/%s.png" % sPluginName
                        stitle = self.sitesManager.getProperty(sPluginName, self.sitesManager.LABEL)

                        if isActive:
                            stitle = ('%s %s') % (stitle, valid)
                        listitem = xbmcgui.ListItem(label=stitle, label2=aPlugin[2])
                        listitem.setArt({'icon': icon, 'thumb': icon})
                        listitem.setProperty('Addon.Summary', aPlugin[2])
                        listitem.setProperty('sitename', aPlugin[1])
                        if isActive:
                            listitem.select(True)

                        listitems.append(listitem)
                    self.container.addItems(listitems)
                    self.setFocus(self.container)

                def onClick(self, controlId):
                    if controlId == 5:       # OK
                        self.sitesManager.save()
                        self.close()
                        return
                    elif controlId == 99:
                        window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
                        del window
                        self.close()
                        return
                    elif controlId == 7:
                        window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
                        del window
                        self.close()
                        return
                    elif controlId == 6:
                        item = self.container.getSelectedItem()
                        if item.isSelected() == True:
                            label = item.getLabel().replace(valid, '')
                            item.setLabel(label)
                            item.select(False)
                            sPluginSettingsName = item.getProperty('sitename')
                            self.sitesManager.setActive(sPluginSettingsName, False)
                        else:
                            label = ('%s %s') % (item.getLabel(), valid)
                            item.setLabel(label)
                            item.select(True)
                            sPluginSettingsName = item.getProperty('sitename')
                            self.sitesManager.setActive(sPluginSettingsName, True)
                        return

                def onFocus(self, controlId):
                    self.controlId = controlId

            path = "special://home/addons/plugin.video.matrix"
            wd = XMLDialog('DialogSelect.xml', path, "Default")
            wd.doModal()
            del wd
            return

        # Set Protected / Unprotected Site
        elif (env == 'cloudflare'):

            from resources.lib.handler.pluginHandler import cPluginHandler
            valid = '[COLOR red][Cloudflare][/COLOR]'

            class XMLDialog(xbmcgui.WindowXMLDialog):

                ADDON = addon()
                sitesManager = siteManager()
                
                def __init__(self, *args, **kwargs):
                    xbmcgui.WindowXMLDialog.__init__(self)
                    pass

                def onInit(self):

                    self.container = self.getControl(6)
                    self.button = self.getControl(5)
                    self.getControl(3).setVisible(False)
                    self.getControl(1).setLabel(self.ADDON.VSlang(30094))
                    self.button.setLabel('OK')
                    listitems = []
                    oPluginHandler = cPluginHandler()
                    aPlugins = oPluginHandler.getAllPlugins()

                    for aPlugin in aPlugins:
                        sPluginName = aPlugin[1]
                        isCloudFlare = self.sitesManager.isCloudFlare(sPluginName)
                        icon = "special://home/addons/plugin.video.matrix/resources/art/sites/%s.png" % sPluginName
                        stitle = self.sitesManager.getProperty(sPluginName, self.sitesManager.LABEL)

                        if isCloudFlare:
                            stitle = ('%s %s') % (stitle, valid)
                        listitem = xbmcgui.ListItem(label=stitle, label2=aPlugin[2])
                        listitem.setArt({'icon': icon, 'thumb': icon})
                        listitem.setProperty('Addon.Summary', aPlugin[2])
                        listitem.setProperty('sitename', aPlugin[1])
                        if isCloudFlare:
                            listitem.select(True)

                        listitems.append(listitem)
                    self.container.addItems(listitems)
                    self.setFocus(self.container)

                def onClick(self, controlId):
                    if controlId == 5:       # OK
                        self.sitesManager.save()
                        self.close()
                        return
                    elif controlId == 99:
                        window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
                        del window
                        self.close()
                        return
                    elif controlId == 7:
                        window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
                        del window
                        self.close()
                        return
                    elif controlId == 6:
                        item = self.container.getSelectedItem()
                        if item.isSelected() == True:
                            label = item.getLabel().replace(valid, '')
                            item.setLabel(label)
                            item.select(False)
                            sPluginSettingsName = item.getProperty('sitename')
                            self.sitesManager.setCloudFlare(sPluginSettingsName, False)
                        else:
                            label = ('%s %s') % (item.getLabel(), valid)
                            item.setLabel(label)
                            item.select(True)
                            sPluginSettingsName = item.getProperty('sitename')
                            self.sitesManager.setCloudFlare(sPluginSettingsName, True)
                        return

                def onFocus(self, controlId):
                    self.controlId = controlId

            path = "special://home/addons/plugin.video.matrix"
            wd = XMLDialog('DialogSelect.xml', path, "Default")
            wd.doModal()
            del wd
            return

        # Update Site Links
        elif (env == 'sitelink'):

            from resources.lib.handler.pluginHandler import cPluginHandler
            from resources.lib.gui.gui import cGui
            valid = '[COLOR red][Cloudflare][/COLOR]'
            oGui = cGui()
            
            class XMLDialog(xbmcgui.WindowXMLDialog):

                ADDON = addon()
                sitesManager = siteManager()
                
                def __init__(self, *args, **kwargs):
                    xbmcgui.WindowXMLDialog.__init__(self)
                    pass

                def onInit(self):

                    self.container = self.getControl(6)
                    self.button = self.getControl(5)
                    self.getControl(3).setVisible(False)
                    self.getControl(1).setLabel(self.ADDON.VSlang(30094))
                    self.button.setLabel('OK')
                    listitems = []
                    oPluginHandler = cPluginHandler()
                    aPlugins = oPluginHandler.getAllPlugins()

                    for aPlugin in aPlugins:
                        sPluginName = aPlugin[1]
                        siteURL = self.sitesManager.getUrlMain(sPluginName)
                        icon = "special://home/addons/plugin.video.matrix/resources/art/sites/%s.png" % sPluginName
                        stitle = self.sitesManager.getProperty(sPluginName, self.sitesManager.LABEL)
                        listitem = xbmcgui.ListItem(label=stitle, label2=siteURL)
                        listitem.setArt({'icon': icon, 'thumb': icon})
                        listitem.setProperty('Addon.Summary', aPlugin[2])
                        listitem.setProperty('sitename', aPlugin[1])
                        listitems.append(listitem)

                    self.container.addItems(listitems)
                    self.setFocus(self.container)

                def onClick(self, controlId):
                    if controlId == 5:       # OK
                        self.sitesManager.save()
                        self.sitesManager._saveSiteUpdates()
                        self.close()
                        return
                    elif controlId == 99:
                        window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
                        del window
                        self.close()
                        return
                    elif controlId == 7:
                        window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
                        del window
                        self.close()
                        return
                    elif controlId == 6:
                        item = self.container.getSelectedItem()
                        sNewUrl = oGui.showKeyBoard(sDefaultText=self.sitesManager.getUrlMain(item.getProperty('sitename')))
                        if sNewUrl:
                            item.setLabel2(sNewUrl)
                            item.select(True)
                            sPluginSettingsName = item.getProperty('sitename')
                            self.sitesManager.setUrlMain(sPluginSettingsName, sNewUrl)
                            return

                def onFocus(self, controlId):
                    self.controlId = controlId

            path = "special://home/addons/plugin.video.matrix"
            wd = XMLDialog('DialogSelect.xml', path, "Default")
            wd.doModal()
            del wd
            return

        elif (env == 'thumb'):

            if self.DIALOG.VSyesno(self.ADDON.VSlang(30098)):

                text = False
                path = "special://userdata/Thumbnails/"
                path_DB = "special://userdata/Database"
                try:
                    xbmcvfs.rmdir(path, True)
                    text = 'Clear Thumbnail Folder, Successful[CR]'
                except:
                    text = 'Clear Thumbnail Folder, Error[CR]'

                folder, items = xbmcvfs.listdir(path_DB)
                items.sort()
                for sItemName in items:
                    if "extures" in sItemName:
                        cached_Cache = "/".join([path_DB, sItemName])
                        try:
                            xbmcvfs.delete(cached_Cache)
                            text += 'Clear Thumbnail DB, Successful[CR]'
                        except:
                            text += 'Clear Thumbnail DB, Error[CR]'

                if text:
                    text = "%s (Important relancer Kodi)" % text
                    self.DIALOG.VSok(text)
            return

        elif (env == 'stalker'):
            from resources.lib import set_stalker
            set_stalker.setpvrstalker()
            return

        elif (env == 'sauv'):
            select = self.DIALOG.VSselect(['Import', 'Export'])
            DB = "special://home/userdata/addon_data/plugin.video.matrix/matrix.db"
            if select >= 0:
                try:
                    if select == 0:
                        # sélection d'un fichier
                        new = self.DIALOG.VSbrowse(1, 'matrix', "files")
                        if new:
                            xbmcvfs.delete(DB)
                            xbmcvfs.copy(new, DB)
                            self.DIALOG.VSinfo(self.ADDON.VSlang(30099))
                    elif select == 1:
                        # sélection d'un répertoire
                        new = self.DIALOG.VSbrowse(3, 'matrix', "files")
                        if new:
                            xbmcvfs.copy(DB, new + 'matrix.db')
                            self.DIALOG.VSinfo(self.ADDON.VSlang(30099))
                except:
                    self.DIALOG.VSerror(self.ADDON.VSlang(30100))

                return

        elif (env == 'cache'):
            if self.DIALOG.VSyesno(self.ADDON.VSlang(30456)):
                from requests_cache import CachedSession
                CACHE = 'special://home/userdata/addon_data/plugin.video.matrix/requests_cache.db'
                session = CachedSession(VSPath(CACHE))
                try:
                    session.cache.clear()
                    self.DIALOG.VSok(self.ADDON.VSlang(30089))
                except:
                    self.DIALOG.VSerror(self.ADDON.VSlang(30096))
            return

        elif (env == 'testpremium'):    # tester un compte premium
            from resources.lib.gui.hoster import cHosterGui
            oHoster = cHosterGui().getHoster("alldebrid")
            oHoster.testPremium()
            return

        else:
            return

        return

    # def ClearDir(self, dir, clearNested=False):
    #     try:
    #         dir = dir.decode("utf8")
    #     except:
    #         pass
    #     for the_file in os.listdir(dir):
    #         file_path = os.path.join(dir, the_file).encode('utf-8')
    #         if clearNested and os.path.isdir(file_path):
    #             self.ClearDir(file_path, clearNested)
    #             try:
    #                 os.rmdir(file_path)
    #             except Exception as e:
    #                 print(str(e))
    #         else:
    #             try:
    #                 os.unlink(file_path)
    #             except Exception as e:
    #                 print str(e)

    # def ClearDir2(self, dir, clearNested=False):
    #     try:
    #         dir = dir.decode("utf8")
    #     except:
    #         pass
    #     try:
    #         os.unlink(dir)
    #     except Exception as e:
    #         print(str(e))

    def TextBoxes(self, heading, anounce):
        # activate the text viewer window
        xbmc.executebuiltin("ActivateWindow(%d)" % 10147)
        # get window
        win = window(10147)
        # win.show()
        # give window time to initialize
        xbmc.sleep(100)
        # set heading
        win.getControl(1).setLabel(heading)
        win.getControl(5).setText(str(anounce))
        return


cClear()
