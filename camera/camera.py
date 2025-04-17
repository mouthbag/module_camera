import cv2
from logging import Logger, StreamHandler, Formatter, getLogger
import subprocess


from camera.moduledefines import DEFAULTLOGLEVEL, LOGGINGFORMAT

class CAMERA():
    
    def __init__(self, logger:Logger=None):
        
        if logger is None:
            self.__logger=self.__create_logger()
        else:
            self.__logger=logger
        
        self.__camera:cv2.VideoCapture
    
    def __create_logger(self)->Logger:
        logger=getLogger(name="DOUBLE ANTENNA")
        logger.setLevel(DEFAULTLOGLEVEL)
        loggingFormat=Formatter(LOGGINGFORMAT)
        loggingStream=StreamHandler()
        loggingStream.setFormatter(loggingFormat)
        loggingStream.setLevel(DEFAULTLOGLEVEL)
        logger.addHandler(loggingStream)
        return logger
        
    
    
    def open_camera(self):
        self.__camera=cv2.VideoCapture()
    
        if self.__camera.isOpened == False:
            self.__logger.error("Could not open camera.")
    
    def take_image(self,path:str=None):
        
        
            
        