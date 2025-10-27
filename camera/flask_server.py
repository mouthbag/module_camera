from flask import Flask, request, jsonify
from threading import Thread
import cv2
import base64

from logging import Logger, StreamHandler, Formatter, getLogger

from .webcam import WEBCAM

class FLASKSERVER(Thread):
    def __init__(self, webcam:WEBCAM,
                 host="0.0.0.0",
                 port=2003,
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

    def _setup_routes(self):
        @self.__app.route("/get_images")
        def get_images():
            try:
                ts_param = request.args.get("timestamp")
                if ts_param is None:
                    return jsonify({"error": "Missing 'timestamp' parameter"}), 400

                timestamp = float(ts_param)
                closest_images = self.__webcam.get_closest_images(timestamp, image_count=5)

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
                return jsonify({"error": str(e)}), 500

        @self.__app.route("/health")
        def health():
            return "OK", 200

    def run(self):
        self.__app.run(host=self.__host, port=self.__port, debug=False, use_reloader=False)
