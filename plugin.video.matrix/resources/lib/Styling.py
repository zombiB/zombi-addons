from resources.lib.comaddon import addon

 
ADDON = addon()
icons = ADDON.getSetting('defaultIcons')


def getThumb(sTitle):
    sTitle = sTitle.replace("أ","ا").replace("آ","ا").replace("ة","ه")
    sThumb = None
    if 'افلام' in sTitle: 
        sThumb = icons + '/Movies.png'
    if 'مسلسلات' in sTitle: 
        sThumb = icons + '/TVShows.png'
    if 'أنمي' in sTitle: 
        sThumb = icons + '/Anime.png'
    if 'اجنبي' in sTitle: 
        sThumb = icons + '/Movies.png'
    if 'عربي' in sTitle: 
        sThumb = icons + '/Arabic.png'
    if 'عربيه' in sTitle: 
        sThumb = icons + '/Arabic.png'
    if 'تركيه' in sTitle: 
        sThumb = icons + '/Turkish.png'
    if 'تركي' in sTitle: 
        sThumb = icons + '/Turkish.png'
    if 'اسيوي' in sTitle: 
        sThumb = icons + '/Asian.png'
    if 'اسيويه' in sTitle: 
        sThumb = icons + '/Asian.png'
    if 'كوري' in sTitle: 
        sThumb = icons + '/Korean.png'
    if 'كوريه' in sTitle: 
        sThumb = icons + '/Korean.png'
    if 'هندي' in sTitle: 
        sThumb = icons + '/Hindi.png'
    if 'هنديه' in sTitle: 
        sThumb = icons + '/Hindi.png'
    if 'ياباني' in sTitle: 
        sThumb = icons + '/Japanese.png'
    if 'يابانية' in sTitle: 
        sThumb = icons + '/Japanese.png'
    if 'صيني' in sTitle: 
        sThumb = icons + '/Chinese.png'
    if 'صينية' in sTitle: 
        sThumb = icons + '/Chinese.png'
    if 'تايواني' in sTitle: 
        sThumb = icons + '/Taiwanese.png'
    if 'تايوانية' in sTitle: 
        sThumb = icons + '/Taiwanese.png'
    if 'تايلندي' in sTitle: 
        sThumb = icons + '/Thai.png'
    if 'تايلندية' in sTitle: 
        sThumb = icons + '/Thai.png'
    if 'فلبيني' in sTitle: 
        sThumb = icons + '/Filipino.png'
    if 'فلبينية' in sTitle: 
        sThumb = icons + '/Filipino.png'
    if 'فيتنامي' in sTitle: 
        sThumb = icons + '/Vietnamese.png'
    if 'فيتنامية' in sTitle: 
        sThumb = icons + '/Vietnamese.png'
        
    if 'مسلسلات اجنبيه' in sTitle: 
        sThumb = icons + '/TVShows.png'
    if 'برامج' in sTitle: 
        sThumb = icons + '/Programs.png'
    if 'وثائقي' in sTitle: 
        sThumb = icons + '/Documentary.png'
    if 'وثائقيه' in sTitle: 
        sThumb = icons + '/Documentary.png'
    if '4k' in sTitle: 
        sThumb = icons + '/4k.png'
    if 'اسلامي' in sTitle: 
        sThumb = icons + '/Islamic.png'
    if 'إسلامي' in sTitle: 
        sThumb = icons + '/Islamic.png'
    if 'رمضان' in sTitle: 
        sThumb = icons + '/Ramadan.png'
    if 'قرآن' in sTitle: 
        sThumb = icons + '/Quran.png'
    if 'اناشيد' in sTitle: 
        sThumb = icons + '/Anasheed.png'
    if 'كوميدي' in sTitle: 
        sThumb = icons + '/Comedy.png'
    if 'باكستاني' in sTitle: 
        sThumb = icons + '/Pakistani.png'
    if 'باكستانيه' in sTitle: 
        sThumb = icons + '/Pakistani.png'
    if 'رياضه' in sTitle: 
        sThumb = icons + '/Sport.png'
    if 'فاتبول' in sTitle: 
        sThumb = icons + '/Sport.png'
    if 'مباريات' in sTitle: 
        sThumb = icons + '/Sport.png'
    if 'مسرح' in sTitle: 
        sThumb = icons + '/Theater.png'
    if 'كلاسيكي' in sTitle: 
        sThumb = icons + '/MoviesClassic.png'
    if 'مصارعه' in sTitle: 
        sThumb = icons + '/WWE.png'
    if 'أخرى' in sTitle: 
        sThumb = icons + '/Misc.png'
    if 'هندي' in sTitle: 
        sThumb = icons + '/Hindi.png'
    if 'كرتون' in sTitle: 
        sThumb = icons + '/Cartoon.png'
    if 'كارتون' in sTitle: 
        sThumb = icons + '/Cartoon.png'
    if 'انمي' in sTitle: 
        sThumb = icons + '/Anime.png'
    if 'انيميشن' in sTitle: 
        sThumb = icons + '/Anime.png'
    if 'الانيميشن' in sTitle: 
        sThumb = icons + '/Anime.png'
    if 'اطفال' in sTitle: 
        sThumb = icons + '/Kids.png'
    if 'عائلي' in sTitle: 
        sThumb = icons + '/Family.png'
    if 'مدبلج' in sTitle: 
        sThumb = icons + '/Dubbed.png'
    if 'مترجم' in sTitle: 
        sThumb = icons + '/Subtitled.png'
    if 'تركيه مدبلجه' in sTitle: 
        sThumb = icons + '/TVShowsTurkish-Dubbed.png'
    if 'كوريه مدبلجه' in sTitle: 
        sThumb = icons + '/TVShowsKoean-Dubbed.png'
    if 'باسكتانيه مدبلجه' in sTitle: 
        sThumb = icons + '/TVShowsPakistani-Dubbed.png'
    if 'هنديه مدبلجه' in sTitle: 
        sThumb = icons + '/TVShowsHindi-Dubbed.png'
    if 'اسيويه مدبلجه' in sTitle: 
        sThumb = icons + '/TVShowsAsian-Dubbed.png'
    if 'بث' in sTitle:
        sThumb = icons + '/Live.png'
    if 'غير عائلي' in sTitle:
        sThumb = icons + '/18.png'
    if sThumb is None:
        sThumb = icons + '/None.png'
    return sThumb

def getFunc(sCat):
    if 'افلام' or 'الانيميشن' or 'ملتيميديا' in sCat:
        return 'showMovies'
    else:
        return 'showSeries'