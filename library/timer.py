import time
import math


class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""


class Timer:
    def __init__(self):
        self._start_time = None
        self._elapsed_time = None

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()
        self._elapsed_time = None

    def stop(self):
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        self._elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None

    def elapsed(self):
        if self._elapsed_time is not None:
            return self._elapsed_time

        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        return time.perf_counter() - self._start_time

    def elapsed_formatted(self):
        elapsed_seconds = self.elapsed()
        if elapsed_seconds < 60:
            return f"{elapsed_seconds:0.2f}s"
        elif elapsed_seconds < 3600:
            minutes = math.floor(elapsed_seconds / 60)
            seconds = elapsed_seconds % 60
            return f"{minutes}m {seconds:0.2f}s"
        else:
            hours = math.floor(elapsed_seconds / 3600)

            hour_seconds = hours * 3600
            minutes = math.floor((elapsed_seconds - hour_seconds) / 60)

            minute_seconds = minutes * 60
            seconds = (elapsed_seconds - hour_seconds - minute_seconds) % 60
            return f"{hours}h {minutes}m {seconds:0.2f}s"
