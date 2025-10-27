import requests
import base64
import cv2
import numpy as np
import time

from camera.moduledefines import DEFAULTLOGLEVEL, LOGGINGFORMAT
from logging import Logger, StreamHandler, Formatter, getLogger

class FLASTIMAGECLIENT:
    def __init__(self, server_ip, port=2003):
        self.base_url = f"http://{server_ip}:{port}"

    def get_health(self):
        try:
            r = requests.get(f"{self.base_url}/health", timeout=1)
            return r.status_code == 200
        except requests.RequestException:
            return False

    def __create_logger(self)->Logger:
        logger=getLogger(name="CAMERA")
        logger.setLevel(DEFAULTLOGLEVEL)
        loggingFormat=Formatter(LOGGINGFORMAT)
        loggingStream=StreamHandler()
        loggingStream.setFormatter(loggingFormat)
        loggingStream.setLevel(DEFAULTLOGLEVEL)
        logger.addHandler(loggingStream)
        return logger

    def get_images(self, timestamp=None):
        if timestamp is None:
            timestamp = time.time()
        
        try:
            url = f"{self.base_url}/get_images?timestamp={timestamp}"
            r = requests.get(url, timeout=5)
            r.raise_for_status()
            data = r.json()

            images = []
            for i, entry in enumerate(data):
                delta = entry["timestamp_delta"]
                b64 = entry["image"]
                img_bytes = base64.b64decode(b64)
                img_array = np.frombuffer(img_bytes, dtype=np.uint8)
                img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                images.append((delta, img))
            return images

        except Exception as e:
            print(f"[CLIENT ERROR] {e}")
            return []

