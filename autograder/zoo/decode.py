from PIL import Image
from glob import glob
from pyzbar.pyzbar import decode
import cv2

def qrdecode(fname):
    image = cv2.imread(fname, 0)
    try: 
        data = decode(image) 
    except TypeError:  
        data = None
    return data

for filename in glob("*"): 
    data = qrdecode(filename)
    if data:
        print(f"{filename:<30}", data[0].data.decode("utf-8"))
    else:
        print(f"{filename:<30}")

