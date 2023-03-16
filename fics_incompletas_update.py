import os as os
import codecs
import string

import csv as csv
import pandas as pd

from mobi import Mobi  # https://pypi.org/project/mobi-reader/
import AO3  # https://github.com/ArmindoFlores/ao3_api

# from mobi import Mobi  # https://github.com/kroo/mobi-python


header = ["Title", "Author", "pairing", "WC", "Rating", "Summary", "url"]
path = "C:/Users/RainbowRider/Documents/hq/fics/"

"""
Mira en la fic list cuáles no están terminadas
Luego las busca en mfl y si fueron updateadas, las descarga
podría modificarlo para que lea la url (total está en la spreadsheet)
y las busque directamente. Quizás sea mejor.
"""


def spreadsheet(data):
    lst = []
    ch_lst = []
    idx_lst = []
    for i in range(len(data)):
        if data.iloc[i]["complete"] == False:
            lst.append(data.iloc[i]["Title"])  # me da los índices de las incompletas
            ch_lst.append(data.iloc[i]["chapters"])
            idx_lst.append(i)
    return (lst, ch_lst, idx_lst)


"""
Ahora tiene que recuperar los títulos de todos los mfl para ver cuáles están incompletos
"""

session = AO3.Session("liightmyfire", "redondos93")
mfl = session.get_marked_for_later()  # tarda un ratito pero no tanto. No los carga


# El dict para eliminar todos los caracteres especiales del título
delete_dict = {sp_character: "" for sp_character in string.punctuation}
table = str.maketrans(delete_dict)


def metadata(ww):
    ww.reload()
    tit = ww.title
    chap = ww.nchapters
    comp = ww.complete

    return (
        tit,
        chap,
        comp,
    )


def descargar():
    data = pd.read_csv(path + "fics en mfl.csv")

    lst, ch_lst, idx_lst = spreadsheet(data)
    for i in range(5):
        ww = mfl[i]
        tit, chap, comp = metadata(ww)
        tit = tit.translate(table)
        if tit in lst:
            idx = lst.index(tit)
            if (
                int(ch_lst[idx]) < chap
            ):  # si los caps que tiene son menos que los que marqué
                data.iloc[
                    idx_lst[idx], data.columns.get_loc("chapters")
                ] = chap  # updatea el número de caps
                data.iloc[
                    idx_lst[idx], data.columns.get_loc("complete")
                ] = comp  # updatea si está o no terminada
                data.to_csv(path + "fics en mfl.csv", index=False)
                ww.download_to_file(path + tit + ".mobi", filetype="MOBI")


descargar()
