from abc import abstractmethod
from media import MediaInfo, MediaControl
import subprocess


class Player(MediaControl, MediaInfo):

    CHUNK = 2048
    SLEEP_TIME = 0.035
    stream = None
    event = None    # TODO: maybe delete?
    _tmp_stream = None

    @abstractmethod
    def playback_position(self):
        pass

    def silence(self, silence_time=0.8):
        self._tmp_stream = self.stream.stdout
        self.stream.stdout = subprocess.Popen(["sox", "-n", "-r", "48000", "-b", "16", "-c", "1", "-t", "wav", "-",
                                               "trim", "0", str(silence_time)],
                                              stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout
