#!/usr/bin/env python3
"""
增强版公网IP查询工具
获取IP地址及详细的地理位置信息
"""

import requests
import json
import sys
from typing import Dict, Any, Optional, List
import time


class IPGeolocationService:
    """IP地理位置查询服务"""

    def __init__(self, timeout: int = 10):
        """
        初始化IP查询服务

        Args:
            timeout: 请求超时时间（秒）
        """
        self.timeout = timeout
        self.ip_address = None
        self.geo_info = {}

    # 定义多个IP查询服务
    IP_SERVICES = [
        {
            'name': 'ipify',
            'url': 'https://api.ipify.org?format=json',
            'ip_key': 'ip',
            'priority': 1
        },
        {
            'name': 'ipinfo.io',
            'url': 'https://ipinfo.io/json',
            'ip_key': 'ip',
            'priority': 2
        },
        {
            'name': 'ip-api',
            'url': 'http://ip-api.com/json/',
            'ip_key': 'query',
            'priority': 3
        },
        {
            'name': 'ifconfig.me',
            'url': 'https://ifconfig.me/all.json',
            'ip_key': 'ip_addr',
            'priority': 4
        },
        {
            'name': 'icanhazip',
            'url': 'https://icanhazip.com/',
            'ip_key': None,
            'is_text': True,
            'priority': 5
        },
        {
            'name': 'checkip.amazonaws.com',
            'url': 'https://checkip.amazonaws.com/',
            'ip_key': None,
            'is_text': True,
            'priority': 6
        }
    ]

    # 定义多个地理位置查询服务
    GEO_SERVICES = [
        {
            'name': 'ip-api',
            'url': 'http://ip-api.com/json/{ip}',
            'fields': 'status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query',
            'priority': 1
        },
        {
            'name': 'ipinfo.io',
            'url': 'https://ipinfo.io/{ip}/json',
            'priority': 2
        },
        {
            'name': 'ip-api.com (field)',
            'url': 'http://ip-api.com/json/{ip}?fields=status,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query',
            'priority': 3
        },
        {
            'name': 'ipapi.co',
            'url': 'https://ipapi.co/{ip}/json/',
            'priority': 4
        },
        {
            'name': 'ipwhois.app',
            'url': 'https://ipwhois.app/json/{ip}',
            'priority': 5
        }
    ]

    def get_public_ip(self) -> Optional[str]:
        """
        获取公网IP地址

        Returns:
            IP地址字符串，失败返回None
        """
        print("=" * 70)
        print("正在获取公网IP地址...")
        print("=" * 70)
        print()

        # 按优先级排序
        sorted_services = sorted(self.IP_SERVICES, key=lambda x: x['priority'])

        for service in sorted_services:
            try:
                response = requests.get(
                    service['url'],
                    timeout=self.timeout
                )
                response.raise_for_status()

                if service.get('is_text', False):
                    # 纯文本响应
                    ip = response.text.strip()
                else:
                    # JSON响应
                    data = response.json()
                    ip_key = service.get('ip_key', 'ip')
                    ip = data.get(ip_key)

                if ip and self._validate_ip(ip):
                    print(f"✓ 从 {service['name']} 成功获取IP: {ip}")
                    self.ip_address = ip
                    return ip

            except requests.exceptions.RequestException as e:
                print(f"✗ {service['name']} 请求失败: {str(e)}")
            except (KeyError, ValueError) as e:
                print(f"✗ {service['name']} 解析失败: {str(e)}")
            except Exception as e:
                print(f"✗ {service['name']} 未知错误: {str(e)}")

            time.sleep(0.5)  # 避免请求过快

        print("\n所有服务均失败，无法获取公网IP")
        return None

    def get_geolocation_info(self, ip: str) -> Optional[Dict[str, Any]]:
        """
        获取IP的地理位置信息

        Args:
            ip: IP地址

        Returns:
            地理位置信息字典，失败返回None
        """
        print(f"\n{'=' * 70}")
        print(f"正在查询IP {ip} 的地理位置信息...")
        print("=" * 70)
        print()

        # 按优先级排序
        sorted_services = sorted(self.GEO_SERVICES, key=lambda x: x['priority'])

        for service in sorted_services:
            try:
                url = service['url'].format(ip=ip)
                print(f"正在使用 {service['name']} 查询...")

                response = requests.get(url, timeout=self.timeout)
                response.raise_for_status()
                data = response.json()

                # 标准化数据格式
                geo_info = self._normalize_geo_data(data, service['name'])

                if geo_info and geo_info.get('status') != 'fail':
                    print(f"✓ {service['name']} 查询成功")
                    self.geo_info = geo_info
                    return geo_info

            except requests.exceptions.RequestException as e:
                print(f"✗ {service['name']} 请求失败: {str(e)}")
            except (KeyError, ValueError) as e:
                print(f"✗ {service['name']} 解析失败: {str(e)}")
            except Exception as e:
                print(f"✗ {service['name']} 未知错误: {str(e)}")

            time.sleep(0.5)  # 避免请求过快

        print("\n所有地理位置查询服务均失败")
        return None

    def _normalize_geo_data(self, data: Dict[str, Any], source: str) -> Optional[Dict[str, Any]]:
        """
        标准化不同服务的地理位置数据格式

        Args:
            data: 原始数据
            source: 数据来源

        Returns:
            标准化的地理位置信息
        """
        try:
            normalized = {
                'source': source,
                'status': 'success',
                'ip': data.get('ip') or data.get('query'),
                'country': data.get('country') or data.get('country_name'),
                'country_code': data.get('countryCode') or data.get('country_code'),
                'region': data.get('regionName') or data.get('region') or data.get('state'),
                'city': data.get('city'),
                'zip': data.get('zip') or data.get('postal'),
                'latitude': data.get('lat') or data.get('latitude'),
                'longitude': data.get('lon') or data.get('longitude'),
                'timezone': data.get('timezone'),
                'isp': data.get('isp'),
                'org': data.get('org'),
                'as': data.get('as'),
            }

            # 检查是否有有效数据
            if not normalized.get('ip'):
                return None

            return normalized

        except Exception as e:
            print(f"数据标准化失败: {str(e)}")
            return None

    def _validate_ip(self, ip: str) -> bool:
        """
        验证IP地址格式

        Args:
            ip: IP地址字符串

        Returns:
            是否为有效的IPv4或IPv6地址
        """
        import socket
        try:
            socket.inet_pton(socket.AF_INET, ip)
            return True
        except socket.error:
            try:
                socket.inet_pton(socket.AF_INET6, ip)
                return True
            except socket.error:
                return False

    def print_detailed_info(self, geo_info: Dict[str, Any]):
        """
        打印详细的IP地理位置信息

        Args:
            geo_info: 地理位置信息字典
        """
        print("\n" + "=" * 70)
        print("IP地址详细信息")
        print("=" * 70)

        # 基本信息
        print(f"\n📍 基本信息:")
        print("-" * 70)
        print(f"  IP地址:        {geo_info.get('ip', 'N/A')}")
        print(f"  数据来源:      {geo_info.get('source', 'N/A')}")

        # 地理位置信息
        print(f"\n🌍 地理位置信息:")
        print("-" * 70)
        print(f"  国家:          {geo_info.get('country', 'N/A')} ({geo_info.get('country_code', 'N/A')})")
        print(f"  地区/省:       {geo_info.get('region', 'N/A')}")
        print(f"  城市:          {geo_info.get('city', 'N/A')}")
        print(f"  邮政编码:      {geo_info.get('zip', 'N/A')}")

        # 坐标信息
        lat = geo_info.get('latitude')
        lon = geo_info.get('longitude')
        if lat and lon:
            print(f"  纬度:          {lat}")
            print(f"  经度:          {lon}")
            print(f"  Google地图:    https://www.google.com/maps?q={lat},{lon}")
            print(f"  百度地图:      http://api.map.baidu.com/marker?location={lat},{lon}&title=IP位置")

        # 时区信息
        if geo_info.get('timezone'):
            print(f"  时区:          {geo_info.get('timezone')}")

        # 网络信息
        print(f"\n🌐 网络信息:")
        print("-" * 70)
        print(f"  ISP运营商:      {geo_info.get('isp', 'N/A')}")
        print(f"  组织:          {geo_info.get('org', 'N/A')}")
        print(f"  AS号:          {geo_info.get('as', 'N/A')}")

        print("\n" + "=" * 70)

    def save_to_json(self, geo_info: Dict[str, Any], filename: str = 'ip_geolocation.json'):
        """
        保存信息到JSON文件

        Args:
            geo_info: 地理位置信息
            filename: 文件名
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(geo_info, f, ensure_ascii=False, indent=2)
            print(f"\n详细信息已保存到: {filename}")
        except Exception as e:
            print(f"\n保存失败: {str(e)}")

    def query_ip(self, ip: str = None) -> Optional[Dict[str, Any]]:
        """
        查询指定IP或本机公网IP的地理位置信息

        Args:
            ip: IP地址，如果为None则查询本机公网IP

        Returns:
            地理位置信息字典
        """
        # 获取IP地址
        if not ip:
            ip = self.get_public_ip()
            if not ip:
                return None
        else:
            self.ip_address = ip
            print(f"查询IP地址: {ip}")

        # 获取地理位置信息
        geo_info = self.get_geolocation_info(ip)

        if geo_info:
            self.print_detailed_info(geo_info)
            self.save_to_json(geo_info)
            return geo_info

        return None


def main():
    """主函数"""
    print("=" * 70)
    print("增强版IP地理位置查询工具")
    print("=" * 70)
    print()

    # 创建服务实例
    service = IPGeolocationService(timeout=10)

    # 如果提供了命令行参数，查询指定IP
    if len(sys.argv) > 1:
        ip = sys.argv[1]
        if service._validate_ip(ip):
            service.query_ip(ip)
        else:
            print(f"错误: '{ip}' 不是有效的IP地址")
            sys.exit(1)
    else:
        # 查询本机公网IP
        service.query_ip()


if __name__ == "__main__":
    main()
