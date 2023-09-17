#!/usr/bin/env python

import subprocess
import time
import os

def flash_image():
    os.chdir("/usr/lib/enigma2/python/Plugins/Extensions/GPT-Boot-Plugin")
    subprocess.call(["./boot.sh", "-b", "3"])
    time.sleep(1)
    subprocess.call(["reboot"])

if __name__ == "__main__":
    flash_image()