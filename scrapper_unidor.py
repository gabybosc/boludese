from PIL import Image
import os as os
import fnmatch
import glob
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
    filename = os.path.join(pathname, url.split("/")[-2]+ ".png")
    # filename = url.split("/")[-2] + ".png"
    print(filename)

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

def unidor(path, pdf_path):
    images = []
    files = glob.glob(os.path.expanduser(path+"*.png"))
    sorted_by_mtime_ascending = sorted(files, key=lambda t: os.stat(t).st_mtime)  # si se bajaron en orden, con esto las selecciona en orden

    for file in sorted_by_mtime_ascending:  #os.listdir(path):
        if fnmatch.fnmatch(file, "*.png"):
            images.append(file)

    final = [Image.open(f) for f in images]

    for i in range(len(final)):
        final[i].load()  # load es necesario porque a veces flashea y no abre bien los archivos

    final[0].save(
        pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=final[1:]
    )

for vol in range(251, 300):
    url = f"https://haikyuumanga.online/manga/haikyuu-chapter-{vol}/"
    path = f"../hq/vol_{vol}/"
    pdf_path = f"../hq/vol_{vol}.pdf"
    main(url, path)
    unidor(path, pdf_path)
