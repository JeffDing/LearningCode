pip install mmcls
pip install decorator sympy
mim download mmcls --config resnet50_8xb32_in1k --dest .
python tools/deploy.py configs/mmcls/classification_ascend_static-224x224.py resnet50_8xb32_in1k.py resnet50_8xb32_in1k_20210831-ea4938fc.pth tests/data/tiger.jpeg --work-dir mmdeploy_models/mmcls/resnet50/cann --device cpu --dump-info
