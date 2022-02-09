import uvicorn
from vidgear.gears.asyncio import WebGear
from vidgear.gears import CamGear
from vidgear.gears import VideoGear

import threading


class LocalStreamer(threading.Thread):
    """
    Each local camera should have a LocalStreamer
    dedicated to it. This thread should handle reconnecting
    if the camera goes dead, as well as transcoding, and serving
    the camera via mjpeg.
    """

    def __init__(self, camID, BlueBoxTable):
        threading.Thread.__init__(self)

        # This camera's cam ID
        self.camID = camID

        # The passed instance of nt from main thread
        self.BlueBoxTable = BlueBoxTable

        # Setup a camgear, to handle capturing this cam
        # self.Camera = CamGear(source=0, logging=True).start()

        self.options = {
            "frame_size_reduction": 40,
            "jpeg_compression_quality": 80,
            "jpeg_compression_fastdct": True,
            "jpeg_compression_fastupsample": False,
            "custom_data_location": "BlueBox/www/",
        }

        self.web = WebGear(source=0, logging=True, **self.options)

        self.BlueBoxTable.putNumber(f"CamStream{camID}", 1)

    def run(self):
        uvicorn.run(self.web(), host="localhost", port=8000)

    def terminate(self):
        self.web.shutdown()
        self.Camera.stop()
