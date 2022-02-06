# FRC 1721
# 2022

import time
import coloredlogs, logging

from CameraThread import CameraThread


class BlueBox:
    def __init__(self):
        """
        Stuff that runs when we first start.
        """

        # Get logger
        self.logger = logging.getLogger(__name__)

        # Setup colored logs
        coloredlogs.install(level="DEBUG")

        # Make threads
        self.thread1 = CameraThread(2)
        self.thread2 = CameraThread(4)

    def run(self):
        self.thread1.start()
        self.thread2.start()

        time.sleep(2.4)


## Capture video from webcam
# vid_capture = cv2.VideoCapture(2)
# vid_cod = cv2.VideoWriter_fourcc(*"XVID")
# output = cv2.VideoWriter("videos/cam_video.mp4", vid_cod, 20.0, (640, 480))

# while True:
#    # Capture each frame of webcam video
#    ret, frame = vid_capture.read()
#    cv2.imshow("My cam video", frame)
#    output.write(frame)
#    # Close and break the loop after pressing "x" key
#    if cv2.waitKey(1) & 0xFF == ord("x"):
#        break

# close the already opened camera
# vid_capture.release()
# close the already opened file
# output.release()
# close the window and de-allocate any associated memory usage
# cv2.destroyAllWindows()
