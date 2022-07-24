import re
from urllib.request import urlopen

"""
Busca en la wiki de hq donde empieza la lista de volúmenes y en cada uno los
capítulos que estén en ese vol.

Sirve para la wiki de hq pero supongo que con cambios mínimos se puede adaptar a
cualquiera.
"""


def find_chapter(pattern_ch, html, end_vol):
    """
    le paso pattern_ch que es el patrón que se repite antes de que aparezca el
    número de capítulo. Busca las iteraciones en las que aparezca ese patrón
    y entre qué volúmenes aparece.
    """
    lst = []
    for match_ch in re.finditer(pattern_ch, html):
        start_ch, end_ch = match_ch.span()
        ch_number = html[end_ch + 1 : end_ch + 4]
        if end_vol < end_ch:
            lst.append(ch_number)

    return lst


def in_vol(pattern_vol, pattern_ch, html):
    for match_vol in re.finditer(pattern_vol, html):
        start_vol, end_vol = match_vol.span()
        vol_title = html[end_vol : end_vol + 20]
        ch = find_chapter(pattern_ch, html, end_vol)
        print(vol_title, ch)


def main_info(url):
    page = urlopen(url)
    html = page.read().decode("utf-8")

    pattern_ch = "\<li\>Chapter"
    pattern_vol = '\(Volume\)" title="'
    in_vol(pattern_vol, pattern_ch, html)


# itero en volumen y hago una lista con la posición en la que están


# hq = "https://en.wikipedia.org/wiki/List_of_Haikyu!!_chapters"
hq = "https://haikyuu.fandom.com/wiki/Haiky%C5%AB!!_Volumes"
main_info(hq)


# # para juntar los caps en un tomo:
#
# from PyPDF2 import PdfMerger
#
# pdfs = ["ch1.pdf", "ch2.pdf", "ch3.pdf", "ch4.pdf"]
#
# merger = PdfMerger()
#
# for pdf in pdfs:
#     merger.append(pdf)
#
# merger.write("Haikyuu!! Vol1.pdf")
# merger.close()
