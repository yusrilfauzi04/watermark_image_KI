import cv2
from imwatermark import WatermarkEncoder, WatermarkDecoder

bgr = cv2.imread("./uploads/Alchemy.Stars.full.3366422.jpg")
wm = "rizky mocahamad"

encoder = WatermarkEncoder()
encoder.set_watermark("bytes", wm.encode("utf-8"))
bgr_encoded = encoder.encode(bgr, "dwtDct")

cv2.imwrite("test_wm.png", bgr_encoded)

newBgr = cv2.imread("test_wm.png")

decoder = WatermarkDecoder("bytes", len(wm) * 8)
watermark = decoder.decode(newBgr, "dwtDct")
print(watermark.decode("utf-8"))
