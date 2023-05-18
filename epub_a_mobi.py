import os as os
import codecs
import AO3 # https://github.com/ArmindoFlores/ao3_api

"""
mira si los tengo en epub y si tienen más de un cap, los pasa a mobi

"""

path = "C:/Users/RainbowRider/Documents/hq/fics/"

lst = []
for fic in os.listdir(path):
    if fic[-4:] == "epub":
        if os.path.getsize(path+fic) > 50000:  # saca las muy livianas que seguro sean oneshots
            lst.append(fic)  # me da las que tengo en epub

titles = [titulo[:-5] for titulo in lst]

session = AO3.Session('liightmyfire', 'redondos93')
mfl = session.get_marked_for_later()  # tarda un ratito pero no tanto. No los carga

# mfl[0] es el más reciente
idx = [s if tit in s for s in titles]


pairings = {"Miya Atsumu/Sakusa Kiyoomi": "SakuAtsu",
            "Iwaizumi Hajime/Oikawa Tooru": "IwaOi",
            "Hinata Shouyou/Kageyama Tobio": "KageHina",
            "Akaashi Keiji/Bokuto Koutarou": "BokuAka",
            "Kozume Kenma/Kuroo Tetsurou": "KuroKen",
            "Sawamura Daichi/Sugawara Koushi": "DaiSuga",
            "Miya Osamu/Suna Rintarou":"OsaSuna",
            "Tendou Satori/Ushijima Wakatoshi":"UshiTen",
            "Azumane Asahi/Nishinoya Yuu":"AsaNoya",
            "Tsukishima Kei/Yamaguchi Tadashi":"TsukkiYama",
            "Kuroo Tetsurou/Tsukishima Kei": "KuroTsuki",
            "Bokuto Koutarou/Kuroo Tetsurou":"BoKuroo",
            "Hanamaki Takahiro/Matsukawa Issei":"MatsuHana",
            "Marco Bott/Jean Kirstein":"JeanMarco",
            "Hasegawa Langa/Kyan Reki":"Renga",
            "Getou Suguru/Gojo Satoru":"SatoSugu",
            "Jean Kirstein/Marco Bodt":"JeanMarco",
            "Reiner Braun/Jean Kirstein":"ReiJean",
            "Reiner Braun/Porco Galliard":"GalliRei",
            "Jean Kirstein/Eren Yeager":"EreJean",
            "Female Shepard/Garrus Vakarian":"Shakarian",
            "Kylo Ren/Rey":"Reylo",
            }


def metadata(ww):
    ww.reload()
    tit = ww.title
    author = ww.authors[0].url.split("/")[-1]
    ship = ww.relationships[0]
    fandom = ww.fandoms[0]
    rat = ww.rating[0]  # que sea sólo la primera letra
    summ = ww.summary
    if len(summ) > 300:
        summ = summ[:300]
    link = ww.url
    wc = ww.words
    return (tit, author, ship, wc, rat, summ, link)

header = ["Title", "Author", "pairing", "WC", "Rating", "Summary", "url"]

for i in range(353, 457):
    ww = mfl[i]
    tit, author, ship, wc, rat, summ, link  = metadata(ww)
    for s in titles:
        if tit in s:
            if ww.nchapters > 1:
                print(s, ww.nchapters)
                ww.download_to_file(path+tit+".mobi", filetype="MOBI")