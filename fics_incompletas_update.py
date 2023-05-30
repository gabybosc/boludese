import os as os
import string
import csv as csv
import pandas as pd

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
    # me da los índices de las incompletas
    lst = []
    for i in range(len(data)):
        if data.iloc[i]["complete"] == False:
            # lst.append(data.iloc[i]["Title"])
            lst.append(i)
    return lst


session = AO3.Session("liightmyfire", "redondos93")


def get_from_spreadsheet(data, idx, colname):
    r = data.iloc[idx][colname]
    return r


# El dict para eliminar todos los caracteres especiales del título
delete_dict = {sp_character: "" for sp_character in string.punctuation}
table = str.maketrans(delete_dict)


def metadata(ww):
    ww.reload()
    tit = ww.title
    chap = ww.nchapters
    comp = ww.complete
    wc = ww.words

    return (
        tit,
        chap,
        comp,
        wc,
    )


def descargar_incompletas(filename):
    data = pd.read_csv(path + filename)

    lst = spreadsheet(data)
    for i in range(len(lst)):
        # print(lst[i])
        url = get_from_spreadsheet(data, lst[i], "url")
        chapter_ssheet = get_from_spreadsheet(data, lst[i], "chapters")
        workid = AO3.utils.workid_from_url(url)
        ww = AO3.Work(workid)
        tit, chap, comp, wc = metadata(ww)
        tit = tit.translate(table)
        # print(tit)
        if int(chapter_ssheet) < int(chap):
            # si los caps que tiene son más que los que dice la spreadsheet
            data.iloc[lst[i], data.columns.get_loc("chapters")] = chap
            # updatea el número de caps
            data.iloc[lst[i], data.columns.get_loc("complete")] = comp
            # updatea si está o no terminada
            data.iloc[lst[i], data.columns.get_loc("WC")] = wc
            # updatea el wordcount
            data.to_csv(path + filename, index=False)
            # escribe el csv
            ww.download_to_file(path + tit + ".mobi", filetype="MOBI")
            # descarga


descargar_incompletas("trigun_mfl.csv")
# descargar_incompletas("fics en mfl.csv")
