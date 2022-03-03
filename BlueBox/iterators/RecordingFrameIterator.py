import queue

from vidgear.gears import WriteGear
from threading import Thread
from vidgear.gears import CamGear

# This is a custom class that iterates through frames and records
class RecordingFrameIterator:
    def __init__(self, source=0, name="Unnamed"):
        self.source = CamGear(source=source)
        self.running = True

        # Construct a writer
        writeGearOptions = {
            "-c:v": "libx264",
            "-crf": 22,
            "-map": 0,
            "-segment_time": 20,
            "-r": 60,
            "-g": 9,
            "-sc_threshold": 0,
            "-force_key_frames": "expr:gte(t,n_forced*9)",
            "-clones": ["-f", "segment"],
        }

        self.writer = WriteGear(
            output_filename=f"/var/BlueBox/{name}-%03d.mp4",
            **writeGearOptions,
        )

        self.queue = queue.Queue(maxsize=128)  # max bufferlen 96 to check overflow
        self.thread = None

    def main_iterator(self):
        self.source.start()
        while self.running:
            frame = self.source.read()
            if frame is None:
                self.running = False
            else:
                self.writer.write(frame)
                if not self.queue.full():
                    self.queue.put(frame)

    def start(self):
        if self.thread is None:
            self.thread = Thread(target=self.main_iterator)
            self.thread.daemon = True
            self.thread.start()
        return self

    def read(self):
        if self.running or not self.queue.empty():
            return self.queue.get()
        else:
            return None

    def stop(self):
        self.running = False
        self.source.stop()
        if not (self.thread is None):
            self.thread.join()
        self.writer.close()
