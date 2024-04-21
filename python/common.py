import time, os

python_folder = os.path.dirname(__file__)
root_folder = os.path.dirname(python_folder)

OUTPUT_PATH = os.path.join(root_folder,"outputs.txt")

MEASUREMENTS_PATH = os.path.join(root_folder,"measurements.txt")

class Timer:
    def __init__(self):
        self.start = time.time()
        
    def elapsed_as_milliseconds(self):
        return (time.time() - self.start) * 1000