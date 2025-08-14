# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.comaddon import isMatrix
import html.entities as htmlentitydefs
import urllib.parse as urllib
urlparse = urllib
import unicodedata
import re
import string


class cUtil:
    def CheckOrd(self, label):
        count = 0
        try:
            label = label.lower()
            label = label.strip()
            label = unicode(label, 'utf-8')
            label = unicodedata.normalize('NFKD', label).encode('ASCII', 'ignore')
            for i in label:
                count += ord(i)
        except:
            pass

        return count

    # str1 : les mots à rechercher
    # str2 : Liste des mots à comparer
    # percent : pourcentage de concordance, 75% = il faut au moins 3 mots sur 4
    # retourne True si pourcentage atteint
    def CheckOccurence(self, str1, str2, percent=75):
        str2 = self.CleanName(str2)
        nbOccurence = nbWord = 0
        list2 = str2.split(' ')   # Comparaison mot à mot
        for part in str1.split(' '):
            if len(part) == 1:    # Ignorer une seule lettre
                continue
            nbWord += 1           # nombre de mots au total
            if part in list2:
                nbOccurence += 1  # Nombre de mots correspondants

        if nbWord == 0:
            return False
        return 100*nbOccurence/nbWord >= percent

    def removeHtmlTags(self, sValue, sReplace=''):
        p = re.compile(r'<.*?>')
        return p.sub(sReplace, sValue)

    def formatTime(self, iSeconds):
        iSeconds = int(iSeconds)
        iMinutes = int(iSeconds / 60)
        iSeconds = iSeconds - (iMinutes * 60)
        if iSeconds < 10:
            iSeconds = '0' + str(iSeconds)

        if iMinutes < 10:
            iMinutes = '0' + str(iMinutes)

        return str(iMinutes) + ':' + str(iSeconds)

    def formatUTF8(self, text):
        # test si nécessaire de convertir
        n2 = re.sub('[^a-zA-Z0-9 ]', '', text)
        if n2 != text:
            bMatrix = isMatrix()
            if not bMatrix:
                try:
                    # converti en unicode pour aider aux convertions
                    text = text.decode('utf8', 'ignore')    
                except Exception as e:
                    pass

            try:
                text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore')
            except Exception as e:
                pass

            if bMatrix:
                try:
                    text = text.decode('utf8', 'ignore')
                except Exception as e:
                    pass
        return text

    def ASCIIDecode(self, string):
        i = 0
        l = len(string)
        ret = ''
        while i < l:
            c = string[i]
            if string[i:(i + 2)] == '\\x':
                c = chr(int(string[(i + 2):(i + 4)], 16))
                i += 3
            if string[i:(i+2)] == '\\u':
                c = chr(int(string[(i + 2):(i + 6)], 16))
                i += 5
            ret = ret + c
            i += 1
    
        return ret

    def unescape(self, text):
        # determine si conversion en unicode nécessaire        
        isStr = isinstance(text, str)

        def fixup(m):
            text = m.group(0)
            if text[:2] == '&#':
                # character reference
                if isStr:
                    if text[:3] == '&#x':
                        return chr(int(text[3:-1], 16))
                    else:
                        return chr(int(text[2:-1]))
                else:
                    if text[:3] == '&#x':
                        return unichr(int(text[3:-1], 16))
                    else:
                        return unichr(int(text[2:-1]))
            else:
                # named entity
                if isStr:
                    text = chr(htmlentitydefs.name2codepoint[text[1:-1]])
                else:
                    text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])

            return text  # leave as is

        return re.sub('&#?\w+;', fixup, text)

    def titleWatched(self, title):
        charMap = {
                    "\u0621": "'", "\u0622": "|", "\u0623": ">", "\u0624": "&",
                    "\u0625": "<", "\u0626": "}", "\u0627": "A", "\u0628": "b",
                    "\u0629": "p", "\u062A": "t", "\u062B": "v", "\u062C": "j",
                    "\u062D": "H", "\u062E": "x", "\u062F": "d", "\u0630": "*",
                    "\u0631": "r", "\u0632": "z", "\u0633": "s", "\u0634": "$",
                    "\u0635": "S", "\u0636": "D", "\u0637": "T", "\u0638": "Z",
                    "\u0639": "E", "\u063A": "g", "\u0640": "_", "\u0641": "f",
                    "\u0642": "q", "\u0643": "k", "\u0644": "l", "\u0645": "m",
                    "\u0646": "n", "\u0647": "h", "\u0648": "w", "\u0649": "Y",
                    "\u064A": "y", "\u064B": "F", "\u064C": "N", "\u064D": "K",
                    "\u064E": "a", "\u064F": "u", "\u0650": "i", "\u0651": "~",
                    "\u0652": "o", "\u0670": "`", "\u0671": "{", "\u067E": "P",
                    "\u0686": "J", "\u06A4": "V", "\u06AF": "G"
                    }
        title = ''.join(charMap.get(char, char) for char in title)
        title = self.formatUTF8(title)

        # cherche la saison et episode puis les balises [color]titre[/color]
        # title, saison = self.getSaisonTitre(title)
        # title, episode = self.getEpisodeTitre(title)
        # supprimer les balises
        title = re.sub(r'\[.*\]|\(.*\)', r'', str(title))
        title = title.replace('VF', '').replace('VOSTFR', '').replace('FR', '')
        # title = re.sub(r'[0-9]+?', r'', str(title))
        title = title.replace('-', ' ')  # on garde un espace pour que Orient-express ne devienne pas Orientexpress pour la recherche tmdb
        title = title.replace('Season', '').replace('season', '').replace('Season', '').replace('Episode', '').replace('episode', '')
        title = re.sub('[^%s]' % (string.ascii_lowercase + string.digits), ' ', title.lower())
        title = re.sub(' +', ' ', title) # vire espace double au milieu
        # title = QuotePlus(title)
        # title = title.decode('string-escape')
        return title

    def CleanName(self, name):

        name = Unquote(name)
        name = name.replace('%20', ' ')

        # on cherche l'annee
        annee = ''
        m = re.search('(\([0-9]{4}\))', name)
        if m:
            annee = str(m.group(0))
            name = name.replace(annee, '')

        # Suppression des ponctuations
        name = re.sub("[\’\'\-\–\:\+\._]", ' ', name)
        name = re.sub("[\,\&\?\!]", '', name)

        # vire tag
        name = re.sub('[\(\[].+?[\)\]]', '', name)
        name = name.replace('[', '').replace(']', '') # crochet orphelin

        # enlève les accents, si nécessaire
        name = self.formatUTF8(name)

        # tout en minuscule
        name = name.lower()
        # vire espace debut et fin
        name = name.strip()
        # vire espace double au milieu
        name = re.sub(' +', ' ', name)

        # on remet l'annee
        if annee:
            name = name + ' ' + annee

        return name

    def CleanMovieName(self, name):
        remove = [
            'تحميل و مشاهدة', 'مشاهدة وتحميل', 'مشاهدة', 'مسلسل', 'الانمي', 'الأنمي', 'الأنمى', 'أنمي', 'انمي', 'أنمى', 'انيمي', 'مترجم عربي',
            'مترجمة', 'مترجم', 'الفيلم', 'الفلم', 'فلم', 'فيلم', 'برنامج', 'مدبلج للعربية', 'والأخيرة', 'والاخيرة', 'الأخيرة', 'الاخيرة', 
            'Arabic', 'كاملة', 'حلقات كاملة', 'مباشرة', 'انتاج ', 'جودة عالية', 'كامل', 'السلسلة الوثائقية', 'الوثائقي', 'عرض', 'الرو ', 
            'جميع حلقات', 'سلسلة افلام', 'سلسلة اجزاء', 'تحميل', 'مشاهده', 'مباشره', 'للعربية', 'للعربي', 'اونلاين', 'أونلاين',
            'اون لاين', 'أون لاين', 'اولاين', 'المسلسل العائلي', 'كرتون', 'بجودة',

            'WEB-DL', 'BRRip', '720p', 'HD-TC', 'HDRip', 'HD-CAM', 'DVDRip', 'BluRay', '1080p', 'WEBRip', 'WEB-dl', '4K', 'All', 'BDRip', 'HDCAM',
            'HDTC', 'HDTV', 'HD', '720', 'HDCam', 'Full HD', '1080', 'بلوراي', 'HC', 'Web-dl', '2160p', ' hd ']
        
        for word in remove:
            name = name.replace(word, "")
        name = name.replace("Arabic","مدبلج")
       
        name = name.strip()
        if name.isdigit():
            name = name
        else:
            match = re.search('([0-9]{4})', name)
            if match:
                year = match.group(1)
                name = name.replace(year,"")

        return name


    def CleanSeriesName(self, name):
        remove = [
            'مشاهدة وتحميل', 'تحميل و مشاهدة', 'مشاهدة', 'المسلسل الباكستاني', 'مسلسل باكستاني', 'لمسلسل','مسلسل', 'الانمي', 'الأنمي', 
            'الأنمى', 'أنمي', 'انمي', 'أنمى', 'انيمي', 'مترجم عربي', 'مترجمة', 'مترجم', 'الفيلم', 'الفلم', 'فلم', 'فيلم', 'برنامج',          
            'مدبلج للعربية', 'والأخيرة', 'والاخيرة', 'الأخيرة', 'الاخيرة', 'Arabic', 'كاملة', 'حلقات كاملة', 'مباشرة', 'انتاج ',
            'جودة عالية', 'كامل', 'السلسلة الوثائقية', 'الوثائقي', 'عرض', 'الرو ', 'جميع حلقات', 'سلسلة افلام', 'بجودة',
            'سلسلة اجزاء', 'تحميل', 'مشاهده', 'مباشره', 'للعربية', 'للعربي', 'اونلاين', 'أونلاين', 'اون لاين',
            'أون لاين', 'اولاين', 'المسلسل العائلي', 'تقرير', '+', 'حلقات', 'الحلقات', ' ة ', 'القصير', 'جميع مواسم',

            'WEB-DL', 'BRRip', '720p', 'HD-TC', 'HDRip', 'HD-CAM', 'DVDRip', 'BluRay', '1080p', 'WEBRip', 'WEB-dl', '4K', 'All', 'BDRip', 'HDCAM',
            'HDTC', 'HDTV', 'HD', '720', 'HDCam', 'Full HD', '1080', 'بلوراي', 'HC', 'Web-dl', '2160p', ' hd ']
        
        for word in remove:
            name = name.replace(word, "")
        
        name = name.replace("Arabic","مدبلج")
        name = self.ConvertSeasons(name)
        
        try:
            name = name.split('الحلقه')[0].split('الحلقة')[0].split('حلقة')[0]
        except:
            name = name

        try:
            name = name.split('الموسم')[0].split('موسم')[0]
        except:
            name = name

        sSeason = ''
        match = re.search(r"S\d{1,2}", name)
        if match:
            sSeason = match.group(0)
            name = re.sub(sSeason, "", name)

        name = name.strip()

        if name.isdigit():
            name = f'{name} {sSeason}'
        else:
            match = re.search('([0-9]{4})', name)
            if match:
                year = match.group(1)
                name = f'{name.replace(year,"")} {sSeason}'
            else:
                 name = f'{name} {sSeason}'

        return name

    # Convert Seasons Arabic Names
    def ConvertSeasons(self, name):
        arabic_seasons = {
            "الجزء": "S", "الموسم العاشر": "S10", "الموسم الحادي عشر": "S11", "الموسم الثاني عشر": "S12", "الموسم الثالث عشر": "S13", 
            "الموسم الرابع عشر": "S14", "الموسم الخامس عشر": "S15", "الموسم السادس عشر": "S16", "الموسم السابع عشر": "S17", 
            "الموسم الثامن عشر": "S18", "الموسم التاسع عشر": "S19", "الموسم العشرون": "S20", "الموسم الحادي و العشرون": "S21", 
            "الموسم الحادي والعشرون": "S21", "الموسم الثاني والعشرون": "S22", "الموسم الثاني و العشرون": "S22", 
            "الموسم الثالث و العشرون": "S23", "الموسم الثالث والعشرون": "S23", "الموسم الرابع و العشرون": "S24", 
            "الموسم الرابع والعشرون": "S24", "الموسم الخامس و العشرون": "S25", "الموسم الخامس والعشرون": "S25", 
            "الموسم السادس و العشرون": "S26", "الموسم السادس والعشرون": "S26", "الموسم السابع و العشرون": "S27", 
            "الموسم السابع والعشرون": "S27", "الموسم الثامن و العشرون": "S28", "الموسم الثامن والعشرون": "S28", 
            "الموسم التاسع و العشرون": "S29", "الموسم التاسع والعشرون": "S29", "الموسم الثلاثون": "S30", 
            "الموسم الحادي و الثلاثون": "S31", "الموسم الحادي والثلاثون": "S31", "الموسم الثاني و الثلاثون": "S32", 
            "الموسم الثاني والثلاثون": "S32", "الموسم الثالث والثلاثون": "S33", "الموسم الثالث والثلاثون": "S33", 
            "الموسم الرابع والثلاثون": "S34", "الموسم الرابع و الثلاثون": "S34", "الموسم الخامس و الثلاثون": "S35", 
            "الموسم الخامس والثلاثون": "S35", "الموسم الاول": "S1", "الموسم الأول": "S1", "الموسم الثاني": "S2", "الموسم الثانى": "S2", "الموسم الثالث": "S3", 
            "الموسم الثالث": "S3", "الموسم الرابع": "S4", "الموسم الخامس": "S5", "الموسم السادس": "S6", "الموسم السابع": "S7", 
            "الموسم الثامن": "S8", "الموسم التاسع": "S9", "الموسم": "S", "موسم": "S", "S ": "S", "مترجمة": "", "مترجم": "", " الحادي عشر": "11", 
            "الثاني عشر": "12", "الثالث عشر": "13", " الرابع عشر": "14", "الخامس عشر": "15", " السادس عشر": "16", 
            "السابع عشر": "17", "الثامن عشر": "18", " التاسع عشر": "19", "العشرون": "20", "الحادي و العشرون": "21", 
            "الثاني و العشرون": "22", "الثالث و العشرون": "23", "الرابع والعشرون": "24", "الخامس و العشرون": "25", 
            "السادس والعشرون": "26", "السابع والعشرون": "27", "الثامن والعشرون": "28", " التاسع والعشرون": "29", 
            "الثلاثون": "30", "الحادي و الثلاثون": "31", "الثاني والثلاثون": "32", "الأول": "1", "الاول": "1", "الثاني": "2", 
            "الثانى": "2", "الثالث": "3", "الرابع": "4", "الخامس": "5", "السادس": "6", "السابع": "7", 
            "الثامن": "8", "التاسع": "9", "العاشر": "10", "Part": "S", "1st Season": "S1", "2nd Season": "S2" , "3rd Season": "S3",
            "4th Season": "S4", "5th Season": "S5", "6th Season": "S6", "7th Season": "S7", "8th Season": "S8", "Season": "S",}
        
        sPattern = r"(\b" + "|".join(arabic_seasons.keys()) + r"\b)"
        clean_name = re.sub(sPattern, lambda match: arabic_seasons[match.group(1)], name)
        clean_name = re.sub(r"\b S (\d+)", r" S\1", clean_name.strip())

        return clean_name

    def getSerieTitre(self, sTitle):
        serieTitle = re.sub(r'\[.*\]|\(.*\)', r'', sTitle)
        serieTitle = re.sub('[- –]+$', '', serieTitle)

        if '|' in serieTitle:
            serieTitle = serieTitle[:serieTitle.index('|')]

        return serieTitle

    def getEpisodeTitre(self, sTitle):
        string = re.search('(?i)(e(?:[a-z]+sode\s?)*([0-9]+))', sTitle)
        if string:
            sTitle = sTitle.replace(string.group(1), '').strip()
            return sTitle, True

        return sTitle, False

    def EvalJSString(self, s):
        s = s.replace(' ', '')
        try:
            s = s.replace('!+[]', '1').replace('!![]', '1').replace('[]', '0')
            s = re.sub(r'(\([^()]+)\+\[\]\)', '(\\1)*10)', s)  # si le bloc fini par +[] >> *10
            s = re.sub(r'\[([^\]]+)\]', 'str(\\1)', s)
            if s[0] == '+':
                s = s[1:]
            val = int(eval(s))
            return val
        except:
            return 0


"""
# ***********************
# Fonctions lights
# ***********************
# Pour les avoirs
# from resources.lib import util
# puis util.Unquote('test')
"""


def Unquote(sUrl):
    return urllib.unquote(sUrl)


def Quote(sUrl):
    return urllib.quote(sUrl)


def UnquotePlus(sUrl):
    return urllib.unquote_plus(sUrl)


def QuotePlus(sUrl):
    return urllib.quote_plus(sUrl)


def QuoteSafe(sUrl):
    return urllib.quote(sUrl, safe=':/')


def urlEncode(sUrl):
    return urllib.urlencode(sUrl)


def urlHostName(sUrl):  # retourne le hostname d'une Url
    return urlparse.urlparse(sUrl).hostname
