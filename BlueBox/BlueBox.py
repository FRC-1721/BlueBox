# FRC 1721
# 2022

import time
import coloredlogs, logging
from networktables import NetworkTables

from LocalStreamer import LocalStreamer


class BlueBox:
    def __init__(self):
        """
        Construct a BlueBox instance
        """

        # Get logger
        self.logger = logging.getLogger(__name__)

        # Setup colored logs
        coloredlogs.install(level="DEBUG")

        # Initialize networktables
        NetworkTables.initialize(server="localhost")
        sd = NetworkTables.getTable("SmartDashboard")
        self.BlueBoxTable = sd.getSubTable("BlueBox")

        # Each camera should have its own threaded handler.
        self.CameraThread0 = LocalStreamer(0, self.BlueBoxTable)
        # self.thread2 = CameraThread(4)

    def run(self):
        self.CameraThread0.start()
        # self.thread2.start()

        try:
            while True:
                logging.debug("Mainloop is waiting...")

                # self.BlueBoxTable.putNumber("Epoch", int(time.time()))
                otherNumber = self.BlueBoxTable.getNumber("otherNumber", 0)

                time.sleep(1)
        except KeyboardInterrupt:
            self.CameraThread0.join()
            quit()
