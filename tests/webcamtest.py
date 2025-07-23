import context
import time

from camera.webcam import WEBCAM

if __name__=='__main__':
    
    address='http://100.83.37.8:8081/'
    sleep_time=10
    
    webcam=WEBCAM(webcam_address=address,
                  display_frame=True)
    
    webcam.start()
    
    time.sleep(sleep_time)
    
    webcam.save_closest_images(time_stamp=time.time()-3,
                               output_path="/home/todor/pferde/module_camera")    