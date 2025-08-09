import os
import cv2

from threading import Thread, Lock
from collections import deque
from typing import Deque
from requests import get
from time import sleep, time

from logging import Logger, StreamHandler, Formatter, getLogger

from camera.moduledefines import DEFAULTLOGLEVEL, LOGGINGFORMAT

class WEBCAM(Thread):
    def __init__(self,
                 webcam_address:str,
                 display_frame:bool=False,
                 image_buffer_size:int=100,
                 logger:Logger=None):
        
        if logger is None:
            self.__logger=self.__create_logger()
        else:
            self.__logger=logger
        
        self.__logger.info("Starting up webcam module. Camera address: {}".format(webcam_address))
        
        self.__webcam_address=webcam_address
        
        self.__lock=Lock()
        
        self.__camera=cv2.VideoCapture(self.__webcam_address)
        
        self.__image_buffer:Deque=deque(maxlen=image_buffer_size)
        
        self.__display_frame=display_frame
        
        if not self.__camera.isOpened():
            self.__logger.error("Could not open connection to {}".format(self.__webcam_address))
            
        
        
        super().__init__()
        
    def __create_logger(self)->Logger:
        logger=getLogger(name="CAMERA")
        logger.setLevel(DEFAULTLOGLEVEL)
        loggingFormat=Formatter(LOGGINGFORMAT)
        loggingStream=StreamHandler()
        loggingStream.setFormatter(loggingFormat)
        loggingStream.setLevel(DEFAULTLOGLEVEL)
        logger.addHandler(loggingStream)
        return logger
        
    def run(self):
        
        while(True):
            
            if self.__camera.isOpened()==False:
                self.__camera=cv2.VideoCapture(self.__webcam_address)
            
            ret, frame = self.__camera.read()
            
            frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            
            if not ret:
                self.__logger.warning("Could not read frame.")
                continue
            
            with self.__lock:
                self.__image_buffer.append((time(),frame))
            
            if self.__display_frame==True:
                cv2.imshow(self.__webcam_address, frame)
            
            cv2.waitKey(1)
            
    def get_closest_images(self,
                           time_stamp:float,
                           image_count:int=5,
                           time_offset:int=0):
        
        try:
            self.__logger.info("Return webcam images.")
            with self.__lock:
                sorted_buffer=sorted((((ts - (time_stamp + time_offset)), frame) for ts, frame in self.__image_buffer), key=lambda x: x[0])
                
            sorted_buffer=[item for item in sorted_buffer if item[0] > 0]
            
        except Exception as ex:
            self.__logger.error("Error on closest image retrieval: {}".format(repr(ex)))
            
        return sorted_buffer[0:image_count]
    
    def save_closest_images(self,
                            time_stamp:float,
                            output_path:str,
                            image_count:int=5,
                            time_offset:int=0):
        try:
            self.__logger.info("Saving images. Destination: {}".format(output_path))
            with self.__lock:
                sorted_buffer=sorted((((ts - (time_stamp + time_offset)), frame) for ts, frame in self.__image_buffer), key=lambda x: x[0])
                
            sorted_buffer=[item for item in sorted_buffer if item[0] > 0]
            
            if len(sorted_buffer)==0:
                self.__logger.warning("No images extracted for timestamp {} and offset {}".format(time_stamp,time_offset))
            
            for frame in sorted_buffer[0:image_count]:
                timestamp=time()
                frame_name=os.path.join(output_path,f"{timestamp:.3f}.jpg")
                img=cv2.cvtColor(frame[1],cv2.COLOR_RGB2BGR)
                cv2.imwrite(filename=frame_name,img=img)
                
                
        except Exception as ex:
            self.__logger.error("Error when saving snapshots: {}".format(repr(ex)))
        
        
            
             
            
            