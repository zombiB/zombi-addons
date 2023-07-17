from resources.lib.comaddon import addon, VSlog

 
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
    if 'فلسطين' in sTitle:
        sThumb = icons + '/Palestinian.png'
    if 'فلسطينيه' in sTitle:
        sThumb = icons + '/Palestinian.png'
    if 'الاردن' in sTitle:
        sThumb = icons + '/Jordanian.png'
    if 'اردنية' in sTitle:
        sThumb = icons + '/Jordanian.png'  
    if 'اردني' in sTitle:
        sThumb = icons + '/Jordanian.png' 
    if 'سوريا' in sTitle:
        sThumb = icons + '/Syrian.png'
    if 'سوريه' in sTitle:
        sThumb = icons + '/Syrian.png'
    if 'لبنان' in sTitle:
        sThumb = icons + '/Lebanese.png'
    if 'لبناني' in sTitle:
        sThumb = icons + '/Lebanese.png'
    if 'لبنانيه' in sTitle:
        sThumb = icons + '/Lebanese.png'
    if 'عراق' in sTitle:
        sThumb = icons + '/Iraqi.png'  
    if 'العراق' in sTitle:
        sThumb = icons + '/Iraqi.png' 
    if 'عراقي' in sTitle:
        sThumb = icons + '/Iraqi.png'
    if 'عراقية' in sTitle:
        sThumb = icons + '/Iraqi.png' 
    if 'تونس' in sTitle:
        sThumb = icons + '/Tunisian.png'
    if 'تونسي' in sTitle:
        sThumb = icons + '/Tunisian.png'
    if 'تونسيه' in sTitle:
        sThumb = icons + '/Tunisian.png'
    if 'مغرب' in sTitle:
        sThumb = icons + '/Moroccan.png'  
    if 'مغربي' in sTitle:
        sThumb = icons + '/Moroccan.png' 
    if 'مغربيه' in sTitle:
        sThumb = icons + '/Moroccan.png'
    if 'جزائر' in sTitle:
        sThumb = icons + '/Algerian.png'
    if 'جزائري' in sTitle:
        sThumb = icons + '/Algerian.png'
    if 'جزائرية' in sTitle:
        sThumb = icons + '/Algerian.png'
    if 'ليبيا' in sTitle:
        sThumb = icons + '/Libyan.png'
    if 'ليبي' in sTitle:
        sThumb = icons + '/Libyan.png'  
    if 'ليبيه' in sTitle:
        sThumb = icons + '/Libyan.png' 
    if 'امارات' in sTitle:
        sThumb = icons + '/UAE.png'
    if 'الامارات' in sTitle:
        sThumb = icons + '/UAE.png' 
    if 'اماراتي' in sTitle:
        sThumb = icons + '/UAE.png'
    if 'اماراتيه' in sTitle:
        sThumb = icons + '/UAE.png'  
    if 'السعودية' in sTitle:
        sThumb = icons + '/Saudi.png'
    if 'سعودي' in sTitle:
        sThumb = icons + '/Saudi.png'
    if 'الكويت' in sTitle:
        sThumb = icons + '/Kuwaiti.png'
    if 'كويتي' in sTitle:
        sThumb = icons + '/Kuwaiti.png'  
    if 'كويتية' in sTitle:
        sThumb = icons + '/Kuwaiti.png' 
    if 'عمان' in sTitle:
        sThumb = icons + '/Omani.png'
    if 'عماني' in sTitle:
        sThumb = icons + '/Omani.png'
    if 'عمانيه' in sTitle:
        sThumb = icons + '/Omani.png'
    if 'االبحرين' in sTitle:
        sThumb = icons + '/Bahraini.png'
    if 'بحريني' in sTitle:
        sThumb = icons + '/Bahraini.png'
    if 'بحرينية' in sTitle:
        sThumb = icons + '/Bahraini.png'  
    if 'قطر' in sTitle:
        sThumb = icons + '/Qatari.png' 
    if 'قطري' in sTitle:
        sThumb = icons + '/Qatari.png'
    if 'قطرية' in sTitle:
        sThumb = icons + '/Qatari.png' 
    if 'الخليج' in sTitle:
        sThumb = icons + '/ArabGulf.png'
    if 'خليجي' in sTitle:
        sThumb = icons + '/ArabGulf.png'  
    if 'خليجية' in sTitle:
        sThumb = icons + '/ArabGulf.png'  
    if 'مصري' in sTitle:
        sThumb = icons + '/Egyptian.png'  
    if 'مصرية' in sTitle:
        sThumb = icons + '/Egyptian.png'
        
    if sThumb is None:
        sThumb = icons + '/None.png'
    return sThumb

def getFunc(sCat):
    if 'افلام' or 'الانيميشن' or 'ملتيميديا' in sCat:
        return 'showMovies'
    else:
        return 'showSeries'
        

