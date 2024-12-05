# https://stackoverflow.com/questions/27233351/how-to-decode-a-qr-code-image-in-preferably-pure-python

import pyqrcode
qr = pyqrcode.create("test1")
qr.png("test1.png", scale=6)

For QR code decoding:

from PIL import Image
from pyzbar.pyzbar import decode
data = decode(Image.open('test1.png'))
print(data)

Works ok

import cv2
# Name of the QR Code Image file
filename = "attandence_Record_QR_code.png"
# read the QRCODE image
image = cv2.imread(filename)
# initialize the cv2 QRCode detector
detector = cv2.QRCodeDetector()
# detect and decode
data, vertices_array, binary_qrcode = detector.detectAndDecode(image)
# if there is a QR code
# print the data
if vertices_array is not None:
  print("QRCode data:")
  print(data)
else:
  print("There was some error") 


