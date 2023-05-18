from PIL import Image
import os as os
from pypdf import PdfMerger
import glob
import re

_nsre = re.compile("([0-9]+)")  # para que funcione el natural sort


def natural_sort_key(s):
    """https://stackoverflow.com/questions/19366517/how-to-sort-a-list-containing-alphanumeric-values
    básicamente, el sort normal me hace 1-10-100-11, etc, no 1-2-3-..-10-..100. Pero además, como los nombres son
    str que tienen a vece el signo +, necesito que "2+3" vaya antes del 4 y después del 1.
    """
    return [
        int(text) if text.isdigit() else text.lower() for text in re.split(_nsre, s)
    ]


for vol in range(1, 15):
    # for vol in range(1, 3):
    # path = f"../../Trigun Ultimate Final Files/Trigun Ultimate Vol {vol}/"
    # path = f"../../Trigun Ultimate Final Files/Trigun Ultimate - Mulitple Bullets/"
    path = f"../../Trigun Ultimate Final Files/TriMax Ultimate Vol {vol}/"
    subfolders = [
        f.path for f in os.scandir(path) if f.is_dir()
    ]  # me da las subcarpetas en el path
    names = [
        f.name for f in os.scandir(path) if f.is_dir()
    ]  # me da las subcarpetas en el path
    for folder in range(len(subfolders)):
        pdf_path = subfolders[folder] + f"/../{names[folder]}.pdf"
        files = glob.glob(os.path.expanduser(path + f"{names[folder]}/*.png"))
        files.sort(key=natural_sort_key)  # los ordeno por nombre

        final = [Image.open(f) for f in files]
        for i in range(len(final)):
            final[
                i
            ].load()  # load es necesario porque a veces flashea y no abre bien los archivos
            if final[i].mode == "RGBA":
                final[i] = final[i].convert("RGB")

        final[0].save(
            pdf_path, "PDF", resolution=100.0, save_all=True, append_images=final[1:]
        )

    """
    hasta acá, me convirtió cada cap en un pdf
    ahora quiero que me los combine PERO también quiero que agregue antes que nada
    la cover page entonces debería hacer un pdf con cover, alt cover y content idealmente
    """
    cover_path = (
        path + f"/a_cover.pdf"
    )  # le puse a adelante para que aparezca primero por default
    cover = glob.glob(os.path.expanduser(path + f"/*Cover*.png"))
    contents = glob.glob(os.path.expanduser(path + f"/*Contents*.png"))
    files = cover + contents

    final = [Image.open(f) for f in files]
    for i in range(len(final)):
        final[
            i
        ].load()  # load es necesario porque a veces flashea y no abre bien los archivos
        if final[i].mode == "RGBA":
            final[i] = final[i].convert("RGB")

    final[0].save(
        cover_path, "PDF", resolution=100.0, save_all=True, append_images=final[1:]
    )

    """
    Ahora sí, que tengo el pdf con la cover, quiero combinar todo en un solo pdf
    """

    pdfs = glob.glob(os.path.expanduser(path + "*.pdf"))

    merger = PdfMerger()

    for pdf in pdfs:
        merger.append(pdf)

    # merger.write(path + f"../Trigun Ultimate Vol {vol}.pdf")
    merger.write(path + f"../TriMax Ultimate Vol {vol}.pdf")
    merger.close()
