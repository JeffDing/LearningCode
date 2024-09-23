#安装cann
wget https://ascend-repo.obs.cn-east-2.myhuaweicloud.com/CANN/6.0.0.alpha001/Ascend-cann-toolkit_6.0.0.alpha001_linux-aarch64.run
chmod a+x Ascend-cann-toolkit_6.0.0.alpha001_linux-aarch64.run
./Ascend-cann-toolkit_6.0.0.alpha001_linux-aarch64.run --full

export PATH=/usr/local/Ascend/ascend-toolkit/latest/bin:/usr/local/Ascend/ascend-toolkit/latest/compiler/ccec_compiler/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/Ascend/ascend-toolkit/latest/lib64:/usr/local/Ascend/ascend-toolkit/latest/lib64/plugin/opskernel:/usr/local/Ascend/ascend-toolkit/latest/lib64/plugin/nnengine:$LD_LIBRARY_PATH
export PYTHONPATH=/usr/local/Ascend/ascend-toolkit/latest/python/site-packages:/usr/local/Ascend/ascend-toolkit/latest/opp/op_impl/built-in/ai_core/tbe:$PYTHONPATH
export ASCEND_AICPU_PATH=/usr/local/Ascend/ascend-toolkit/latest
export ASCEND_OPP_PATH=/usr/local/Ascend/ascend-toolkit/latest/opp
export TOOLCHAIN_HOME=/usr/local/Ascend/ascend-toolkit/latest/toolkit
export ASCEND_HOME_PATH=/usr/local/Ascend/ascend-toolkit/latest

# 安装cmake
wget https://github.com/Kitware/CMake/releases/download/v3.24.3/cmake-3.24.3.tar.gz
tar -xvf cmake-3.24.3.tar.gz
cd cmake
./configure
make
sudo make install

#安装miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh
bash Miniconda3-latest-Linux-aarch64.sh
export PATH=$HOME/miniconda3/bin:$PATH

#创建虚拟环境
conda create --name mmlab python=3.8 -y
conda activate mmlab

#安装Pytroch
pip install torch==1.8.1 torchvision==0.9.1 --extra-index-url https://download.pytorch.org/whl/cpu

#安装MMCV
pip install openmim
pip install mmcv-full

#模型推理依赖环境
apt-get update
apt-get install libopencv-dev

# mmdeploy依赖安装
git clone --recursive https://github.com/open-mmlab/mmdeploy.git
cd mmdeploy

# 安装mmdeploy模型转换器
pip install -v -te .

#编译 mmdeploy 推理SDK

#设置 ascend-toolkit环境变量
source /usr/local/Ascend/ascend-toolkit/set_env.sh

mkdir -p build && cd build
cmake .. -DMMDEPLOY_BUILD_SDK=ON -DMMDEPLOY_BUILD_SDK_PYTHON_API=ON \ -DMMDEPLOY_TARGET_BACKENDS=acl

make -j$(nproc) && make install
cd ..

#验证
#检查mmdeploy模型转换器是否安装成功
python tools/check_env.py
#检查mmdeploy推理SDK是否编译安装成功
export PYTHONPATH=$(pwd)/build/lib:$PYTHONPATH
python -c "import mmdeploy_python"


cp /usr/local/python3.7.5/lib/python3.7/py_compile.py  /usr/lib/python3.7