def getGenreIcon(sTitle):
    sTitle = sTitle.replace("أ","ا").replace("آ","ا").replace("ة","ه").strip()
    genre = False
    
    if 'كوميديا' in sTitle:
         genre =  'Comedy'
    if 'كوميدي' in sTitle:
         genre =  'Comedy'
    if 'رعب' in sTitle:
         genre =  'Horror'
    if 'اكشن' in sTitle:
         genre =  'Action'
    if 'اثاره' in sTitle:
         genre =  'Thriller'
    if 'غموض' in sTitle:
         genre =  'Mystery'
    if 'مغامره' in sTitle:
         genre =  'Adventure'
    if 'دراما' in sTitle:
         genre =  'Drama'
    if 'جريمه' in sTitle:
         genre =  'Crime'
    if 'رومانسيه' in sTitle:
         genre =  'Romance'
    if 'خيال علمي' in sTitle:
         genre =  'sci-fi'
    if 'سيره ذاتيه' in sTitle:
         genre =  'biography'
    if 'خيال' in sTitle:
         genre =  'fantasy'
    if 'حرب' in sTitle:
         genre =  'War'
    if 'عائليه' in sTitle:
         genre =  'Family'
    if 'غربيه' in sTitle:
         genre =  'Western'
    if 'موسيقيه' in sTitle:
         genre =  'Musical'
    if 'وثائقيه' in sTitle:
         genre =  'Documentary'
    if 'فنتازيا' in sTitle:
         genre =  'Fantasy'
    if 'فانتازيا' in sTitle:
         genre =  'Fantasy'
    if 'سامبا' in sTitle:
         genre =  'samba'
    if 'سالسا' in sTitle:
         genre =  'slasa'
    if 'شرقي' in sTitle:
         genre =  'oriental'
    if 'موسيقي' in sTitle:
         genre =  'Musical'
    if 'وثائقي' in sTitle:
         genre =  'Documentary'
    if 'رومانس' in sTitle:
         genre =  'Romance'
    if 'جرائم' in sTitle:
         genre =  'Crime'
    if 'مغامرات' in sTitle:
         genre =  'Adventure'
    if 'غربي' in sTitle:
         genre =  'Western'
    if 'ويسترن' in sTitle:
         genre =  'Western'
    if 'عائلي' in sTitle:
         genre =  'Family'
    if 'خيالي' in sTitle:
         genre =  'Fiction'
    if 'خياليه' in sTitle:
         genre =  'Fiction'
    if 'فضاء' in sTitle:
         genre =  'aliens'
    if 'فضائيين' in sTitle:
         genre =  'aliens'
    if 'فضائي' in sTitle:
         genre =  'aliens'
    if 'اطفال' in sTitle:
         genre =  'children'
    if 'كريسماس' in sTitle:
         genre =  'christmas'
    if 'اعيادميلاد' in sTitle:
         genre =  'christmas'
    if 'كلاسيكي' in sTitle:
         genre =  'classical'
    if 'كلاسيكيه' in sTitle:
         genre =  'classical'
    if 'كوارث' in sTitle:
         genre =  'disaster'
    if 'ديزني' in sTitle:
         genre =  'disney'
    if 'الكتروني' in sTitle:
         genre =  'electronic'
    if 'تاريخ' in sTitle:
         genre =  'history'
    if 'تاريخي' in sTitle:
         genre =  'history'
    if 'شرطه' in sTitle:
         genre =  'police'
    if 'قصير' in sTitle:
         genre =  'short'
    if 'فصيره' in sTitle:
         genre =  'short'
    if 'روح' in sTitle:
         genre =  'soul'
    if 'روحاني' in sTitle:
         genre =  'soul'
    if 'روحانيه' in sTitle:
         genre =  'soul'
    if 'ارواح' in sTitle:
         genre =  'soul'
    if 'رياضه' in sTitle:
         genre =  'sport'
    if 'رياضي' in sTitle:
         genre =  'sport'
    if 'استوائي' in sTitle:
         genre =  'tropical'
    if 'استوائيه' in sTitle:
         genre =  'tropical'
    if 'حروب' in sTitle:
         genre =  'war'
    if 'كرتون' in sTitle:
         genre =  'kids'
    if 'كارتون' in sTitle:
         genre =  'kids'
    if 'انمي' in sTitle:
         genre =  'Anime'
    if 'انيميشن' in sTitle:
         genre =  'Anime'
    if 'رومنسي' in sTitle:
         genre =  'Romance'
    if 'غريبه' in sTitle:
         genre =  'mystery'
    if 'غريب' in sTitle:
         genre =  'mystery'
    if 'موسيقى' in sTitle:
         genre =  'music'
    if 'موسيقي' in sTitle:
         genre =  'music'
    if 'موسيقيه' in sTitle:
         genre =  'music'
    if 'خارق للطبيعه' in sTitle:
         genre =  'soul' 
         
    if genre:
        return 'genres/' + str(genre.lower()) + '.png'
    else:
        return False
        
