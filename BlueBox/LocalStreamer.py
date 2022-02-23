import uvicorn
from vidgear.gears.asyncio import WebGear
from vidgear.gears import CamGear
from vidgear.gears import VideoGear

# import necessary libs
import uvicorn, asyncio, cv2
from vidgear.gears import WriteGear
from vidgear.gears.asyncio.helper import reducer

import threading


class LocalStreamer(threading.Thread):
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

        writeGearOptions = {
            "-c:v": "libx264",
            "-crf": 22,
            "-map": 0,
            "-segment_time": data["segment_time"],
            "-r": 29.9,
            "-g": 9,
            "-sc_threshold": 0,
            "-force_key_frames": "expr:gte(t,n_forced*9)",
            "-clones": ["-f", "segment"],
        }

        # Setup blank WebGear
        self.web = WebGear(logging=True, **self.webGearOptions)

        self.web.config["generator"] = self.frame_producer

        self.writer = WriteGear(
            output_filename="/var/bluebox/output%03d.mp4",
            logging=True,
            **writeGearOptions,
        )

        self.BlueBoxTable.putNumber(data["name"], 1)

        self.cameraStream = CamGear(
            source=0,
            logging=True,
        ).start()

    async def frame_producer(self):

        while True:
            # Read frames
            frame = self.cameraStream.read()

            # Break if bad or no frame
            if frame is None:
                break

            # Write full size frame
            self.writer.write(frame)

            # Use reducer to compress frame
            frame = await reducer(frame, percentage=30, interpolation=cv2.INTER_AREA)

            # handle JPEG encoding
            encodedImage = cv2.imencode(".jpg", frame)[1].tobytes()
            # yield frame in byte format
            yield (
                b"--frame\r\nContent-Type:image/jpeg\r\n\r\n" + encodedImage + b"\r\n"
            )
            await asyncio.sleep(0)
        # safely close video stream
        stream.stop()

    def run(self):
        uvicorn.run(self.web(), host="0.0.0.0", port=5801)

    def terminate(self):
        self.writer.close()
        self.web.shutdown()
        self.Camera.stop()
