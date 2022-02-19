# FRC 1721
# 2022

import time
import yaml
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

        self.const = self.getConstants()

        # Setup colored logs
        coloredlogs.install(level="DEBUG")

        # Initialize networktables
        NetworkTables.initialize(server="localhost")
        sd = NetworkTables.getTable("SmartDashboard")
        self.BlueBoxTable = sd.getSubTable("BlueBox")

        # Each camera should have its own threaded handler.
        # This is messy, maybe look at python multiprocessing?
        self.RearFisheyeThread = LocalStreamer(
            self.const["streams"]["rearfisheye"],
            self.BlueBoxTable,
        )

    def run(self):
        self.RearFisheyeThread.start()
        # self.thread2.start()

        try:
            while True:
                # logging.debug("Mainloop is waiting...")

                # self.BlueBoxTable.putNumber("Epoch", int(time.time()))
                otherNumber = self.BlueBoxTable.getNumber("otherNumber", 0)

                time.sleep(1)
        except KeyboardInterrupt:
            self.RearFisheyeThread.join()
            quit()

    def getConstants(self):
        constants = {}

        try:
            # Try opening requested .yaml
            with open("config.yaml", "r") as yamlFile:
                # Use yaml.safe_load to load the yaml into a dict
                constants = yaml.safe_load(yamlFile)
        except FileNotFoundError as e:
            # If the file is not found, report it!
            logging.error("Config not found!")
            raise e

        # When all is done, return the important bits!
        return constants
