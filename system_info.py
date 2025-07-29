import os
import platform
import psutil
import requests
import json
import socket
import uuid
import datetime
import cpuinfo
import GPUtil
import time

def get_system_info():
    info = {
        "system": {
            "hostname": socket.gethostname(),
            "os": platform.system(),
            "os_version": platform.version(),
            "os_release": platform.release(),
            "architecture": platform.architecture()[0],
            "machine": platform.machine(),
            "processor": platform.processor(),
            "cpu_info": cpuinfo.get_cpu_info()['brand_raw'],
            "boot_time": datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"),
            "uptime": str(datetime.timedelta(seconds=time.time() - psutil.boot_time())),
            "local_ip": socket.gethostbyname(socket.gethostname()),
            "mac_address": ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1])
        },
        "python": {
            "version": platform.python_version(),
            "implementation": platform.python_implementation(),
            "compiler": platform.python_compiler(),
            "build": platform.python_build(),
            "path": os.path.realpath(os.path.dirname(__file__)),
            "python_home": os.getenv('PYTHONHOME', 'Not set')
        },
        "hardware": {
            "cpu": {
                "physical_cores": psutil.cpu_count(logical=False),
                "logical_cores": psutil.cpu_count(logical=True),
                "usage_per_core": [f"{x}%" for x in psutil.cpu_percent(percpu=True)],
                "total_usage": f"{psutil.cpu_percent()}%",
                "frequency": {
                    "current": f"{psutil.cpu_freq().current:.2f} MHz",
                    "min": f"{psutil.cpu_freq().min:.2f} MHz",
                    "max": f"{psutil.cpu_freq().max:.2f} MHz"
                }
            },
            "memory": {
                "total": f"{psutil.virtual_memory().total / (1024**3):.2f} GB",
                "available": f"{psutil.virtual_memory().available / (1024**3):.2f} GB",
                "used": f"{psutil.virtual_memory().used / (1024**3):.2f} GB",
                "percent": f"{psutil.virtual_memory().percent}%",
                "swap_total": f"{psutil.swap_memory().total / (1024**3):.2f} GB",
                "swap_used": f"{psutil.swap_memory().used / (1024**3):.2f} GB",
                "swap_free": f"{psutil.swap_memory().free / (1024**3):.2f} GB"
            },
            "disks": [],
            "gpu": []
        },
        "network": {
            "public_ip": requests.get('https://api.ipify.org').text,
            "geo_location": get_geo_location(),
            "connections": []
        }
    }

    for partition in psutil.disk_partitions():
        usage = psutil.disk_usage(partition.mountpoint)
        info["hardware"]["disks"].append({
            "device": partition.device,
            "mountpoint": partition.mountpoint,
            "fstype": partition.fstype,
            "total": f"{usage.total / (1024**3):.2f} GB",
            "used": f"{usage.used / (1024**3):.2f} GB",
            "free": f"{usage.free / (1024**3):.2f} GB",
            "percent": f"{usage.percent}%"
        })

    try:
        gpus = GPUtil.getGPUs()
        for gpu in gpus:
            info["hardware"]["gpu"].append({
                "id": gpu.id,
                "name": gpu.name,
                "load": f"{gpu.load*100}%",
                "memory_total": f"{gpu.memoryTotal} MB",
                "memory_used": f"{gpu.memoryUsed} MB",
                "memory_free": f"{gpu.memoryFree} MB",
                "temperature": f"{gpu.temperature} °C"
            })
    except:
        pass

    for conn in psutil.net_connections(kind='inet'):
        info["network"]["connections"].append({
            "fd": conn.fd,
            "family": conn.family,
            "type": conn.type,
            "local_address": f"{conn.laddr.ip}:{conn.laddr.port}",
            "remote_address": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None,
            "status": conn.status,
            "pid": conn.pid
        })

    return info

def get_geo_location():
    try:
        response = requests.get('http://ipinfo.io/json')
        return response.json()
    except:
        return None

if __name__ == "__main__":
    info = get_system_info()
    print(json.dumps(info, indent=4, ensure_ascii=False))
