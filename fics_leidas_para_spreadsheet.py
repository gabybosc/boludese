import os as os
import codecs
import csv as csv

from mobi import Mobi  # https://pypi.org/project/mobi-reader/
import AO3  # https://github.com/ArmindoFlores/ao3_api

# from mobi import Mobi  # https://github.com/kroo/mobi-python


header = ["Title", "Author", "pairing", "WC", "Rating", "Summary", "url"]
path = "C:/Users/RainbowRider/Documents/hq/otras fics/"

"""
Lo primero es agarrar todos los títulos descargados.
Después va a agarrar una lista con los títulos que tengo en mfl.
Compara ambos.
Abre los que no tengo en mfl y busca la url a AO3
Va a AO3 y lee la metadata
Escribe un csv con lo relevante
"""

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


# títulos descargados
descargadas = []
for fic in os.listdir(path):
    descargadas.append(fic[:-5])

# títulos en mfl
sin_leer = []
with open(path + "lista.txt") as file:
    while line := file.readline().rstrip():
        sin_leer.append(line)

# quiero hacer una lista en la cual aparezcan sólo los que no están en mfl

leidas = []
for i in range(len(descargadas)):
    if descargadas[i][:10] not in sin_leer:
        leidas.append(descargadas[i])

with open(path + "leidas.txt", "a") as file:
    for i in range(len(leidas)):
        file.write(leidas[i] + "\n")

# obtengo el ID de ao3 de la fic
def obtain_id(work):
    book = Mobi(path + f"{work}.mobi")
    out = book.read()  # es un bytearray
    book.close()

    libro = (
        out.decode()
    )  # lo convierto a string para poder buscar adentro dónde está la info relevante
    idx = libro.find("http://archiveofourown.org/works/")  # busco el link
    url = libro[idx : idx + 41]  # la url

    # workid = AO3.utils.workid_from_url(url)
    workid = libro[idx + 33 : idx + 41]
    if '"' in workid:
        workid = workid[:-1]
    return workid


def metadata(workid):
    ww = AO3.Work(workid)
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


session = AO3.Session("liightmyfire", "redondos93")
session.refresh_auth_token()

with codecs.open(path + "fics leidas.csv", "a", "utf-8") as f:  # "a" si quiero append
    archivo = csv.writer(f)
    # archivo.writerow(header)
    for i in range(129, len(leidas)):
        workid = obtain_id(leidas[i])
        tit, author, ship, wc, rat, summ, link = metadata(workid)
        if pairings.get(ship) is None:
            archivo.writerow([tit, author, ship, wc, rat, summ, link])
        else:
            archivo.writerow([tit, author, pairings.get(ship), wc, rat, summ, link])
