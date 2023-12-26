import csv as csv
import codecs
import string
import os as os
import AO3  # https://github.com/ArmindoFlores/ao3_api
from clear_cache import clear as clear_cache
from creds import creds

from fics_incompletas_update import descargar_incompletas
from time import sleep

"""
Hay dos que podrían servir, no puedo tener instalados ambos a la vez
https://github.com/alexwlchan/ao3 y https://github.com/ArmindoFlores/ao3_api
Uso el segundo
"""

"""
Mira todo lo que tenga en marked for later y lo descarga
También mira en la lista qué fics están sin terminar y chequea si hubo update
(en caso de que sí, la descarga) -> hace lo de fics_incompletas_update
"""


clear_cache(
    dir="."
)  # esto es porque por algún motivo, cuando lo corro, flashea y abre todo mi mfl

# import gspread
# from oauth2client.service_account import ServiceAccountCredentials

session = AO3.Session(creds["User"], creds["Password"])
print("abrió la sesión")
mfl = session.get_marked_for_later()  # tarda un ratito pero no tanto. No los carga
print("abrió la lista de mfl")
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
    "Akaashi Keiji/Bokuto Koutarou/Kuroo Tetsurou/Tsukishima Kei": "BokuAkaKuroTsukki",
    "Akaashi Keiji/Bokuto Koutarou/Kuroo Tetsurou": "BoKuroAka",
    "Hanamaki Takahiro/Matsukawa Issei": "MatsuHana",
    "Kuroo Tetsurou/Oikawa Tooru": "KuroOi",
    "Hasegawa Langa/Kyan Reki": "Renga",
    "Getou Suguru/Gojo Satoru": "SatoSugu",
    "Marco Bott/Jean Kirstein": "JeanMarco",
    "Jean Kirstein/Marco Bodt": "JeanMarco",
    "Reiner Braun/Jean Kirstein": "ReiJean",
    "Reiner Braun/Porco Galliard": "GalliRei",
    "Jean Kirstein/Eren Yeager": "EreJean",
    "Female Shepard/Garrus Vakarian": "Shakarian",
    "Commander Shepard/Garrus Vakarian": "Shakarian",
    "Kylo Ren/Rey": "Reylo",
    "Thanatos/Zagreus": "ThanZag",
    "Vash the Stampede/Nicholas D. Wolfwood": "VashWood",
    "Millions Knives/Vash the Stampede (Trigun)": "Plantcest",
    "Millions Knives/Vash the Stampede/Nicholas D. Wolfwood": "PlantWood",
    "Millions Knives/Nicholas D. Wolfwood/Vash the Stampede": "PlantWood",
    "Millions Knives/Nicholas D. Wolfwood": "KnivesWood",
    "Mitsurugi Reiji | Miles Edgeworth/Naruhodou Ryuuichi | Phoenix Wright": "NaruMitsu",
    "Mitsurugi Reiji/Naruhodou Ryuuichi | Miles Edgeworth/Phoenix Wright": "NaruMitsu",
    "Monkey D. Luffy/Roronoa Zoro": "ZoLu",
    "Lán Zhàn | Lán Wàngjī/Wèi Yīng | Wèi Wúxiàn": "WanXian",
}


relevant_tags = [
    "AU",
    "Alternate Universe",
    "Alternate Universe - Soulmates",
    "Alternate Universe - Modern Setting",
    "Alternate Universe - College/University",
    "Alternate Universe - Medieval",
    "Alternate Universe - Flower Shop",
    "Alternate Universe - Coffee Shop",
    "Alternate Universe - Modern Setting",
    "Alternate Universe - Canon Divergence",
    "Alternate Universe - Werewolf",
    "Alternate Universe - Vampire",
    "Alternate Universe - Pirates",
    "Office AU",
    "Time Travel",
    "Time Loop",
    "Reincarnation",
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
    "Canon Universe",
    "Genderswap",
    "Rule 63",
    "Dead Dove: Do Not Eat",
    "Humor",
    "Getting Together",
    "Fluff",
    "Angst",
    "Kissing",
    "Fluff and Angst",
    "Heavy Angst",
    "Angst with a Happy Ending",
    "Smut",
    "Porn",
    "Anal",
    "Rimming",
    "Rough Sex",
    "Fingering",
    "Blow Jobs",
    "Hand Jobs",
    "Frottage",
    "Oral Sex",
    "Alien Sex",
    "Anal Sex",
    "Wolfwood Eats Pussy Like A Champ",
    "Nicholas D. Wolfwood is Good at Cunnilingus",
    "Creampie",
    "Eventual smut",
    "Pining",
    "Mutual Pining",
    "Hurt/Comfort",
    "Practice Kissing",
    "First Kiss",
    "Plot What Plot/Porn Without Plot",
    "Porn With Plot",
    "PWP",
    "Porn with Feelings",
    "Fake/Pretend Relationship",
    "Established Relationship",
    "Soulmates",
    "Jealousy",
    "Fix-It",
    "Slow Burn",
    "Slow Build",
]

