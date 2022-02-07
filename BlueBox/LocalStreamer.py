import cv2
import time
import logging
import threading


class LocalStreamer(threading.Thread):
    """
    Handles offloading the job of capturing frames
    to a separate thread, construct one for
    each camera, and make possible to support multiple
    camera stream types.
    """

    def __init__(self, camID):
        threading.Thread.__init__(self)

        # This camera's cam ID
        self.camID = camID

        # Setup a video capture
        self.vidCap = cv2.VideoCapture(self.camID)

        self.vidCodec = cv2.VideoWriter_fourcc(*"XVID")
        self.vidWriter = cv2.VideoWriter(
            f"videos/camera{self.camID}.mp4", self.vidCodec, 20.0, (640, 480)
        )

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

                cv2.imshow("My cam video", frame)

            time.sleep(0.01)

    def terminate(self):
        cv2.destroyAllWindows()
        self.vidCap.release()
        self.vidWriter.release()
