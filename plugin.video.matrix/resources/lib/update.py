# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.comaddon import addon, siteManager, VSlog
from resources.lib.handler.requestHandler import cRequestHandler
import datetime, time

class cUpdate:

    def getUpdateSetting(self):
        addons = addon()

        # If no old date = first installation, we force an old date
        setting_time = addons.getSetting('setting_time')
        if not setting_time:
            setting_time = '2000-09-23 10:59:50.877000'

        # update delay
        if addons.getSetting('auto_update_sites') == "true":
            try:
                siteManager()
            except:
                VSlog('error applying from local')
            time_now = datetime.datetime.now()
            time_service = self.__strptime(setting_time)
            time_sleep = datetime.timedelta(hours = 1)
            if time_now - time_service > time_sleep:
                sUrl = 'https://raw.githubusercontent.com/matrix/Dist/master/repo/plugin.video.matrix/resources/sites.json'
                oRequestHandler = cRequestHandler(sUrl)
                properties = oRequestHandler.request(jsonDecode=True)
                if properties == "":
                    return
                siteManager().setUserProps(properties)

                addons.setSetting('setting_time', str(time_now))


    # formattage date (bug python)
    def __strptime(self, date):
        if len(date) > 19:
            format = '%Y-%m-%d %H:%M:%S.%f'
        else:
            format = '%Y-%m-%d %H:%M:%S'
        try:
            date = datetime.datetime.strptime(date, format)
        except TypeError:
            date = datetime.datetime(*(time.strptime(date, format)[0:6]))
        return date
