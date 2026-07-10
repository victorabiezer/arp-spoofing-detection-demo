#!/usr/bin/env python3
"""
dashboard server: csci4345 network application project
purpose: watches the arp detector's log file and streams new entries
to the browser dashboard live, using server-sent events (sse)
"""

from flask import Flask, Response
from flask_cors import CORS
import time
import os

app = Flask(__name__)
CORS(app)

LOG_FILE = "/home/ubuntu/arp_log.jsonl"

def tail_log():
    # this generator function keeps checking the log file for new lines
    # and sends them out the moment they appear, kind of like "tail -f" in bash
    last_position = 0

    # if the log file doesn't exist yet, wait for the detector to create it
    while not os.path.exists(LOG_FILE):
        time.sleep(0.5)

    while True:
        with open(LOG_FILE, "r") as f:
            f.seek(last_position)
            new_lines = f.readlines()
            last_position = f.tell()

        for line in new_lines:
            # sse format requires each message to start with "data: "
            yield f"data: {line.strip()}\n\n"

        time.sleep(0.5)  # check for new lines twice a second

@app.route("/stream")
def stream():
    # this is the live connection the dashboard will hook into
    return Response(tail_log(), mimetype="text/event-stream")

@app.route("/")
def home():
    return "arp dashboard server is running, connect the html dashboard to /stream"

if __name__ == "__main__":
    print("[*] dashboard server starting on http://192.168.125.23:5000")
    app.run(host="0.0.0.0", port=5000)
