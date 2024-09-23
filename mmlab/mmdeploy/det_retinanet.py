import cv2
from mmdeploy_python import Detector

#create a detector
detector = Detector(
	model_path = 'mmdeploy_models/mmdet/',
	device_name='cpu',
	device_id=0)

#read an image
img = cv2.imread('demo/resources/det.jpg')
#perform inference
bboxes, labels, _ = detector(img)

#visualize result
for index, (bbox, label_id_ in enumerate(zip(bboxes,labels)):
	[left, top, right, bottom],score - bbox[0:4].astype(int),bbox[4]
	if score < 0.3:
		continue
	cv2.rectangle(img, (left,top),(right,bottom),(0,255,0))

cv2.imwrite('output_detection.png',img)
