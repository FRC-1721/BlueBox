import imp
import cv2
import queue
import asyncio
import uvicorn
import threading

from vidgear.gears import WriteGear
from threading import Thread
from vidgear.gears.asyncio.helper import reducer
from vidgear.gears.asyncio import WebGear
from vidgear.gears import CamGear

from iterators.RecordingFrameIterator import RecordingFrameIterator


class LocalCamera(threading.Thread):
    """
    Each local camera should have a LocalStreamer
    dedicated to it. This thread should handle reconnecting
    if the camera goes dead, as well as transcoding, and serving
    the camera via mjpeg.
    """

    def __init__(self, data, BlueBoxTable):
        threading.Thread.__init__(self)

        # This camera's cam ID
        self.camID = int(data["id"])

        # The passed instance of nt from main thread
        self.BlueBoxTable = BlueBoxTable

        self.webGearOptions = {
            "frame_size_reduction": 40,
            "jpeg_compression_quality": 80,
            "jpeg_compression_fastdct": True,
            "jpeg_compression_fastupsample": False,
            "custom_data_location": "BlueBox/www/",
        }

        # Setup blank WebGear
        self.web = WebGear(logging=True, **self.webGearOptions)

        self.web.config["generator"] = self.frame_producer

        self.BlueBoxTable.putNumber(data["name"], 1)

    async def frame_producer(self):
        # !!! define your own video source and output video filename here!!!
        # open any valid video stream(for e.g `myvideo.mp4` file)
        self.stream = RecordingFrameIterator(name="myoutput.mp4").start()
        # loop over frames
        while True:
            # read frames from stream
            frame = self.stream.read()

            # check for frame if Nonetype
            if frame is None:
                break

            # {do something with your OpenCV frame here}
            # reducer frames size if you want more performance otherwise comment this line
            frame = await reducer(frame, percentage=30, interpolation=cv2.INTER_AREA)

            # handle JPEG encoding
            encodedImage = cv2.imencode(".jpg", frame)[1].tobytes()
            # yield frame in byte format
            yield (
                b"--frame\r\nContent-Type:image/jpeg\r\n\r\n" + encodedImage + b"\r\n"
            )
            await asyncio.sleep(0)
        # safely close video stream
        self.stream.stop()

    def run(self):
        uvicorn.run(self.web(), host="0.0.0.0", port=5801)

    def terminate(self):
        self.writer.close()
        self.web.shutdown()
        self.Camera.stop()
