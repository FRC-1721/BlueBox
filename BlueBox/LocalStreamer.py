import cv2
import time
import logging
import threading
import subprocess as sp


class LocalStreamer(threading.Thread):
    """
    Each local camera should have a LocalStreamer
    dedicated to it. This thread should handle reconnecting
    if the camera goes dead, as well as transcoding, and serving
    the camera via mjpeg.
    """

    def __init__(self, camID):
        threading.Thread.__init__(self)

        # This camera's cam ID
        self.camID = camID

        # Setup a video capture
        self.vidCap = cv2.VideoCapture(self.camID)

        codec = cv2.VideoWriter_fourcc(*"MJPG")
        fps = 29.9  # 29.9
        resolution = (640, 480)
        self.vidWriter = cv2.VideoWriter(
            f"videos/camera{self.camID}.avi", codec, fps, resolution
        )

        command = ["ffmpeg", "-i", "-", "-f", "flv", "localhost:9000"]
        self.ffmpeg = sp.Popen(command, stdin=sp.PIPE, shell=False)

    def run(self):
        logging.info(f"Thread for camera {self.camID} has started.")

        while True:
            logging.debug(
                f"Camera number {self.camID} Attempting to capture a new frame"
            )
            ret, frame = self.vidCap.read()

            if not ret:
                logging.error("Could not capture last frame.")

            else:
                logging.debug("Frame was valid, writing to file.")
                self.vidWriter.write(frame)
                logging.info("Wrote frame.")

                self.ffmpeg.stdin.write(frame.tobytes())

                cv2.imshow("My cam video", frame)

            time.sleep(0.01)

    def terminate(self):
        cv2.destroyAllWindows()
        self.vidCap.release()
        self.vidWriter.release()
