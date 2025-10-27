from flask import Flask, request, jsonify
from threading import Thread
import cv2
import base64

from logging import Logger, StreamHandler, Formatter, getLogger

from camera.moduledefines import DEFAULTLOGLEVEL, LOGGINGFORMAT, DEFAULTFLASKPORT, DEFAULTFLASKHOST

from .webcam import WEBCAM

class FLASKSERVER(Thread):
    def __init__(self,
                 webcam:WEBCAM,
                 host=DEFAULTFLASKHOST,
                 port=DEFAULTFLASKPORT,
                 logger:Logger=None):
        
        super().__init__(daemon=True)
        
        if logger is None:
            self.__logger=self.__create_logger()
        else:
            self.__logger=logger
        
        self.__webcam = webcam
        self.__host = host
        self.__port = port
        self.__app = Flask(__name__)
        self._setup_routes()
        
    def __create_logger(self)->Logger:
        logger=getLogger(name="FLASKSERVER")
        logger.setLevel(DEFAULTLOGLEVEL)
        loggingFormat=Formatter(LOGGINGFORMAT)
        loggingStream=StreamHandler()
        loggingStream.setFormatter(loggingFormat)
        loggingStream.setLevel(DEFAULTLOGLEVEL)
        logger.addHandler(loggingStream)
        return logger

    def _setup_routes(self):
        @self.__app.route("/get_images")
        def get_images():
            try:
                self.__logger.debug(f"Incoming request '/get_images' from {request.remote_addr}")
                timestamp_param = request.args.get("timestamp")
                timeoffset_param=request.args.get("timeoffset")
                image_count_param=request.args.get("imagecount")
                
                if timestamp_param is None:
                    self.__logger.error("No image timestamp provided.")
                    return jsonify({"error": "Missing 'timestamp' parameter"}), 400
                
                if image_count_param is None:
                    self.__logger.error("No image count provided.")
                    return jsonify({"error": "Missing 'imagecount' parameter"}), 400
                
                if timeoffset_param is None:
                    self.__logger.error("No time offset provided.")
                    return jsonify({"error": "Missing 'timeoffset' parameter"}), 400
                    

                timestamp = float(timestamp_param)
                image_count=int(image_count_param)
                time_offset=float(timeoffset_param)
                
                self.__logger.debug(f"Timestamp: {timestamp}")
                self.__logger.debug(f"Image count: {image_count}")
                self.__logger.debug(f"Time offset: {time_offset}")
                
                closest_images = self.__webcam.get_closest_images(timestamp,
                                                                  image_count=image_count,
                                                                  time_offset=time_offset)

                result = []
                for delta, frame in closest_images:
                    _, jpg = cv2.imencode(".jpg", frame)
                    b64 = base64.b64encode(jpg.tobytes()).decode("utf-8")
                    result.append({
                        "timestamp_delta": delta,
                        "image": b64
                    })

                return jsonify(result)

            except Exception as e:
                self.__logger.error(str(e))
                return jsonify({"error": str(e)}), 500

        @self.__app.route("/health")
        def health():
            self.__logger.debug(f"Incoming request '/health' from {request.remote_addr}")
            return "OK", 200
        
        @self.__app.route("/manual")
        def manual():
            self.__logger.debug(f"Incoming request '/manual' from {request.remote_addr}")
            return (
                """\
Flask API Manual

Available Endpoints:

1. /health
   - Method: GET
   - Returns 'OK' if the server is alive and not currently engulfed in fire.

2. /get_images?timestamp=<float>&imagecount=<int>&timeoffset=<float>
   - Method: GET
   - Required parameters:
       - timestamp (float): Unix epoch timestamp in seconds
       - imagecount (int): Number of images to return (e.g., 5)
       - timeoffset (float): Acceptable time offset window in seconds (e.g., 1.5)
   - Description:
       Returns a JSON array of base64-encoded JPEGs and timestamp deltas,
       where each image is the closest match within ±timeoffset seconds.
   - Response format:
       [
           {
               "timestamp_delta": <float>,
               "image": "<base64-encoded JPEG>"
           },
           ...
       ]

3. /manual
   - Method: GET
   - Returns this documentation, because no one ever documents anything anymore.

Notes:
- All timestamps use Unix epoch (float, seconds).
- Image data is base64-encoded JPEG. Decode or perish.
- This server runs in a background thread and is doing its best.
""",
        200,
        {"Content-Type": "text/plain"},
    )

    def run(self):
        self.__app.run(host=self.__host, port=self.__port, debug=False, use_reloader=False)
