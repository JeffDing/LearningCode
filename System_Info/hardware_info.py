#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
设备硬件信息查询工具
支持查询：系统信息、外网IP及地理位置、NPU/GPU、内存、硬盘、网卡等信息
"""

import platform
import subprocess
import re
import json
import socket
import os
import requests
from typing import Dict, List, Optional, Any
import psutil
import sys

class HardwareInfoCollector:
    """硬件信息收集器"""

    def __init__(self):
        self.system_info = {}
        self.ip_info = {}
        self.cpu_info = {}
        self.gpu_info = []
        self.npu_info = []
        self.memory_info = {}
        self.disk_info = []
        self.network_info = []

    def get_system_info(self) -> Dict[str, str]:
        """获取系统基本信息，包括厂商和型号"""
        print("正在获取系统基本信息...")

        system = platform.system()
        machine = platform.machine()
        processor = platform.processor()
        node = platform.node()

        info = {
            "操作系统": system,
            "主机名": node,
            "处理器架构": machine,
            "处理器": processor,
            "Python版本": platform.python_version()
        }

        # 尝试获取更详细的系统信息
        try:
            if system == "Linux":
                # 读取DMI信息
                dmi_files = {
                    "制造商": "/sys/class/dmi/id/sys_vendor",
                    "产品型号": "/sys/class/dmi/id/product_name",
                    "产品序列号": "/sys/class/dmi/id/product_serial",
                    "BIOS版本": "/sys/class/dmi/id/bios_version",
                    "BIOS日期": "/sys/class/dmi/id/bios_date"
                }

                for key, filepath in dmi_files.items():
                    if os.path.exists(filepath):
                        with open(filepath, 'r') as f:
                            value = f.read().strip()
                            if value:
                                info[key] = value

                # 尝试使用dmidecode命令（需要root权限）
                try:
                    result = subprocess.run(['dmidecode', '-t', 'system'], capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        output = result.stdout
                        if 'Manufacturer:' in output:
                            match = re.search(r'Manufacturer:\s*(.+)', output)
                            if match:
                                info["系统制造商"] = match.group(1).strip()
                        if 'Product Name:' in output:
                            match = re.search(r'Product Name:\s*(.+)', output)
                            if match:
                                info["产品名称"] = match.group(1).strip()
                except (subprocess.TimeoutExpired, FileNotFoundError, PermissionError):
                    pass

            elif system == "Windows":
                try:
                    # 使用wmic获取Windows系统信息
                    result = subprocess.run(
                        ['wmic', 'csproduct', 'get', 'Vendor,Name,Version'],
                        capture_output=True, text=True, timeout=10
                    )
                    if result.returncode == 0:
                        lines = result.stdout.strip().split('\n')
                        if len(lines) > 1:
                            parts = lines[1].strip().split()
                            if len(parts) >= 2:
                                info["制造商"] = parts[0]
                                info["产品型号"] = parts[1]

                    result = subprocess.run(
                        ['wmic', 'bios', 'get', 'SerialNumber,Version'],
                        capture_output=True, text=True, timeout=10
                    )
                    if result.returncode == 0:
                        lines = result.stdout.strip().split('\n')
                        if len(lines) > 1:
                            serial = lines[1].strip()
                            if serial:
                                info["序列号"] = serial
                except (subprocess.TimeoutExpired, FileNotFoundError, PermissionError):
                    pass

            elif system == "Darwin":  # macOS
                try:
                    result = subprocess.run(['system_profiler', 'SPHardwareDataType'], capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        output = result.stdout
                        if 'Model Name:' in output:
                            match = re.search(r'Model Name:\s*(.+)', output)
                            if match:
                                info["产品型号"] = match.group(1).strip()
                        if 'Manufacturer:' in output:
                            match = re.search(r'Manufacturer:\s*(.+)', output)
                            if match:
                                info["制造商"] = match.group(1).strip()
                        if 'Serial Number:' in output:
                            match = re.search(r'Serial Number:\s*(.+)', output)
                            if match:
                                info["序列号"] = match.group(1).strip()
                except (subprocess.TimeoutExpired, FileNotFoundError, PermissionError):
                    pass

        except Exception as e:
            print(f"获取系统详细信息时出错: {e}")

        self.system_info = info
        return info

    def get_cpu_info(self) -> Dict[str, str]:
        """获取CPU详细信息，包括厂商和型号"""
        print("正在获取CPU信息...")

        info = {
            "厂商": "未知",
            "型号": "未知",
            "架构": platform.machine(),
            "核心数": str(psutil.cpu_count(logical=False)),
            "逻辑核心数": str(psutil.cpu_count(logical=True)),
            "频率": "未知"
        }

        try:
            if platform.system() == "Linux":
                # 方法1: 读取/proc/cpuinfo
                try:
                    with open('/proc/cpuinfo', 'r') as f:
                        cpuinfo = f.read()

                    # 提取model name
                    model_match = re.search(r'model name\s*:\s*(.+)', cpuinfo)
                    if model_match:
                        model = model_match.group(1).strip()
                        info["型号"] = model

                        # 从型号中提取厂商
                        model_upper = model.upper()
                        if "INTEL" in model_upper or "INTEL(R)" in model_upper:
                            info["厂商"] = "Intel"
                        elif "AMD" in model_upper or "ADVANCED MICRO DEVICES" in model_upper:
                            info["厂商"] = "AMD"
                        elif "ARM" in model_upper:
                            info["厂商"] = "ARM"
                        elif "QUALCOMM" in model_upper:
                            info["厂商"] = "Qualcomm"
                        elif "HUAWEI" in model_upper or "KUNPENG" in model_upper:
                            info["厂商"] = "Huawei"
                        elif "PHYTEC" in model_upper:
                            info["厂商"] = "Phytec"

                    # 提取CPU频率
                    freq_match = re.search(r'cpu MHz\s*:\s*([\d.]+)', cpuinfo)
                    if freq_match:
                        freq_mhz = float(freq_match.group(1))
                        if freq_mhz >= 1000:
                            info["频率"] = f"{freq_mhz/1000:.2f} GHz"
                        else:
                            info["频率"] = f"{freq_mhz:.0f} MHz"

                    # 提取缓存信息
                    l1d_match = re.search(r'L1d cache\s*:\s*(.+)', cpuinfo)
                    l1i_match = re.search(r'L1i cache\s*:\s*(.+)', cpuinfo)
                    l2_match = re.search(r'L2 cache\s*:\s*(.+)', cpuinfo)
                    l3_match = re.search(r'L3 cache\s*:\s*(.+)', cpuinfo)

                    if l1d_match:
                        info["L1数据缓存"] = l1d_match.group(1).strip()
                    if l1i_match:
                        info["L1指令缓存"] = l1i_match.group(1).strip()
                    if l2_match:
                        info["L2缓存"] = l2_match.group(1).strip()
                    if l3_match:
                        info["L3缓存"] = l3_match.group(1).strip()

                except FileNotFoundError:
                    pass

                # 方法2: 使用lscpu命令
                try:
                    result = subprocess.run(['lscpu'], capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        output = result.stdout

                        # 提取厂商信息
                        vendor_match = re.search(r'Vendor ID:\s*(.+)', output)
                        if vendor_match:
                            vendor_id = vendor_match.group(1).strip()
                            if vendor_id == "GenuineIntel":
                                info["厂商"] = "Intel"
                            elif vendor_id == "AuthenticAMD":
                                info["厂商"] = "AMD"
                            elif vendor_id == "ARM":
                                info["厂商"] = "ARM"

                        # 提取型号
                        model_match = re.search(r'Model name:\s*(.+)', output)
                        if model_match:
                            info["型号"] = model_match.group(1).strip()

                        # 提取频率
                        max_freq_match = re.search(r'CPU max MHz:\s*([\d.]+)', output)
                        if max_freq_match:
                            max_freq = float(max_freq_match.group(1))
                            info["最大频率"] = f"{max_freq/1000:.2f} GHz"

                        min_freq_match = re.search(r'CPU min MHz:\s*([\d.]+)', output)
                        if min_freq_match:
                            min_freq = float(min_freq_match.group(1))
                            info["最小频率"] = f"{min_freq/1000:.2f} GHz"

                except (subprocess.TimeoutExpired, FileNotFoundError):
                    pass

                # 方法3: 使用dmidecode获取CPU详细信息（需要root权限）
                try:
                    result = subprocess.run(['dmidecode', '-t', 'processor'], capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        output = result.stdout

                        # 提取Socket设计
                        socket_match = re.search(r'Socket Designation:\s*(.+)', output)
                        if socket_match:
                            info["插槽"] = socket_match.group(1).strip()

                        # 提取制造商
                        manufacturer_match = re.search(r'Manufacturer:\s*(.+)', output)
                        if manufacturer_match:
                            info["制造商"] = manufacturer_match.group(1).strip()
                            # 如果厂商还是未知，使用dmidecode的结果
                            if info["厂商"] == "未知":
                                manufacturer = manufacturer_match.group(1).strip().upper()
                                if "INTEL" in manufacturer:
                                    info["厂商"] = "Intel"
                                elif "AMD" in manufacturer:
                                    info["厂商"] = "AMD"

                        # 提取版本
                        version_match = re.search(r'Version:\s*(.+)', output)
                        if version_match:
                            version = version_match.group(1).strip()
                            if info["型号"] == "未知" or len(version) > len(info["型号"]):
                                info["型号"] = version

                        # 提取当前速度
                        speed_match = re.search(r'Current Speed:\s*(.+)', output)
                        if speed_match:
                            info["当前速度"] = speed_match.group(1).strip()

                        # 提取最大速度
                        max_speed_match = re.search(r'Max Speed:\s*(.+)', output)
                        if max_speed_match:
                            info["最大速度"] = max_speed_match.group(1).strip()

                        # 提取电压
                        voltage_match = re.search(r'Voltage:\s*(.+)', output)
                        if voltage_match:
                            info["电压"] = voltage_match.group(1).strip()

                        # 提取序列号
                        serial_match = re.search(r'Serial Number:\s*(.+)', output)
                        if serial_match:
                            info["序列号"] = serial_match.group(1).strip()

                except (subprocess.TimeoutExpired, FileNotFoundError, PermissionError):
                    pass

            elif platform.system() == "Windows":
                # Windows系统使用wmic获取CPU信息
                try:
                    result = subprocess.run(
                        ['wmic', 'cpu', 'get', 'Manufacturer,Name,NumberOfCores,NumberOfLogicalProcessors,MaxClockSpeed'],
                        capture_output=True, text=True, timeout=10
                    )
                    if result.returncode == 0:
                        lines = result.stdout.strip().split('\n')
                        if len(lines) > 1:
                            parts = [p.strip() for p in lines[1].split(maxsplit=4)]

                            if parts:
                                info["厂商"] = parts[0]

                                if len(parts) > 1:
                                    info["型号"] = parts[1]

                                if len(parts) > 2 and parts[2]:
                                    info["核心数"] = parts[2]

                                if len(parts) > 3 and parts[3]:
                                    info["逻辑核心数"] = parts[3]

                                if len(parts) > 4 and parts[4]:
                                    # 转换MHz到GHz
                                    try:
                                        mhz = float(parts[4])
                                        info["最大频率"] = f"{mhz/1000:.2f} GHz"
                                    except ValueError:
                                        pass

                except (subprocess.TimeoutExpired, FileNotFoundError):
                    pass

            elif platform.system() == "Darwin":  # macOS
                try:
                    result = subprocess.run(['sysctl', '-n', 'machdep.cpu.brand_string'],
                                          capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        model = result.stdout.strip()
                        info["型号"] = model

                        # 从型号中提取厂商
                        model_upper = model.upper()
                        if "INTEL" in model_upper:
                            info["厂商"] = "Intel"
                        elif "APPLE" in model_upper:
                            info["厂商"] = "Apple"

                except (subprocess.TimeoutExpired, FileNotFoundError):
                    pass

                # 获取CPU频率
                try:
                    result = subprocess.run(['sysctl', '-n', 'hw.cpufrequency'],
                                          capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        freq_hz = int(result.stdout.strip())
                        info["频率"] = f"{freq_hz/1000000000:.2f} GHz"
                except (subprocess.TimeoutExpired, FileNotFoundError, ValueError):
                    pass

            # 使用psutil获取CPU频率（通用方法）
            try:
                cpu_freq = psutil.cpu_freq()
                if cpu_freq:
                    if cpu_freq.max:
                        info["最大频率"] = f"{cpu_freq.max/1000:.2f} GHz"
                    if cpu_freq.min:
                        info["最小频率"] = f"{cpu_freq.min/1000:.2f} GHz"
                    if cpu_freq.current:
                        info["当前频率"] = f"{cpu_freq.current/1000:.2f} GHz"
            except:
                pass

            # 获取CPU使用率
            try:
                cpu_percent = psutil.cpu_percent(interval=1)
                info["CPU使用率"] = f"{cpu_percent}%"
            except:
                pass

        except Exception as e:
            print(f"获取CPU信息时出错: {e}")

        self.cpu_info = info
        return info

    def get_external_ip_info(self) -> Dict[str, Any]:
        """获取外网IP地址及地理位置信息"""
        print("正在获取外网IP信息...")

        info = {
            "外网IP": "未知",
            "地理位置": "未知",
            "ISP": "未知",
            "详细地址": "未知"
        }

        try:
            # 尝试多个IP查询API
            apis = [
                "http://ip-api.com/json/",
                "http://ipinfo.io/json",
                "https://api.ipify.org?format=json",
                "http://checkip.amazonaws.com"
            ]

            for api in apis:
                try:
                    response = requests.get(api, timeout=5)
                    if response.status_code == 200:
                        data = response.json()

                        # 解析不同API的响应格式
                        if "query" in data:  # ip-api.com
                            info["外网IP"] = data.get("query", "未知")
                            info["国家"] = data.get("country", "未知")
                            info["地区"] = data.get("regionName", "未知")
                            info["城市"] = data.get("city", "未知")
                            info["ISP"] = data.get("isp", "未知")
                            info["详细地址"] = f"{data.get('country', '')} {data.get('regionName', '')} {data.get('city', '')}".strip()
                            break
                        elif "ip" in data:  # ipinfo.io
                            info["外网IP"] = data.get("ip", "未知")
                            info["地理位置"] = data.get("loc", "未知")
                            info["ISP"] = data.get("org", "未知")
                            info["详细地址"] = data.get("city", "未知") + ", " + data.get("region", "未知") + ", " + data.get("country", "未知")
                            break
                        elif "ip" in data and len(data) == 1:  # api.ipify.org
                            info["外网IP"] = data.get("ip", "未知")
                            # 继续尝试其他API获取地理位置
                            continue

                except requests.exceptions.RequestException:
                    continue
                except json.JSONDecodeError:
                    continue

        except Exception as e:
            print(f"获取外网IP信息时出错: {e}")
            # 降级方案：获取本机IP
            try:
                hostname = socket.gethostname()
                local_ip = socket.gethostbyname(hostname)
                info["外网IP"] = f"{local_ip} (内网IP)"
            except:
                pass

        self.ip_info = info
        return info

    def get_gpu_info(self) -> List[Dict[str, str]]:
        """获取GPU信息，包括国产GPGPU"""
        print("正在获取GPU信息...")

        gpus = []
        seen_models = set()  # 用于去重

        # ============ 国产GPGPU检测 ============
        # 注意：华为昇腾是NPU设备，不在GPGPU中显示，请在NPU信息中查看

        # 方法1: 摩尔线程 (Moore Threads) - 使用musa-smi
        try:
            result = subprocess.run(['musa-smi'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                output = result.stdout

                # 解析摩尔线程GPU信息
                # 匹配类似 "MTT S80" 的型号
                model_pattern = re.compile(r'MTT\s+\S+', re.IGNORECASE)
                models = model_pattern.findall(output)

                for model in models:
                    model_key = f"摩尔线程-{model}"
                    if model_key not in seen_models:
                        gpu = {
                            "厂商": "摩尔线程",
                            "型号": model,
                            "类型": "GPGPU"
                        }
                        gpus.append(gpu)
                        seen_models.add(model_key)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        # 方法2: 壁仞科技 - 使用brsmi
        try:
            result = subprocess.run(['brsmi'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                output = result.stdout

                # 解析壁仞GPU信息
                # 匹配类似 "BR100" 等型号
                model_pattern = re.compile(r'BR\d+', re.IGNORECASE)
                models = model_pattern.findall(output)

                for model in models:
                    model_key = f"壁仞科技-{model}"
                    if model_key not in seen_models:
                        gpu = {
                            "厂商": "壁仞科技",
                            "型号": model,
                            "类型": "GPGPU"
                        }
                        gpus.append(gpu)
                        seen_models.add(model_key)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        # 方法3: 沐曦 - 使用mx-smi
        try:
            result = subprocess.run(['mx-smi'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                output = result.stdout

                # 解析沐曦GPU信息
                # 匹配类似 "MXC500 VF"、"C500"、"N280" 等型号
                # 要求至少2位数字，避免匹配到 python3.10 中的 n3
                model_pattern = re.compile(r'\b(?:MXC|C|N)\d{2,}\b\s*(?:VF)?', re.IGNORECASE)
                models = [m.strip() for m in model_pattern.findall(output)]

                for model in models:
                    model_key = f"沐曦-{model}"
                    if model_key not in seen_models:
                        gpu = {
                            "厂商": "沐曦",
                            "型号": model,
                            "类型": "GPGPU"
                        }
                        gpus.append(gpu)
                        seen_models.add(model_key)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        # 方法4: 天数智芯 - 使用ixsmi
        try:
            result = subprocess.run(['ixsmi'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                output = result.stdout

                # 解析天数智芯GPU信息
                # 匹配类似 "Iluvatar BI-V100" 等型号
                model_pattern = re.compile(r'Iluvatar\s+BI-V\d+', re.IGNORECASE)
                models = model_pattern.findall(output)

                for model in models:
                    model_key = f"天数智芯-{model}"
                    if model_key not in seen_models:
                        gpu = {
                            "厂商": "天数智芯",
                            "型号": model,
                            "类型": "GPGPU"
                        }
                        gpus.append(gpu)
                        seen_models.add(model_key)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        # 方法5: 海光 - 使用dcgmi
        try:
            result = subprocess.run(['dcgmi', 'diag', '-r'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                output = result.stdout

                # 解析海光GPU信息
                if "海光" in output or "Hygon" in output:
                    model_key = "海光-GPGPU"
                    if model_key not in seen_models:
                        gpu = {
                            "厂商": "海光",
                            "型号": "海光GPGPU",
                            "类型": "GPGPU"
                        }
                        gpus.append(gpu)
                        seen_models.add(model_key)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        # 方法6: 使用lspci检测国产GPU (Linux)
        try:
            result = subprocess.run(['lspci', '-nn', '-d', '::0300'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    vendor = "未知"
                    model = "未知"

                    line_upper = line.upper()

                    # 检测国产GPU厂商
                    if "MOORE THREADS" in line_upper or "摩尔线程" in line:
                        vendor = "摩尔线程"
                        model_match = re.search(r'MTT\s+\S+', line, re.IGNORECASE)
                        if model_match:
                            model = model_match.group(0)
                        else:
                            model = "摩尔线程GPU"

                    elif "BR" in line_upper and "BIRENTECH" not in line_upper:
                        vendor = "壁仞科技"
                        model_match = re.search(r'BR\d+', line, re.IGNORECASE)
                        if model_match:
                            model = model_match.group(0)
                        else:
                            model = "壁仞科技GPU"

                    elif "ILUVATAR" in line_upper or "天数" in line:
                        vendor = "天数智芯"
                        # 天数智芯型号通常是 Iluvatar BI-Vxxx 格式
                        model_match = re.search(r'Iluvatar\s+BI-V\d+', line, re.IGNORECASE)
                        if not model_match:
                            model_match = re.search(r'BI-V\d+', line, re.IGNORECASE)
                        if model_match:
                            model = model_match.group(0)
                        else:
                            model = "天数智芯GPU"

                    elif "MAXXIR" in line_upper or "沐曦" in line:
                        vendor = "沐曦"
                        # 沐曦型号通常是 MXC500 VF、C500、N280 等格式
                        # 要求至少2位数字，避免匹配到错误文本
                        model_match = re.search(r'\b(?:MXC|C|N)\d{2,}\b\s*(?:VF)?', line, re.IGNORECASE)
                        if model_match:
                            model = model_match.group(0)
                        else:
                            model = "沐曦GPU"

                    elif "HYGON" in line_upper or "海光" in line:
                        vendor = "海光"
                        model = "海光GPU"

                    # 注意：华为昇腾是NPU设备，不在GPGPU中显示，请在NPU信息中查看

                    # 如果检测到国产GPU，添加到列表
                    if vendor != "未知":
                        gpu_id = line.split()[0] if line.split() else "未知"

                        # 尝试获取详细信息
                        try:
                            detail_result = subprocess.run(['lspci', '-v', '-s', gpu_id], capture_output=True, text=True, timeout=5)
                            detail_output = detail_result.stdout

                            # 尝试获取显存信息
                            vram = "未知"
                            vram_match = re.search(r'prefetchable.*size=\[(\d+[KMGT])\]', detail_output)
                            if vram_match:
                                vram = vram_match.group(1)

                            gpu_info = {
                                "厂商": vendor,
                                "型号": model,
                                "显存": vram,
                                "设备ID": gpu_id,
                                "类型": "GPGPU"
                            }

                            model_key = f"{vendor}-{model}-{gpu_id}"
                            if model_key not in seen_models:
                                gpus.append(gpu_info)
                                seen_models.add(model_key)

                        except subprocess.TimeoutExpired:
                            pass

        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        # ============ 国际主流GPU检测 ============

        # 方法7: 使用nvidia-smi (NVIDIA GPU)
        try:
            result = subprocess.run(['nvidia-smi', '--query-gpu=name,driver_version,memory.total', '--format=csv,noheader'],
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    parts = [p.strip() for p in line.split(',')]
                    if len(parts) >= 1:
                        model_key = f"NVIDIA-{parts[0]}"
                        if model_key not in seen_models:
                            gpu = {
                                "厂商": "NVIDIA",
                                "型号": parts[0],
                                "驱动版本": parts[1] if len(parts) > 1 else "未知",
                                "显存": parts[2] if len(parts) > 2 else "未知",
                                "类型": "GPU"
                            }
                            gpus.append(gpu)
                            seen_models.add(model_key)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        # 方法8: 使用rocm-smi (AMD GPU)
        try:
            result = subprocess.run(['rocm-smi', '--showproductname'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if 'Card series' in line or 'GPU' in line:
                        model = line.split(':')[-1].strip()
                        model_key = f"AMD-{model}"
                        if model_key not in seen_models:
                            gpu = {
                                "厂商": "AMD",
                                "型号": model,
                                "类型": "GPU"
                            }
                            gpus.append(gpu)
                            seen_models.add(model_key)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        # 方法9: 使用lspci检测国际GPU (Linux)
        try:
            result = subprocess.run(['lspci', '-nn', '-d', '::0300'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if 'VGA' in line or '3D' in line:
                        gpu_id = line.split()[0]
                        try:
                            detail_result = subprocess.run(['lspci', '-v', '-s', gpu_id], capture_output=True, text=True, timeout=5)
                            detail_output = detail_result.stdout

                            vendor = "未知"
                            model = line.split(':')[-1].strip() if ':' in line else "未知"

                            if "NVIDIA" in model.upper():
                                vendor = "NVIDIA"
                            elif "AMD" in model.upper() or "Advanced Micro Devices" in model:
                                vendor = "AMD"
                            elif "Intel" in model.upper():
                                vendor = "Intel"

                            # 只处理国际厂商，国产GPU已经在前面处理过
                            if vendor in ["NVIDIA", "AMD", "Intel"]:
                                # 尝试获取显存信息
                                vram = "未知"
                                vram_match = re.search(r'prefetchable.*size=\[(\d+[KMGT])\]', detail_output)
                                if vram_match:
                                    vram = vram_match.group(1)

                                gpu = {
                                    "厂商": vendor,
                                    "型号": model,
                                    "显存": vram,
                                    "设备ID": gpu_id,
                                    "类型": "GPU"
                                }

                                model_key = f"{vendor}-{model}-{gpu_id}"
                                if model_key not in seen_models:
                                    gpus.append(gpu)
                                    seen_models.add(model_key)

                        except subprocess.TimeoutExpired:
                            pass
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        # 方法10: Windows下的查询
        if platform.system() == "Windows":
            try:
                result = subprocess.run(
                    ['wmic', 'path', 'win32_VideoController', 'get', 'name,AdapterRAM,DriverVersion'],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    for line in lines[1:]:  # 跳过标题行
                        parts = line.strip().split()
                        if parts:
                            vendor = "未知"
                            model = parts[0]

                            if any(keyword in model.upper() for keyword in ["MOORE", "摩尔", "THREADS"]):
                                vendor = "摩尔线程"
                            elif any(keyword in model.upper() for keyword in ["BR", "BIREN", "壁仞"]):
                                vendor = "壁仞科技"
                            elif any(keyword in model.upper() for keyword in ["ILUVATAR", "天数"]):
                                vendor = "天数智芯"
                            elif any(keyword in model.upper() for keyword in ["MAXXIR", "沐曦"]):
                                vendor = "沐曦"
                            elif any(keyword in model.upper() for keyword in ["HYGON", "海光"]):
                                vendor = "海光"
                            # 注意：华为昇腾是NPU设备，不在GPGPU中显示，请在NPU信息中查看
                            elif "NVIDIA" in model.upper():
                                vendor = "NVIDIA"
                            elif "AMD" in model.upper():
                                vendor = "AMD"
                            elif "Intel" in model.upper():
                                vendor = "Intel"

                            gpu_type = "GPGPU" if vendor in ["摩尔线程", "壁仞科技", "天数智芯", "沐曦", "海光"] else "GPU"

                            gpu = {
                                "厂商": vendor,
                                "型号": model,
                                "类型": gpu_type
                            }

                            model_key = f"{vendor}-{model}"
                            if model_key not in seen_models:
                                gpus.append(gpu)
                                seen_models.add(model_key)
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass

        # 方法11: macOS下的查询
        if platform.system() == "Darwin":
            try:
                result = subprocess.run(['system_profiler', 'SPDisplaysDataType'], capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    output = result.stdout
                    matches = re.findall(r'Chipset Model:\s*(.+)', output)
                    for model in matches:
                        model = model.strip()
                        model_key = f"Apple-{model}"
                        if model_key not in seen_models:
                            gpu = {
                                "厂商": "Apple",
                                "型号": model,
                                "类型": "GPU"
                            }
                            gpus.append(gpu)
                            seen_models.add(model_key)
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass

        self.gpu_info = gpus
        return gpus

    def get_npu_info(self) -> List[Dict[str, str]]:
        """获取NPU信息"""
        print("正在获取NPU信息...")

        npus = []

        # 方法: 使用npu-smi info查询华为昇腾NPU
        try:
            result = subprocess.run(['npu-smi', 'info'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                output = result.stdout

                # 解析npu-smi info输出格式
                # 示例输出:
                # +------------------------------------------------------------------------------------------------+
                # | npu-smi 24.1.rc2.1               Version: 24.1.rc2.1                                           |
                # +---------------------------+---------------+----------------------------------------------------+
                # | NPU   Name                | Health        | Power(W)    Temp(C)           Hugepages-Usage(page)|
                # | Chip                      | Bus-Id        | AICore(%)   Memory-Usage(MB)  HBM-Usage(MB)        |
                # +===========================+===============+====================================================+
                # | 3     910B2               | OK            | 119.9       45                0    / 0             |
                # | 0                         | 0000:02:00.0  | 9           0    / 0          61125/ 65536         |
                # +===========================+===============+====================================================+
                # | 4     910B2               | OK            | 116.1       45                0    / 0             |
                # | 0                         | 0000:81:00.0  | 9           0    / 0          61120/ 65536         |
                # +===========================+===============+====================================================+
                # | 5     910B2               | OK            | 110.6       62                0    / 0             |
                # | 0                         | 0000:41:00.0  | 5           0    / 0          61122/ 65536         |
                # +===========================+===============+====================================================+
                # | 6     910B2               | OK            | 109.9       45                0    / 0             |
                # | 0                         | 0000:82:00.0  | 0           0    / 0          61123/ 65536         |
                # +===========================+===============+====================================================+
                # +---------------------------+---------------+----------------------------------------------------+
                # | NPU     Chip              | Process id    | Process name             | Process memory(MB)      |
                # +===========================+===============+====================================================+
                # | 3       0                 | 6290          | VLLMWorker_TP            | 57776                   |
                # +===========================+===============+====================================================+

                lines = output.split('\n')
                npu_data = {}
                current_npu_id = None

                for line in lines:
                    line = line.strip()
                    if not line or line.startswith('+') or line.startswith('| npu-smi'):
                        continue

                    # 匹配NPU信息行 (第一行数据)
                    # | 3     910B2               | OK            | 119.9       45                0    / 0             |
                    npu_match = re.match(r'\|\s*(\d+)\s+(\S+)\s+\|\s*(\w+)\s+\|\s*([\d.]+)\s+(\d+)\s+([\d/ ]+)\s*\|', line)
                    if npu_match:
                        current_npu_id = npu_match.group(1)
                        npu_data[current_npu_id] = {
                            "NPU ID": current_npu_id,
                            "型号": npu_match.group(2),
                            "健康状态": npu_match.group(3),
                            "功耗": f"{npu_match.group(4)} W",
                            "温度": f"{npu_match.group(5)} C",
                            "Hugepages使用": npu_match.group(6),
                            "厂商": "华为"
                        }
                        continue

                    # 匹配Chip信息行 (第二行数据)
                    # | 0                         | 0000:02:00.0  | 9           0    / 0          61125/ 65536         |
                    if current_npu_id and current_npu_id in npu_data:
                        chip_match = re.match(r'\|\s*(\d+)\s+\|\s*(\S+)\s+\|\s*(\d+)\s+([\d/ ]+)\s+([\d/ ]+)\s*\|', line)
                        if chip_match:
                            npu_data[current_npu_id].update({
                                "Chip ID": chip_match.group(1),
                                "Bus-Id": chip_match.group(2),
                                "AICore使用率": f"{chip_match.group(3)}%",
                                "Memory使用": chip_match.group(4),
                                "HBM使用": chip_match.group(5)
                            })
                            current_npu_id = None  # 重置，准备下一个NPU

                # 将解析的数据转换为列表
                for npu_id, data in npu_data.items():
                    npus.append(data)

                # 如果解析失败但检测到华为NPU，返回基本信息
                if not npus and ("Huawei" in output or "910" in output):
                    npus.append({
                        "厂商": "华为",
                        "型号": "昇腾NPU",
                        "备注": "详细信息请使用npu-smi info查看"
                    })

        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        # 备用方法: 查询特定设备文件 (华为昇腾)
        if not npus:
            try:
                if os.path.exists('/dev/davinci0') or os.path.exists('/dev/davinci_manager'):
                    npus.append({
                        "厂商": "华为",
                        "型号": "昇腾NPU (Davinci架构)",
                        "设备路径": "/dev/davinci*"
                    })
            except:
                pass

        self.npu_info = npus
        return npus

    def get_memory_info(self) -> Dict[str, Any]:
        """获取内存信息"""
        print("正在获取内存信息...")

        info = {}

        try:
            # 使用psutil获取内存信息
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()

            info = {
                "总内存": self._format_size(mem.total),
                "可用内存": self._format_size(mem.available),
                "已使用内存": self._format_size(mem.used),
                "内存使用率": f"{mem.percent}%",
                "总交换空间": self._format_size(swap.total),
                "已使用交换空间": self._format_size(swap.used),
                "交换空间使用率": f"{swap.percent if swap.total > 0 else 0}%"
            }

            # 尝试获取更详细的内存信息
            if platform.system() == "Linux":
                try:
                    # 使用dmidecode获取内存详细信息（需要root权限）
                    result = subprocess.run(['dmidecode', '-t', 'memory'], capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        output = result.stdout

                        # 提取内存条信息
                        slots = re.findall(r'Device Locator:\s*(.+)', output)
                        sizes = re.findall(r'Size:\s*(.+)', output)
                        speeds = re.findall(r'Speed:\s*(.+)', output)
                        manufacturers = re.findall(r'Manufacturer:\s*(.+)', output)
                        types = re.findall(r'Type:\s*(.+)', output)

                        memory_details = []
                        for i, (slot, size, speed, manufacturer, mem_type) in enumerate(zip(slots, sizes, speeds, manufacturers, types)):
                            if 'No Module Installed' not in size:
                                memory_details.append({
                                    "插槽": slot.strip(),
                                    "容量": size.strip(),
                                    "速度": speed.strip(),
                                    "制造商": manufacturer.strip(),
                                    "类型": mem_type.strip()
                                })

                        if memory_details:
                            info["内存详细信息"] = memory_details

                except (subprocess.TimeoutExpired, FileNotFoundError, PermissionError):
                    pass

            elif platform.system() == "Windows":
                try:
                    result = subprocess.run(['wmic', 'memorychip', 'get', 'Capacity,Speed,Manufacturer,PartNumber'],
                                          capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        lines = result.stdout.strip().split('\n')
                        memory_details = []
                        for line in lines[1:]:
                            parts = line.strip().split()
                            if parts:
                                memory_details.append({
                                    "容量": self._format_size(int(parts[0])) if parts[0].isdigit() else parts[0],
                                    "速度": parts[1] if len(parts) > 1 else "未知",
                                    "制造商": parts[2] if len(parts) > 2 else "未知"
                                })
                        if memory_details:
                            info["内存详细信息"] = memory_details
                except (subprocess.TimeoutExpired, FileNotFoundError):
                    pass

        except Exception as e:
            print(f"获取内存信息时出错: {e}")
            info = {"错误": str(e)}

        self.memory_info = info
        return info

    def get_disk_info(self) -> List[Dict[str, Any]]:
        """获取硬盘/存储信息"""
        print("正在获取硬盘信息...")

        disks = []

        try:
            # 获取所有磁盘分区
            partitions = psutil.disk_partitions()

            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disk = {
                        "设备": partition.device,
                        "挂载点": partition.mountpoint,
                        "文件系统类型": partition.fstype,
                        "总容量": self._format_size(usage.total),
                        "已使用": self._format_size(usage.used),
                        "可用空间": self._format_size(usage.free),
                        "使用率": f"{usage.percent}%"
                    }
                    disks.append(disk)
                except PermissionError:
                    # 某些挂载点可能没有权限访问
                    continue
                except Exception:
                    continue

            # 尝试获取磁盘物理信息
            if platform.system() == "Linux":
                try:
                    # 使用lsblk获取磁盘信息
                    result = subprocess.run(['lsblk', '-d', '-o', 'NAME,SIZE,MODEL,VENDOR,TYPE'],
                                          capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        lines = result.stdout.strip().split('\n')
                        for line in lines[1:]:
                            parts = line.split()
                            if parts and parts[-1] == 'disk':
                                disk_detail = {
                                    "设备名": parts[0],
                                    "容量": parts[1] if len(parts) > 1 else "未知",
                                    "型号": parts[2] if len(parts) > 2 else "未知",
                                    "厂商": parts[3] if len(parts) > 3 else "未知"
                                }
                                # 添加到对应的磁盘信息中
                                for disk in disks:
                                    if parts[0] in disk["设备"]:
                                        disk.update(disk_detail)
                                        break

                except (subprocess.TimeoutExpired, FileNotFoundError):
                    pass

                # 尝试使用smartctl获取详细信息
                try:
                    result = subprocess.run(['lsblk', '-d', '-n', '-o', 'NAME'], capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        disk_names = result.stdout.strip().split('\n')
                        for disk_name in disk_names:
                            if disk_name:
                                try:
                                    smart_result = subprocess.run(
                                        ['smartctl', '-i', f'/dev/{disk_name}'],
                                        capture_output=True, text=True, timeout=5
                                    )
                                    if smart_result.returncode == 0:
                                        output = smart_result.stdout

                                        vendor = "未知"
                                        model = "未知"
                                        serial = "未知"

                                        vendor_match = re.search(r'Vendor:\s*(.+)', output)
                                        if vendor_match:
                                            vendor = vendor_match.group(1).strip()

                                        model_match = re.search(r'Device Model:\s*(.+)', output) or re.search(r'Model Family:\s*(.+)', output)
                                        if model_match:
                                            model = model_match.group(1).strip()

                                        serial_match = re.search(r'Serial Number:\s*(.+)', output)
                                        if serial_match:
                                            serial = serial_match.group(1).strip()

                                        # 更新对应磁盘信息
                                        for disk in disks:
                                            if disk_name in disk["设备"]:
                                                if "厂商" not in disk:
                                                    disk["厂商"] = vendor
                                                if "型号" not in disk:
                                                    disk["型号"] = model
                                                if "序列号" not in disk:
                                                    disk["序列号"] = serial
                                                break

                                except (subprocess.TimeoutExpired, FileNotFoundError):
                                    continue
                except (subprocess.TimeoutExpired, FileNotFoundError):
                    pass

            elif platform.system() == "Windows":
                try:
                    result = subprocess.run(
                        ['wmic', 'diskdrive', 'get', 'Model,Size,SerialNumber,InterfaceType'],
                        capture_output=True, text=True, timeout=10
                    )
                    if result.returncode == 0:
                        lines = result.stdout.strip().split('\n')
                        for line in lines[1:]:
                            parts = line.strip().split()
                            if parts:
                                disk_detail = {
                                    "型号": parts[0],
                                    "容量": self._format_size(int(parts[1])) if len(parts) > 1 and parts[1].isdigit() else "未知",
                                    "序列号": parts[2] if len(parts) > 2 else "未知",
                                    "接口类型": parts[3] if len(parts) > 3 else "未知"
                                }
                                # 尝试匹配到现有磁盘
                                for disk in disks:
                                    if "型号" not in disk:
                                        disk.update(disk_detail)
                                        break
                                else:
                                    disks.append(disk_detail)

                except (subprocess.TimeoutExpired, FileNotFoundError):
                    pass

        except Exception as e:
            print(f"获取硬盘信息时出错: {e}")

        self.disk_info = disks
        return disks

    def get_network_info(self) -> List[Dict[str, Any]]:
        """获取网卡信息"""
        print("正在获取网卡信息...")

        networks = []

        try:
            # 获取网络接口统计信息
            net_io = psutil.net_io_counters(pernic=True)

            # 获取网络接口地址
            net_addrs = psutil.net_if_addrs()

            for interface_name, addrs in net_addrs.items():
                info = {
                    "接口名称": interface_name,
                    "IPv4地址": [],
                    "IPv6地址": [],
                    "MAC地址": "",
                    "状态": "未知"
                }

                # 获取地址信息
                for addr in addrs:
                    if addr.family == socket.AF_INET:
                        info["IPv4地址"].append(addr.address)
                    elif addr.family == socket.AF_INET6:
                        info["IPv6地址"].append(addr.address)
                    elif addr.family == psutil.AF_LINK:
                        info["MAC地址"] = addr.address

                # 获取I/O统计信息
                if interface_name in net_io:
                    io = net_io[interface_name]
                    info.update({
                        "发送字节数": self._format_size(io.bytes_sent),
                        "接收字节数": self._format_size(io.bytes_recv),
                        "发送包数": str(io.packets_sent),
                        "接收包数": str(io.packets_recv),
                        "发送错误": str(io.errout),
                        "��收错误": str(io.errin)
                    })

                # 尝试获取更多详细信息
                if platform.system() == "Linux":
                    try:
                        # 使用ethtool获取网卡详细信息
                        result = subprocess.run(['ethtool', '-i', interface_name],
                                              capture_output=True, text=True, timeout=5)
                        if result.returncode == 0:
                            output = result.stdout

                            driver_match = re.search(r'driver:\s*(.+)', output)
                            if driver_match:
                                info["驱动程序"] = driver_match.group(1).strip()

                            version_match = re.search(r'version:\s*(.+)', output)
                            if version_match:
                                info["驱动版本"] = version_match.group(1).strip()

                            bus_info_match = re.search(r'bus-info:\s*(.+)', output)
                            if bus_info_match:
                                info["总线信息"] = bus_info_match.group(1).strip()

                        # 使用ip link查看状态
                        result = subprocess.run(['ip', 'link', 'show', interface_name],
                                              capture_output=True, text=True, timeout=5)
                        if result.returncode == 0:
                            if 'UP' in result.stdout:
                                info["状态"] = "UP (已启用)"
                            elif 'DOWN' in result.stdout:
                                info["状态"] = "DOWN (已禁用)"

                        # 从lspci获取网卡详细信息
                        result = subprocess.run(['lspci', '-v'], capture_output=True, text=True, timeout=5)
                        if result.returncode == 0:
                            output = result.stdout
                            # 查找包含MAC地址的网卡信息
                            if info["MAC地址"]:
                                mac_section = output.find(info["MAC地址"])
                                if mac_section != -1:
                                    section = output[max(0, mac_section-500):mac_section+500]
                                    vendor_match = re.search(r'Vendor:\s*(.+)', section)
                                    if vendor_match:
                                        info["厂商"] = vendor_match.group(1).strip()

                    except (subprocess.TimeoutExpired, FileNotFoundError):
                        pass

                elif platform.system() == "Windows":
                    try:
                        result = subprocess.run(
                            ['wmic', 'nic', 'where', f'NetConnectionID="{interface_name}"', 'get', 'Manufacturer,ProductName,DriverVersion,MACAddress'],
                            capture_output=True, text=True, timeout=10
                        )
                        if result.returncode == 0:
                            lines = result.stdout.strip().split('\n')
                            if len(lines) > 1:
                                parts = [p.strip() for p in lines[1].split()]
                                if parts:
                                    info["厂商"] = parts[0]
                                    if len(parts) > 1:
                                        info["产品名称"] = parts[1]
                                    if len(parts) > 2:
                                        info["驱动版本"] = parts[2]

                    except (subprocess.TimeoutExpired, FileNotFoundError):
                        pass

                elif platform.system() == "Darwin":
                    try:
                        result = subprocess.run(['ifconfig', interface_name], capture_output=True, text=True, timeout=5)
                        if result.returncode == 0:
                            if 'status: active' in result.stdout:
                                info["状态"] = "active (已启用)"
                            else:
                                info["状态"] = "inactive"

                    except (subprocess.TimeoutExpired, FileNotFoundError):
                        pass

                networks.append(info)

        except Exception as e:
            print(f"获取网卡信息时出错: {e}")

        self.network_info = networks
        return networks

    def _format_size(self, size_bytes: int) -> str:
        """格式化字节大小为人类可读格式"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"

    def collect_all(self) -> Dict[str, Any]:
        """收集所有硬件信息"""
        print("=" * 60)
        print("开始收集设备硬件信息...")
        print("=" * 60)
        print()

        all_info = {
            "系统信息": self.get_system_info(),
            "CPU信息": self.get_cpu_info(),
            "外网IP信息": self.get_external_ip_info(),
            "GPU信息": self.get_gpu_info(),
            "NPU信息": self.get_npu_info(),
            "内存信息": self.get_memory_info(),
            "硬盘信息": self.get_disk_info(),
            "网卡信息": self.get_network_info()
        }

        print()
        print("=" * 60)
        print("硬件信息收集完成！")
        print("=" * 60)

        return all_info

    def print_info(self, info: Optional[Dict[str, Any]] = None):
        """打印硬件信息"""
        if info is None:
            info = self.collect_all()

        print()
        print("=" * 60)
        print("设备硬件信息报告")
        print("=" * 60)
        print()

        # 系统信息
        print("【系统基本信息】")
        print("-" * 60)
        for key, value in info["系统信息"].items():
            print(f"{key:15}: {value}")
        print()

        # CPU信息
        print("【CPU信息】")
        print("-" * 60)
        for key, value in info["CPU信息"].items():
            print(f"{key:15}: {value}")
        print()

        # 外网IP信息
        print("【外网IP信息】")
        print("-" * 60)
        for key, value in info["外网IP信息"].items():
            print(f"{key:15}: {value}")
        print()

        # GPU信息
        print("【GPU/GPGPU信息】")
        print("-" * 60)
        if info["GPU信息"]:
            # 按厂商分组显示
            from collections import defaultdict
            vendor_groups = defaultdict(list)
            for gpu in info["GPU信息"]:
                vendor = gpu.get("厂商", "未知")
                vendor_groups[vendor].append(gpu)

            for vendor, gpus in sorted(vendor_groups.items()):
                print(f"{vendor}:")
                for i, gpu in enumerate(gpus, 1):
                    print(f"  设备 {i}:")
                    for key, value in gpu.items():
                        if key != "厂商":
                            print(f"    {key:15}: {value}")
        else:
            print("未检测到GPU/GPGPU设备")
        print()

        # NPU信息
        print("【NPU信息】")
        print("-" * 60)
        if info["NPU信息"]:
            for i, npu in enumerate(info["NPU信息"], 1):
                print(f"NPU {i}:")
                for key, value in npu.items():
                    print(f"  {key:15}: {value}")
        else:
            print("未检测到NPU设备")
        print()

        # 内存信息
        print("【内存信息】")
        print("-" * 60)
        for key, value in info["内存信息"].items():
            if key != "内存详细信息":
                print(f"{key:15}: {value}")
        if "内存详细信息" in info["内存信息"]:
            print("\n内存详细信息:")
            for i, mem in enumerate(info["内存信息"]["内存详细信息"], 1):
                print(f"  内存条 {i}:")
                for key, value in mem.items():
                    print(f"    {key:15}: {value}")
        print()

        # 硬盘信息
        print("【硬盘信息】")
        print("-" * 60)
        if info["硬盘信息"]:
            for i, disk in enumerate(info["硬盘信息"], 1):
                print(f"磁盘 {i}:")
                for key, value in disk.items():
                    print(f"  {key:15}: {value}")
        else:
            print("未检测到硬盘设备")
        print()

        # 网卡信息
        print("【网卡信息】")
        print("-" * 60)
        if info["网卡信息"]:
            for i, net in enumerate(info["网卡信息"], 1):
                print(f"网卡 {i}:")
                for key, value in net.items():
                    if isinstance(value, list) and value:
                        print(f"  {key:15}: {', '.join(value)}")
                    elif value:
                        print(f"  {key:15}: {value}")
        else:
            print("未检测到网卡设备")
        print()

        print("=" * 60)
        print("报告结束")
        print("=" * 60)

    def save_to_json(self, filename: str = "hardware_info.json"):
        """将硬件信息保存为JSON文件"""
        info = {
            "系统信息": self.system_info,
            "CPU信息": self.cpu_info,
            "外网IP信息": self.ip_info,
            "GPU信息": self.gpu_info,
            "NPU信息": self.npu_info,
            "内存信息": self.memory_info,
            "硬盘信息": self.disk_info,
            "网卡信息": self.network_info
        }

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(info, f, ensure_ascii=False, indent=2)
            print(f"\n硬件信息已保存到: {filename}")
        except Exception as e:
            print(f"保存JSON文件时出错: {e}")


def main():
    """主函数"""
    try:
        # 创建收集器实例
        collector = HardwareInfoCollector()

        # 收集所有信息
        all_info = collector.collect_all()

        # 打印信息
        collector.print_info(all_info)

        # 保存为JSON文件
        collector.save_to_json()

        print("\n注意: 某些信息可能需要管理员/root权限才能获取完整详情")
        print("如果NPU/GPU信息显示不完整，请尝试使用sudo权限运行此脚本")

    except KeyboardInterrupt:
        print("\n\n用户中断操作")
        sys.exit(0)
    except Exception as e:
        print(f"\n发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
