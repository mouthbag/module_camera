import context
import time

import matplotlib.pyplot as plt

from PIL import Image

from camera.webcam import WEBCAM

if __name__=='__main__':
    
    address='http://100.83.37.8:8081/'
    sleep_time=5
    
    webcam=WEBCAM(webcam_address=address,
                  display_frame=False)
    
    webcam.start()
    
    time.sleep(sleep_time)
    
    image_list=webcam.get_closest_images(time_stamp=time.time()-sleep_time,
                              image_count=5,
                              time_offset=0)
    
    detection_images=[image[1] for image in image_list]
    
    detection_images=[Image.fromarray(array) for array in detection_images]
    
    #for img in detection_images:
   # 
   #     plt.imshow(img)
   #     plt.show()
    
    bla=0
    
    from  uuid import uuid4
    from io import BytesIO
    import psycopg2 as ps
    import numpy
    table_name='resnet_detection'
    
    session_id=uuid4()
    
    img_buffer=BytesIO()
    detection_images[0].save(img_buffer,format='JPEG')
    
    
    parameters={
                    'sessionid'         :   str(session_id),
                    'image'             :   ps.Binary(img_buffer.getvalue()),
                    'yolo_box_x1'       :   0,
                    'yolo_box_x2'       :   100,
                    'yolo_box_y1'       :   0,
                    'yolo_box_y2'       :   100,
                    'yolo_class'        :   "some_class",
                    'yolo_confidence'   :   0.56,
                    'resnet_embedding'  :   numpy.array([0,1,2,3]).tobytes(),
                    'distances'         :   [[0.1,0,3]],
                    'predictions'       :   ['none'],
                    'result'            :   "blah",
                    'host'              :   "some host"
                }
            
    query="""INSERT INTO {} (sessionid, image, yolo_box_x1, yolo_box_x2, yolo_box_y1, yolo_box_y2, yolo_class,
    yolo_confidence, resnet_embedding, distances, predictions,result,host)
    values (%(sessionid)s, %(image)s, %(yolo_box_x1)s, %(yolo_box_x2)s, %(yolo_box_y1)s, %(yolo_box_y2)s, %(yolo_class)s,
    %(yolo_confidence)s, %(resnet_embedding)s, %(distances)s, %(predictions)s, %(result)s, %(host)s)
    """.format(table_name)
    
    db_parameters={'db_host':"100.105.245.157",
               'db_port':5432,
               'db_name':"master",
               'db_user':"pferdeaue",
               'db_password':"pferdeaue"}
    
    db_connection=ps.connect(host=db_parameters['db_host'],
                             port=db_parameters['db_port'],
                             user=db_parameters['db_user'],
                             password=db_parameters['db_password'],
                             dbname=db_parameters['db_name'])
    
    with db_connection.cursor() as cur:
        
        cur.execute(query=query,vars=parameters)
        db_connection.commit()
    
    import pandas as pd
       
    with db_connection.cursor() as cur:
        
        query="""SELECT * FROM {} where sessionid='{}'""".format(table_name,str(session_id))
        
        parameters={
            'sessionid' : str(session_id)
        }
        
        cur.execute(query=query,vars=parameters)
        
        rows=cur.fetchall()
        
        columns=[desc[0] for desc in cur.description]
        
        mydata=pd.DataFrame(rows,columns=columns)
    
    #mydata=mydata[mydata['sessionid']==session_id]
    print(mydata)
    for index,result in mydata.iterrows():
        
        print(result['sessionid'])
        
        output_img=Image.open(BytesIO(result['image']))
        
    plt.imshow(output_img)
    plt.show()
        
    bla=0
        
        