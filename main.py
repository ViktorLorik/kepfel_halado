import tkinter as tk
from tkinter.filedialog import askopenfilename
import cv2
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import sys

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

root = tk.Tk()
root.withdraw()

absolutPathToImg = askopenfilename()

try:
    data = pytesseract.image_to_data(Image.open(absolutPathToImg))
    image = cv2.cv.LoadImage(absolutPathToImg)
except Exception:
    sys.exit("Invalid image")

lines = data.split('\n')
for i in range(1, len(lines)):
    cols = lines[i].split('\t')

    confidence = int(cols[10])
    if confidence <= 0:
        continue

    left = int(cols[6])
    top = int(cols[7])
    width = int(cols[8])
    height = int(cols[9])

    print(cols)

    # Draw rectangles to original image
    cv2.rectangle(image, (left, top), (left + width, top + height), (100, 100, 100), 1)
    cv2.putText(image, cols[10] + "%", (left, top - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0))
    cv2.putText(image, "\"" + cols[11] + "\"", (left, top + height + 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0))

cv2.imshow("Image with detected text", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
