import os
import platform
import psutil
import requests
import json

def print_system_info():
    # 获取操作系统信息
    os_name = platform.system()
    os_version = platform.version()
    os_arch = platform.architecture()[0]
    python_version = platform.python_version()
    python_home = os.getenv('PYTHONHOME', 'Not set')

    print(f"Operating System: {os_name}")
    print(f"OS Version: {os_version}")
    print(f"OS Architecture: {os_arch}")
    print(f"Python Version: {python_version}")
    print(f"Python Home: {python_home}")

    # 获取内存信息
    total_memory = psutil.virtual_memory().total / (1024 * 1024 * 1024)  # GB
    available_memory = psutil.virtual_memory().available / (1024 * 1024 * 1024)  # GB
    used_memory = psutil.virtual_memory().used / (1024 * 1024 * 1024)  # GB

    print(f"Total Memory: {total_memory:.2f} GB")
    print(f"Available Memory: {available_memory:.2f} GB")
    print(f"Used Memory: {used_memory:.2f} GB")

def print_geo_location():
    try:
        # 获取地理位置
        response = requests.get('http://ipinfo.io/json')
        geo_data = response.json()
        
        # 格式化输出
        formatted_geo_data = json.dumps(geo_data, indent=4)
        print("Formatted Geo Location Data: ")
        print(formatted_geo_data)
    except Exception as e:
        print(f"Error fetching geo-location: {e}")

if __name__ == "__main__":
    print_system_info()
    print_geo_location()
