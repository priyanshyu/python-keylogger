import os
import platform
import socket
import uuid
from datetime import datetime

def get_system_info():
    return {
        "platform": platform.system(),
        "platform_release": platform.release(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "hostname": socket.gethostname(),
        "ip_address": socket.gethostbyname(socket.gethostname()),
        "mac_address": ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff)
                                 for elements in range(0, 2*6, 8)][::-1]),
        "processor": platform.processor(),
        "timestamp": str(datetime.now())
    }

def get_current_time():
    return str(datetime.now())

def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
