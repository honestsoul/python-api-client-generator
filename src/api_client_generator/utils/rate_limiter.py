# api_client_generator/utils/rate_limiter.py

import time
from threading import Lock

class RateLimiter:
    def __init__(self, calls: int, period: float):
        self.calls = calls
        self.period = period
        self.timestamps = []
        self.lock = Lock()

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            with self.lock:
                now = time.time()
                
                # Remove timestamps older than the period
                self.timestamps = [t for t in self.timestamps if now - t <= self.period]
                
                if len(self.timestamps) >= self.calls:
                    sleep_time = self.period - (now - self.timestamps[0])
                    if sleep_time > 0:
                        time.sleep(sleep_time)
                
                self.timestamps.append(time.time())
            
            return func(*args, **kwargs)
        return wrapper

# Usage:
# @RateLimiter(calls=100, period=60)
# def make_api_call():
#     # Your API call here
#     pass