import os

DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(DIR, 'VERSION')) as fs:
    __version__ = fs.read().strip()
