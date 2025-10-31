import requests
import base64
import cv2
import numpy as np
import time
from PIL import Image
from io import BytesIO

from camera.moduledefines import DEFAULTLOGLEVEL, LOGGINGFORMAT, DEFAULTFLASKPORT
from logging import Logger, StreamHandler, Formatter, getLogger

class FLASKIMAGECLIENT:
    def __init__(self,
                 server_ip,
                 port=DEFAULTFLASKPORT,
                 default_time_offset=0,
                 default_image_count=5,
                 logger:Logger=None):
        
        if logger is None:
            self.__logger=self.__create_logger()
        else:
            self.__logger=logger
        
        self.__default_time_offset=default_time_offset
        self.__default_image_count=default_image_count
        
        self.__base_url = f"http://{server_ip}:{port}"
        self.__logger.info(f"Server url: {self.__base_url}:{port}")

    def __create_logger(self)->Logger:
        logger=getLogger(name="FLASKCLIENT")
        logger.setLevel(DEFAULTLOGLEVEL)
        loggingFormat=Formatter(LOGGINGFORMAT)
        loggingStream=StreamHandler()
        loggingStream.setFormatter(loggingFormat)
        loggingStream.setLevel(DEFAULTLOGLEVEL)
        logger.addHandler(loggingStream)
        return logger

    def get_health(self):
        try:
            r = requests.get(f"{self.__base_url}/health", timeout=1)
            return r.status_code == 200
        except requests.RequestException:
            return False

    def get_images(self,
                   timestamp,
                   time_offset=None,
                   image_count=None):
        
        if time_offset is None:
            time_offset=self.__default_time_offset
        if image_count is None:
            image_count=self.__default_image_count
        
        try:
            url = f"{self.__base_url}/get_images?timestamp={timestamp}&timeoffset={time_offset}&imagecount={image_count}"
            r = requests.get(url, timeout=5)
            r.raise_for_status()
            data = r.json()

            images = []
            for i, entry in enumerate(data):
                #delta = entry["timestamp_delta"]
                b64 = entry["image"]
                img_bytes = base64.b64decode(b64)
                #img_array = np.frombuffer(img_bytes, dtype=np.uint8)
                #img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                
                img=Image.open(BytesIO(img_bytes))
                
                images.append(img)
            return images

        except Exception as e:
            self.__logger.error(f"{repr(e)}")
            return []