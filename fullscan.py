#!/usr/bin/python3

from utils import *
import threading
from dataclasses import dataclass

height = get_height()
remaining = height - ringct_start
threads = 4
split = int(remaining / threads)

class ScanThread (threading.Thread):
   def __init__(self, start_height):
      threading.Thread.__init__(self)
      self.start_height = start_height
   def run(self):
      scan_blocks(self.start_height)

def scan_blocks(start_height):
    end_height = start_height + split
    current_height = start_height
    while current_height < end_height:
        block = get_block_by_height(current_height)
        record_any_transactions(block)
        current_height += 1
    print("End thread.")

current_thread = 0
while current_thread < threads:
    try:
        start_height = ringct_start + (split * current_thread)
        scan_thread = ScanThread(start_height)
        scan_thread.start()
    except:
        print("Error: unable to start thread")
    current_thread += 1
