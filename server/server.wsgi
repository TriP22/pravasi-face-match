#!/usr/bin/python3
import sys
import os

activate_this = '/home/ubuntu/pravasi-face-match/server/venv/bin/activate'
with open(activate_this) as file_:
    print(file_)
    print(exec(file_.read(), dict(__file__=activate_this)))

sys.path.insert(0, '/home/ubuntu/pravasi-face-match/server')

from server import app as application