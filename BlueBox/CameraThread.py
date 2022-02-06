import cv2
import logging
import threading


class CameraThread(threading.Thread):
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
        logging.info("Starting.")

        try:
            while True:
                logging.debug(f"Camera number {self.camID} capture a new frame")
                ret, frame = self.vidCap.read()

                # Write the frame we just grabbed
                self.vidWriter.write(frame)
        except KeyboardInterrupt():
            self.vidCap.release()
            self.vidWriter.release()
