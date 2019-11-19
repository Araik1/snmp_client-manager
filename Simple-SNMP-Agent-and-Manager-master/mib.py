import threading
import platform
import socket
import re
import uuid
import json
import psutil

class Mib(object):
    
    def __init__(self):
        self._lock = threading.RLock()
        try:
            self._platform = platform.system()
            self._platformRelease = platform.release()
            self._platformVersion = platform.version()
            self._architecture = platform.machine()
            self._hostname = socket.gethostname()
            self._ipAddress = socket.gethostbyname(socket.gethostname())
            self._macAddress = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
            self._processor = platform.processor()
            self._ram = str(
                round(psutil.virtual_memory().total / (1024.0 ** 3)))+" GB"

        except Exception as e:
            logging.exception(e)

    def getPlatform(self):
        return self._platform

    def setPlatform(self, value):
        with self._lock:
            self._platform = value
    
    def getPlatformRelease(self):
        return self._platformRelease

    def setPlatformRelease(self, value):
        with self._lock:
            self._platformRelease = value
    
    def getPlatformVersion(self):
        return self._platformVersion

    def setPlatformVersion(self, value):
        with self._lock:
            self._platformVersion = value
    
    def getArchitecture(self):
        return self._architecture

    def setArchitecture(self, value):
        with self._lock:
            self._architecture = value
    
    def getHostname(self):
        return self._hostname

    def setHostname(self, value):
        with self._lock:
            self._hostname = value
    
    def getIpAddress(self):
        return self._ipAddress

    def setIpAddress(self, value):
        with self._lock:
            self._ipAddress = value
    
    def getMacAddress(self):
        return self._macAddress

    def setMacAddress(self, value):
        with self._lock:
            self._macAddress = value
    
    def getProcessor(self):
        return self._processor

    def setProcessor(self, value):
        with self._lock:
            self._processor = value
    
    def getRam(self):
        return self._ram

    def setRam(self, value):
        with self._lock:
            self._ram = value


