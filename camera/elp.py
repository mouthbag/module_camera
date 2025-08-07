import cv2

from time import sleep




class ELP():
    
    def __init__(self):
        
        #print(cv2.__version__)
        
        #Open camera
        camera=cv2.VideoCapture(2,cv2.CAP_V4L2)
        
        if not camera.isOpened():
            print("Could not open camera.")
            return
        else:
            print("Camera open.")
            
        camera.set(cv2.CAP_PROP_AUTO_EXPOSURE,1)
        
        #camera.set(cv2.CAP_PROP_AUTO_EXPOSURE,1)
            
        camera.set(cv2.CAP_PROP_EXPOSURE,10.0)
        
        #sleep(5)
        
        for i in range(0,10):
            camera.grab()
            
        camera.grab()
        
        ret, image=camera.retrieve(2)
        
        cv2.imshow('Snapshot',image)
        
        cv2.waitKey(0)