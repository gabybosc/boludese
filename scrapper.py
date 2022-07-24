import requests
import os
from tqdm import tqdm
import time
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen
from google_drive_downloader import GoogleDriveDownloader as gdd

# from urllib3.exceptions import InsecureRequestWarning
# from urllib3 import disable_warnings

"""
saqué esta de https://www.thepythoncode.com/article/download-web-page-images-python
"""

# primero vemos que la URL sea válida
def is_valid(url):
    """
    Chequea que la url sea válida.
    netloc = domain name
    scheme = protocol
    Necesito asegurarme de que ambas existan
    """

    parsed = urlparse(url)

    return bool(parsed.netloc) and bool(parsed.scheme)


# ahora viene la función que agarra las imágenes
def get_all_images(url):
    """
    soup nos va a dar el contenido HTML de la página.
    find_all es el método que nos va a dar todos loe img elementos como lista
    tqdm me va a dar la progress bar nomás
    src me va la URL de una img tag, pero si no tienen src lo saltea y listo
    """
    soup = bs(requests.get(url).content, "html.parser")
    urls = []
    for img in tqdm(soup.find_all("img"), "Extracting images"):

        img_url = img.attrs.get("src")
        if not img_url:
            # si img no tiene src, lo saltea
            continue
        # aseguramos que la URL sea absoluta (?): si no lo es mergeamos el dominio con la URL recién extraída
        img_url = urljoin(url, img_url)

        # no queremos las URL que tengan http get key-values (???)
        # como estas se ven de la forma /image.png?c=3.2.5, nos fijamos de borrar
        # todo lo que venga después del ?. El try está para que si no hay, no nos dé error
        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass

        if is_valid(img_url):
            urls.append(img_url)

    return urls


# ahora la función que baja los archivos
def download(url, pathname):
    """
    Baja un archivo de una dada URL y lo guarda en cierto path
    """
    # si no existe, crea el path
    if not os.path.isdir(pathname):
        os.makedirs(pathname)

    # download the body of response by chunk, not immediately (?)
    response = requests.get(url, stream=True, timeout=3)

    # tamaño total del archivo
    file_size = int(response.headers.get("Content-Length", 0))

    # nombre del archivo
    filename = os.path.join(pathname, url.split("/")[-1])

    # progress bar con unidad de bytes
    progress = tqdm(
        response.iter_content(1024),
        f"Dowloading {filename}",
        total=file_size,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    )

    with open(filename, "wb") as f:
        for data in progress.iterable:
            # write data read to the file
            f.write(data)
            # progress bar
            progress.update(len(data))


# ahora sí la función principal
def main(url, path):
    # get all images
    imgs = get_all_images(url)
    for img in imgs:
        # time.sleep(5)
        # for each image, download it
        download(img, path)


# url = "https://stackoverflow.com/questions/16230850/httpsconnectionpool-max-retries-exceeded"
# url = "https://mangaplus.shueisha.co.jp/viewer/1000331"
# url = "https://w12.haikyuuu.com/manga/chapter-1-2/"
# main(url, "hq")

# url que tiene links de drive con los pdfs de los caps

"""
Función para descargar pdfs (o lo que sea) de una página donde hay links de drive
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
    soup = bs(req.content, "html")

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
    id = id_gdrive(url)
    for ch, f_id in enumerate(id):
        gdd.download_file_from_google_drive(file_id=f_id, dest_path=f"./ch{ch+1}.pdf")


url = "https://www.popularanimehere.com/haikyuu-manga-online-read-download/"
download_pdf(url)