relevant_tags_dict = {
    "Alternate Universe": "AU",
    "Alternate Universe - Soulmates": "Soulmates",
    "Alternate Universe - College/University": "College AU",
    "Alternate Universe - Medieval": "Medieval AU",
    "Alternate Universe - Flower Shop": "Flower Shop AU",
    "Alternate Universe - Coffee Shop": "Coffee Shop AU",
    "Alternate Universe - Werewolf": "Werewolf AU",
    "Alternate Universe - Vampire": "Vampire AU",
    "Alternate Universe - Pirates": "Pirate AU",
    "Alternate Universe - Modern Setting": "Modern AU",
    "Time Travel": "Time Loop",
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
    "Rimming": "Smut",
    "Rough Sex": "Smut",
    "Anal Sex": "Smut",
    "Creampie": "Smut",
    "Oral Sex": "Smut",
    "Alien Sex": "Smut",
    "Blow Jobs": "Smut",
    "Fingering": "Smut",
    "Hand Jobs": "Smut",
    "Frottage": "Smut",
    "Nicholas D. Wolfwood is Good at Cunnilingus": "Smut",
    "Wolfwood Eats Pussy Like A Champ": "Smut",
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
    if "AU" in ww.tags or "Alternate Universe" in ww.tags:
        taglist.append("AU")
    return set(taglist)  # para que no haya repetidas


def serie(ww):
    serie = ww.series
    if type(serie) is list and len(serie) > 0:
        ser = str(serie[0])
        for i in ["Series", "[", "]", "<", ">"]:
            ser = borrar(ser, i)
    else:
        ser = serie
    return ser


def ships(ww):
    ship = ww.relationships
    if type(ship) is list and len(ship) > 0:
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


def assign_path(fandom):
    if "Haikyuu" in fandom:
        path = "../../fics/hq/"
    elif "Jujutsu" in fandom:
        path = "../../fics/jjk/"
    elif "Trigun" in fandom:
        path = "../../fics/trigun/"
    elif "Attorney" in fandom:
        path = "../../fics/aa/"
    elif "One Piece" in fandom:
        path = "../../fics/op/"
    elif "Shingeki" in fandom:
        path = "../../fics/snk/"
    else:
        path = "../../fics/"
    return path


header = ["Title", "Author", "pairing", "WC", "Rating", "Summary", "url"]
csv_path = "../../fics/"

# El dict para eliminar todos los caracteres especiales del título
delete_dict = {sp_character: "" for sp_character in string.punctuation}
table = str.maketrans(delete_dict)


def search_in_downloads(path, table):
    lst = [fic for fic in os.listdir(path)]
    titles = [
        titulo[:-5].translate(table) for titulo in lst
    ]  # los títulos sin caracteres especiales
    return titles


def writefile(filename, ww, tit, md):
    path = assign_path(md[-4])
    titles = search_in_downloads(path, table)
    with codecs.open(filename, "a", "utf-8") as f:
        archivo = csv.writer(f)
        if tit not in titles:  # lo descarga sólo si no lo tengo ya bajado
            archivo.writerow(md)
            # si quiero además descargarlos:
            ww.download_to_file(path + tit + ".epub", filetype="epub")


def downloader(numero):
    """
    Va a abrir los últimos que tenga en mfl. Si los tengo bajados, no los descarga.
    Si no, los baja"""

    # archivo.writerow(header)
    for i in range(0, numero):  # los últimos n que haya puesto en mfl
        ww = mfl[i]
        md = metadata(ww)
        tit = md[0]
        path = assign_path(md[-4])
        tit = tit.translate(table)  # elimina los caracteres especiales
        if (
            md[10] == "Trigun Stampede (Anime 2023)"
            or md[10] == "Trigun (Anime & Manga 1995-2008)"
        ):
            writefile(csv_path + "trigun_mfl.csv", ww, tit, md)
        else:
            writefile(csv_path + "fics en mfl.csv", ww, tit, md)
        if i % 5 == 0 and i != 0:
            sleep(120)  # cada cinco descansa


downloader(10)
print("download listo\n")
sleep(120)
# descargar_incompletas("trigun_mfl.csv")
# print("incompletas trigun listo\n")
# sleep(120)
# descargar_incompletas("fics en mfl.csv")
# print("incompletas etc listo\n")
