pip install mmdet
pip install decorator sympy
mim download mmdet --config retinanet_r50_fpn_1x_coco --dest .
python tools/deploy.py configs/mmdet/detection/detection_ascend_static-800x1344.py retinanet_r50_fpn_1x_coco.py retinanet_r50_fpn_1x_coco_20200130-c2398f9e.pth demo/resources/det.jpg --work-dir mmdeploy_models/mmdet/retinanet/cann --device cpu --dump-info
