import numpy as np
import cv2 as cv

imgs = np.load("sample_original_images.npy")
img = imgs[43]
if len(img.shape) == 3:
	img = img.transpose((1,2,0))
img = cv.resize(img, (64,64))
print(img.shape)
cv.imshow("img", img)
cv.waitKey(5000)
cv.imwrite("result.png", np.array(img*255, dtype=np.uint8))