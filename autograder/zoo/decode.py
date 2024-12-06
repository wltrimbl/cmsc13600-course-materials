from PIL import Image
from glob import glob
import cv2
import platform

if platform.system() == "Darwin": 
# QR detector from opencv, not as capable 
# https://stackoverflow.com/questions/72542475/opencv-qrdetector-read-nothing-but-detect-the-qr
    def qrdecode(fname):
        image = cv2.imread(filename)
        try: 
            detector = cv2.QRCodeDetector()
            data, vertices_array, binary_qrcode = detector.detectAndDecode(image)
        except:
            vertices_array=None
        if vertices_array is not None:
            return data
        else:
            return None
else: 
    from pyzbar.pyzbar import decode
    def qrdecode(fname):
        image = cv2.imread(fname, 0)
        try: 
            data = decode(image) 
        except TypeError:  
            data = None
        if data:
            return data[0].data.decode("utf-8")


for filename in glob("*"): 
    data = qrdecode(filename)
    if data:
        print(f"{filename:<30}", data)
    else:
        print(f"{filename:<30}")

