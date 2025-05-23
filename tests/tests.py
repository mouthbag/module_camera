import paho.mqtt
import paho.mqtt.client
import context
import time
import paho
import requests

from camera.camera import CAMERA

def __on_mqtt_connected(client, userdata, flags, rc):
    print("MQTT connected")
    #mqtt_client.subscribe(topic="camera")

def __on_mqtt_disconnected(client, userdata, rc):
    print("MQTT client disconnected. Trying to reconnect.")
    
    #mqtt_client.connect(host="192.168.10.119",
    #                                    port=1884)

def __on_mqtt_message(client, userdata, message:paho.mqtt.client.MQTTMessage):
    
    for i in range(0,10):
        response=requests.get("http://localhost:8080/0/action/snapshot")
        time.sleep(1)


if __name__=="__main__":
    
    camera=CAMERA(last_image_path="/home/todor/704-20250418151830-snapshot.jpg",
                  mqtt_host="192.168.10.119",
                  mqtt_port=1884,
                  mqtt_user="todor",
                  mqtt_password="bla",
                  image_topic="camera_images")
    
    camera.take_image()
    
    camera.send_last_image_to_mqtt()
    
    
    """ mqtt_client=paho.mqtt.client.Client()
    
    mqtt_client.on_connect=__on_mqtt_connected
    mqtt_client.on_disconnect=__on_mqtt_disconnected
    mqtt_client.on_message=__on_mqtt_message
    
    mqtt_client.reconnect_delay_set(min_delay=1,max_delay=5)
    
    
    #Connect MQTT client
    mqtt_client.connect(host="192.168.10.119",
                                        port=1884)
    
    print("Starting loop")
    
    mqtt_client.loop_start()
    
    while True:
        continue """
    
    
    


