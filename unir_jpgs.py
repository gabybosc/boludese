from PIL import Image
import os as os
import fnmatch

for n in range(33, 34):#range(32, 46):
    path = f"../Haikyuu!!/Haikyuu!!/Vol{n}/"
    pdf_path = f"../Haikyuu!!/Vol{n}.pdf"

    """
    antes mejor si corro esto en la terminal para borrar toda la basura que le meten

    PERO PARADA EN LA CARPETA CORRECTA

    find . -name "*.jpg" -type f -size -110k -delete

    -110k significa que borra lo que sea menor a 110 kbytes
    """

    images = []
    for file in os.listdir(path):
        for i in range(240):
            if fnmatch.fnmatch(file, f"{str(i).zfill(4)}*.jpg"):
                images.append(file)

    images.sort()
    final = [Image.open(path+f) for f in images]

    for i in range(len(final)):
        final[i].load()  # load es necesario porque a veces flashea y no abre bien los archivos

    final[0].save(
        pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=final[1:]
    )
