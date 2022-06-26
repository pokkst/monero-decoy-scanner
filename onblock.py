#!/usr/bin/python3

from utils import *

height = get_height()
should_lookback = height % 20 == 0
if should_lookback:
    lookback_height = height - 19
    while height >= lookback_height:
        block = get_block_by_height(height)
        record_any_transactions(block)
        height -= 1

block_hash = sys.argv[1]

block = get_block(block_hash)
record_any_transactions(block)
