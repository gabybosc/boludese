from PIL import Image
import os as os
import fnmatch
import glob

# for n in range(33, 34):#range(32, 46):
    # path = f"../Haikyuu!!/Haikyuu!!/Vol{n}/"
    # pdf_path = f"../Haikyuu!!/Vol{n}.pdf"
path = "../hq/"
pdf_path = "../hq/vol_231.pdf"
"""
antes mejor si corro esto en la terminal para borrar toda la basura que le meten

PERO PARADA EN LA CARPETA CORRECTA

find . -name "*.jpg" -type f -size -110k -delete

-110k significa que borra lo que sea menor a 110 kbytes
"""

images = []
files = glob.glob(os.path.expanduser(path+"*.png"))
sorted_by_mtime_ascending = sorted(files, key=lambda t: os.stat(t).st_mtime)  # si se bajaron en orden, con esto las selecciona en orden

for file in sorted_by_mtime_ascending:#os.listdir(path):
    # for i in range(240):
    if fnmatch.fnmatch(file, "*.png"):#f"{str(i).zfill(4)}*.png"):
        images.append(file)

# images.sort()
# sorted(path + images, key=lambda t: -os.stat(t).st_mtime)
final = [Image.open(path+f) for f in images]

for i in range(len(final)):
    final[i].load()  # load es necesario porque a veces flashea y no abre bien los archivos

final[0].save(
    pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=final[1:]
)
