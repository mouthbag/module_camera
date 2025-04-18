import cv2
import paho
import paho.mqtt
import paho.mqtt.client
import requests

from logging import Logger, StreamHandler, Formatter, getLogger

from camera.moduledefines import DEFAULTLOGLEVEL, LOGGINGFORMAT

class CAMERA():
    
    def __init__(self,
                 last_image_path:str,
                 mqtt_host:str,
                 mqtt_port:int,
                 mqtt_user:str,
                 mqtt_password:str,
                 image_topic:str,
                 logger:Logger=None):
        
        if logger is None:
            self.__logger=self.__create_logger()
        else:
            self.__logger=logger
        
        self.__last_image_path=last_image_path
        self.__last_image_topic=image_topic
        
        self.__mqtt_host=mqtt_host
        self.__mqtt_port=mqtt_port
        self.__mqtt_user=mqtt_user
        self.__mqtt_password=mqtt_password
        
        self.__mqtt_client:paho.mqtt.client.Client
        
        self.__connect_mqtt()
        
    def __connect_mqtt(self):
        self.__mqtt_client=paho.mqtt.client.Client()
        
        #Set credentials
        self.__mqtt_client.username_pw_set(username=self.__mqtt_user,
                                           password=self.__mqtt_password)
        
        #Set callbacks
        self.__mqtt_client.on_connect=self.__on_mqtt_connected
        self.__mqtt_client.on_disconnect=self.__on_mqtt_disconnected
        self.__mqtt_client.on_connect_fail=self.__on_mqtt_connect_fail
        
        self.__mqtt_client.reconnect_delay_set(min_delay=1,max_delay=5)
        self.__mqtt_client.disable_logger()
        
        #Connect MQTT client
        self.__mqtt_client.connect_async(host=self.__mqtt_host,
                                         port=self.__mqtt_port)
        
        
        self.__mqtt_client.loop_start()
     
    def __on_mqtt_connect_fail(self,client,userdata):
        self.__logger.error("Connection failed. Starting reconnection attempt")
        self.__mqtt_client.reconnect()
        
    def __on_mqtt_connected(self, client, userdata, flags, rc):
        self.__logger.info("MQTT client connected.")

    
    def __on_mqtt_disconnected(self, client, userdata, rc):
        self.__logger.error("MQTT client disconnected. Trying to reconnect.")
        
        self.__mqtt_client.connect_async(host=self.__mqtt_host,
                                         port=self.__mqtt_port)
    
    
    def __create_logger(self)->Logger:
        logger=getLogger(name="CAMERA")
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
        response=requests.get("http://localhost:8080/0/action/snapshot")
        
    def send_last_image_to_mqtt(self):
        
        with open(self.__last_image_path,'rb') as image_file:
            
            image=image_file.read()
            
            self.__mqtt_client.publish(topic=self.__last_image_topic,
                                       payload=image)
        
        
        
            
        