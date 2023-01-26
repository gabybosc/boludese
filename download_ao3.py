"""
Hay dos que podrían servir, no puedo tener instalados ambos a la vez
https://github.com/alexwlchan/ao3 y https://github.com/ArmindoFlores/ao3_api
Uso el segundo
"""
# from ao3 import AO3  # https://github.com/alexwlchan/ao3
# from ao3.works import RestrictedWork
#
# api = AO3()
# api.login('liightmyfire', 'redondos93')
# work = api.work(id='258626')

"""
Mira todo lo que tenga en marked for later y lo
"""

import csv as csv
import codecs
import string
import os as os
import AO3  # https://github.com/ArmindoFlores/ao3_api

# import gspread
# from oauth2client.service_account import ServiceAccountCredentials

session = AO3.Session("liightmyfire", "redondos93")
mfl = session.get_marked_for_later()  # tarda un ratito pero no tanto. No los carga

# mfl[0] es el más reciente


pairings = {
    "Miya Atsumu/Sakusa Kiyoomi": "SakuAtsu",
    "Iwaizumi Hajime/Oikawa Tooru": "IwaOi",
    "Hinata Shouyou/Kageyama Tobio": "KageHina",
    "Akaashi Keiji/Bokuto Koutarou": "BokuAka",
    "Kozume Kenma/Kuroo Tetsurou": "KuroKen",
    "Sawamura Daichi/Sugawara Koushi": "DaiSuga",
    "Miya Osamu/Suna Rintarou": "OsaSuna",
    "Tendou Satori/Ushijima Wakatoshi": "UshiTen",
    "Azumane Asahi/Nishinoya Yuu": "AsaNoya",
    "Tsukishima Kei/Yamaguchi Tadashi": "TsukkiYama",
    "Kuroo Tetsurou/Tsukishima Kei": "KuroTsuki",
    "Bokuto Koutarou/Kuroo Tetsurou": "BoKuroo",
    "Hanamaki Takahiro/Matsukawa Issei": "MatsuHana",
    "Marco Bott/Jean Kirstein": "JeanMarco",
    "Hasegawa Langa/Kyan Reki": "Renga",
    "Getou Suguru/Gojo Satoru": "SatoSugu",
    "Jean Kirstein/Marco Bodt": "JeanMarco",
    "Reiner Braun/Jean Kirstein": "ReiJean",
    "Reiner Braun/Porco Galliard": "GalliRei",
    "Jean Kirstein/Eren Yeager": "EreJean",
    "Female Shepard/Garrus Vakarian": "Shakarian",
    "Kylo Ren/Rey": "Reylo",
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
path = "../hq/fics/"

lst = [fic for fic in os.listdir(path)]
titles = [titulo[:-5] for titulo in lst]

# El dict para eliminar todos los caracteres especiales del título
delete_dict = {sp_character: "" for sp_character in string.punctuation}
table = str.maketrans(delete_dict)

"""
Va a abrir los últimos 15 que tenga en mfl. Si los tengo bajados, no los descarga.
Si no, los baja
"""
with codecs.open(path + "fics en mfl.csv", "a", "utf-8") as f:  # "a" si quiero append
    archivo = csv.writer(f)
    # archivo.writerow(header)
    for i in range(0, 15):  # los últimos 15 que haya puesto en mfl
        ww = mfl[i]
        tit, author, ship, wc, rat, summ, link = metadata(ww)
        if tit not in titles:  # lo descarga sólo si no lo tengo ya bajado
            if pairings.get(ship) is None:
                archivo.writerow([tit, author, ship, wc, rat, summ, link])
            else:
                archivo.writerow([tit, author, pairings.get(ship), wc, rat, summ, link])
            # si quiero además descargarlos:
            tit = tit.translate(table)  # elimina los caracteres especiales
            ww.download_to_file(path + tit + ".mobi", filetype="MOBI")
