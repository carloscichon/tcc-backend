import numpy as np
import cv2

def process_image(img_string):
    nparr = np.fromstring(img_string, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.imwrite('teste_cv2.png',img_np)
    