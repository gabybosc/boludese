import re
from urllib.request import urlopen

"""
Busca en la wiki de hq donde empieza la lista de volúmenes y en cada uno los
capítulos que estén en ese vol.

Sirve para la wiki de hq pero supongo que con cambios mínimos se puede adaptar a
cualquiera.
"""


def lista(pattern_vol, pattern_ch, html):
    """
    Arma una lista vacía. Itera en volumen, escribe el titulo. Itera en ch, si
    está entre un volumen y el siguiente: lo agrega a ese título.
    Habría que buscar cómo hacer para que ponga los últimos capítulos
    (como no existe un post-último volumen, termina con los ch del anteúltimo vol)
    """
    lst = []
    end_vol_prev = 0

    for match_vol in re.finditer(pattern_vol, html):
        start_vol, end_vol = match_vol.span()
        vol_title = html[end_vol : end_vol + 10]

        for match_ch in re.finditer(pattern_ch, html):
            start_ch, end_ch = match_ch.span()
            ch_number = html[end_ch + 1 : end_ch + 4]

            if end_vol_prev < end_ch < end_vol:
                lst.append(int(ch_number))  # como int, puedo hacer str si quiero

        if vol_title not in lst:  # si ya está ese título, no lo escribe de nuevo
            lst.append(vol_title)
        end_vol_prev = end_vol

    return lst


def main_info(url):
    page = urlopen(url)
    html = page.read().decode("utf-8")

    pattern_ch = "\<li\>Chapter"
    pattern_vol = '\(Volume\)" title="'
    lst = lista(pattern_vol, pattern_ch, html)


# hq = "https://en.wikipedia.org/wiki/List_of_Haikyu!!_chapters"
hq = "https://haikyuu.fandom.com/wiki/Haiky%C5%AB!!_Volumes"
page = urlopen(hq)
html = page.read().decode("utf-8")

pattern_ch = "\<li\>Chapter"
pattern_vol = '\(Volume\)" title="'

# ahora mergea los pdfs según lo que dé la lista
from PyPDF2 import PdfMerger

[ch for ch in lst if type(ch) is str]

for i in lst:
    if type(i) is str:
        title = i
    if type(i) is int:
        pdf_1 = [f"ch{i}.pdf", f"ch{i}.pdf", "file3.pdf", "file4.pdf"]

        merger = PdfMerger()

        for pdf in pdfs:
            merger.append(pdf)

        merger.write("result.pdf")
        merger.close()
