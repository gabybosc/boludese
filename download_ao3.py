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
Mira todo lo que tenga en marked for later y lo descarga
También mira en la lista qué fics están sin terminar y chequea si hubo update
(en caso de que sí, la descarga) -> hace lo de fics_incompletas_update
"""

import csv as csv
import codecs
import string
import os as os
import AO3  # https://github.com/ArmindoFlores/ao3_api
from fics_incompletas_update import descargar_incompletas

# import gspread
# from oauth2client.service_account import ServiceAccountCredentials

session = AO3.Session("liightmyfire", "redondos93")
mfl = session.get_marked_for_later()  # tarda un ratito pero no tanto. No los carga

# mfl[0] es el más reciente


pairings = {
    "Miya Atsumu/Sakusa Kiyoomi": "SakuAtsu",
    "Iwaizumi Hajime/Oikawa Tooru": "IwaOi",
    "Hinata Shouyou/Miya Atsumu": "AtsuHina",
    "Hinata Shouyou/Kageyama Tobio": "KageHina",
    "Akaashi Keiji/Bokuto Koutarou": "BokuAka",
    "Kozume Kenma/Kuroo Tetsurou": "KuroKen",
    "Kuroo Tetsurou/Sawamura Daichi": "KuroDai",
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
    "Akaashi Keiji/Bokuto Koutarou/Kuroo Tetsurou/Tsukishima Kei": "BokuAkaKuroTsukki",
    "Akaashi Keiji/Bokuto Koutarou/Kuroo Tetsurou": "BoKuroAka",
    "Kuroo Tetsurou/Oikawa Tooru": "KuroOi",
    "Vash the Stampede/Nicholas D. Wolfwood": "VashWood",
}


relevant_tags = [
    "Alternate Universe",
    "Alternate Universe - Soulmates",
    "Alternate Universe - College/University",
    "Office AU",
    "Friends With Benefits",
    "Friends to Lovers",
    "Rivals to Lovers",
    "Enemies to Lovers",
    "Exes to Lovers",
    "Stangers to Lovers",
    "Idiots in Love",
    "Annoyances to Lovers",
    "Future fic",
    "Post-Canon",
    "Post-Time Skip",
    "Canon Compliant",
    "Genderswap",
    "Rule 63",
    "Dead Dove: Do Not Eat",
    "Humor",
    "Getting Together",
    "Fluff",
    "Angst",
    "Fluff and Angst",
    "Heavy Angst",
    "Smut",
    "Porn",
    "Anal",
    "Fingering",
    "Blow Jobs",
    "Hand Jobs",
    "Frottage",
    "Oral Sex",
    "Alien Sex",
    "Anal Sex",
    "Creampie",
    "Eventual smut",
    "Pining",
    "Mutual Pining",
    "Hurt/Comfort",
    "First Kiss",
    "Practice Kissing",
    "Plot What Plot/Porn Without Plot",
    "Porn With Plot",
    "Porn with Feelings",
    "Fake/Pretend Relationship",
    "Established Relationship",
    "Soulmates",
    "Jealousy",
    "Fix-It",
]

relevant_tags_dict = {
    "Alternate Universe": "AU",
    "Alternate Universe - Soulmates": "Soulmates",
    "Alternate Universe - College/University": "College AU",
    "Friends to Lovers": "FtL",
    "Rivals to Lovers": "RtL",
    "Enemies to Lovers": "EtL",
    "Stangers to Lovers": "StL",
    "Friends With Benefits": "FwB",
    "Fluff and Angst": "Fluff, Angst",
    "Porn With Plot": "pwp",
    "Heavy Angst": "Angst",
    "Porn": "Smut",
    "Anal": "Smut",
    "Anal Sex": "Smut",
    "Creampie": "Smut",
    "Oral Sex": "Smut",
    "Alien Sex": "Smut",
    "Blow Jobs": "Smut",
    "Fingering": "Smut",
    "Hand Jobs": "Smut",
    "Frottage": "Smut",
    "Eventual smut": "Smut",
    "Genderswap": "fem",
    "Rule 63": "fem",
    "Mutual Pining": "Pining",
    "Dead Dove: Do Not Eat": "DD:DNE",
    "Plot What Plot/Porn Without Plot": "PwoP",
    "Fake/Pretend Relationship": "Fake Dating",
}


def borrar(string, palabra):
    s = string.replace(palabra, "")
    return s


def taglist(ww):
    taglist = []
    for t in ww.tags:
        if t in relevant_tags:
            if relevant_tags_dict.get(t) is None:
                taglist.append(t)
            else:
                taglist.append(relevant_tags_dict.get(t))
    return set(taglist)  # para que no haya repetidas


def serie(ww):
    serie = ww.series
    if type(serie) == list and len(serie) > 0:
        ser = str(serie[0])
        for i in ["Series", "[", "]", "<", ">"]:
            ser = borrar(ser, i)
    else:
        ser = serie
    return ser


def ships(ww):
    ship = ww.relationships
    if type(ship) == list and len(ship) > 0:
        ship = ship[0]
    elif len(ship) == 0:
        ship = "ninguno"
    if pairings.get(ship) is None:
        sh = ship
    else:
        sh = pairings.get(ship)
    return sh


def metadata(ww):
    ww.reload()
    tit = ww.title
    author = ww.authors[0].url.split("/")[-1]
    fandom = ww.fandoms[0]
    rat = ww.rating[0]  # que sea sólo la primera letra
    summ = ww.summary
    if len(summ) > 300:
        summ = summ[:300]
    link = ww.url
    wc = ww.words
    chap = ww.nchapters
    date = ww.date_published
    kd = ww.kudos
    comp = ww.complete
    sh = ships(ww)
    taglst = taglist(ww)
    ser = serie(ww)

    fecha = str(date.year) + "-" + str(date.month)

    return (
        tit,
        author,
        sh,
        wc,
        rat,
        summ,
        ", ".join(taglst),
        fecha,
        ser,
        kd,
        fandom,
        link,
        chap,
        comp,
    )


header = ["Title", "Author", "pairing", "WC", "Rating", "Summary", "url"]
path = "../../hq/fics/"

# El dict para eliminar todos los caracteres especiales del título
delete_dict = {sp_character: "" for sp_character in string.punctuation}
table = str.maketrans(delete_dict)

lst = [fic for fic in os.listdir(path)]
titles = [
    titulo[:-5].translate(table) for titulo in lst
]  # los títulos sin caracteres especiales


def downloader(numero):
    """
    Va a abrir los últimos que tenga en mfl. Si los tengo bajados, no los descarga.
    Si no, los baja"""

    with codecs.open(
        path + "fics en mfl.csv", "a", "utf-8"
    ) as f:  # "a" si quiero append
        archivo = csv.writer(f)
        # archivo.writerow(header)
        for i in range(0, numero):  # los últimos 15 que haya puesto en mfl
            ww = mfl[i]
            md = metadata(ww)
            tit = md[0]
            tit = tit.translate(table)  # elimina los caracteres especiales
            if tit not in titles:  # lo descarga sólo si no lo tengo ya bajado
                archivo.writerow(md)
                # si quiero además descargarlos:
                chap = md[-2]
                if chap > 1:
                    ww.download_to_file(path + tit + ".mobi", filetype="MOBI")
                else:
                    ww.download_to_file(path + tit + ".epub", filetype="epub")


downloader(20)
descargar_incompletas()
