import context
import time

from camera.webcam import WEBCAM

if __name__=='__main__':
    
    address='http://100.99.128.36:8081/'
    sleep_time=20
    
    webcam=WEBCAM(webcam_address=address)
    
    webcam.start()
    
    time.sleep(sleep_time)
    
    webcam.get_closest_images(time.time()-3)    