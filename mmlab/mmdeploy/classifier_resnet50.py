import cv2
from mmdeploy_python import Classifier

# create a classifer
classifier = Classifier(model_path="mmdeploy_models/mmcls/resnet50/cann",device_name='cpu',device_id=0)

#read an image
img = cv2.imread("tests/data/tiger.jpeg")

#person inference
result = classifier(img)

#show result
for label_id, score in result:
	print(label_id,score)
