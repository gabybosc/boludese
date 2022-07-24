import requests
from bs4 import BeautifulSoup as bs
from google_drive_downloader import GoogleDriveDownloader as gdd

"""
Función para descargar pdfs (o lo que sea) de una página donde hay links de drive
Creo que no me deja hacer muchos de una por un tema de que es google y no quiere
que lo scrapeen
Pero de a 20 o 30 de unos 10mb salen
"""


def id_gdrive(url):
    """
    devuelve el id de uno o más links a archivos en drive en una página web
    """

    # hago esto porque a veces si no tira un error 403
    hed = requests.utils.default_headers()
    hed.update(
        {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0"
        }
    )

    # llama a la url
    req = requests.get(url, headers=hed)

    # hace la sopa
    soup = bs(req.content, "lxml")

    # hace una lista con los links de la sopa
    links = []
    for link in soup.findAll("a"):
        links.append(link.get("href"))

    links = list(filter(None, links))  # elimina los None si los hay

    # elije sólo los links que dicen "drive"
    id = [link.split("/")[5] for link in links if "drive" in link]

    # el id de drive es el quinto coso si tiene la forma
    # https://drive.google.com/file/d/1djZBi0ZO5Aj9zP4U5kdugXxiHJKLcO8o/view

    return id


def download_pdf(url):
    ch_start = int(input("last chapter downloaded\n"))
    id = id_gdrive(url)
    for ch in range(ch_start, ch_start + 20):
        gdd.download_file_from_google_drive(
            file_id=id[ch], dest_path=f"../../Documents/Haikyuu/ch{ch+1}.pdf"
        )


url = "https://www.popularanimehere.com/haikyuu-manga-online-read-download/"

download_pdf(url)
