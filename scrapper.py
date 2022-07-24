import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen
from google_drive_downloader import GoogleDriveDownloader as gdd


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
    response = requests.get(url, stream=True)

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
        # for each image, download it
        download(img, path)


main("https://w12.haikyuuu.com/manga/chapter-1-2/", "hq")

"""
Función para descargar pdfs (o lo que sea) de una página donde hay links de drive
"""

url = "https://www.popularanimehere.com/"
url = "https://www.popularanimehere.com/haikyuu-manga-online-read-download/"


def id_gdrive(url):
    req = Request(url)
    html_page = urlopen(req)

    # hace la sopa
    soup = bs(html_page, "lxml")

    # hace una lista con los links de la sopa
    links = []
    for link in soup.findAll("a"):
        links.append(link.get("href"))

    # elije sólo los links que dicen "drive"
    id = []
    # drive = []
    for link in links:
        if "drive" in link:
            # drive.append(link)
            id = link.split("/")[5]  # el id de drive es el quinto coso
            # url = "https://drive.google.com/file/d/1djZBi0ZO5Aj9zP4U5kdugXxiHJKLcO8o/view"

    return id


def download_pdf(url):
    id = id_gdrive(url)
    for ch, f_id in enumerate(id):
        gdd.download_file_from_google_drive(file_id=f_id, dest_path=f"./ch{ch}.pdf")


download_pdf(url)
