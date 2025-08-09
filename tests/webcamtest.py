import context
import time

import matplotlib.pyplot as plt

from PIL import Image

from camera.webcam import WEBCAM

if __name__=='__main__':
    
    address='http://192.168.1.22/livestream/11?action=play&media=mjpeg&user=pferdeaue&pwd=Blubb..Blubb..88'
    sleep_time=5
    
    webcam=WEBCAM(webcam_address=address,
                  display_frame=False)
    
    webcam.start()
    
    time.sleep(sleep_time)
    
    #image_list=webcam.get_closest_images(time_stamp=time.time()-sleep_time,
    #                          image_count=5,
    #                          time_offset=0)
    #
    #detection_images=[image[1] for image in image_list]
    #
    #detection_images=[Image.fromarray(array) for array in detection_images]
    
    webcam.save_closest_images(time_stamp=time.time(),
                               output_path='/home/todor/instar',
                               time_offset=-sleep_time)
    
    print("Done.")
    
    #for img in detection_images:
   # 
   #     plt.imshow(img)
   #     plt.show()
    
        
        