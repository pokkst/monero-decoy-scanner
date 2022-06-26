#!/usr/bin/python3

import sys
import requests
import json
from dataclasses import dataclass

@dataclass
class RingMember:
    idx: int
    tx_hash: str

ringct_start = 1220516
existing_txs = []

#UPDATE THIS TO WATCH FOR DESIRED OUTPUTS
outputs_to_watch = [00000000, 00000000, 00000000, 00000000, 00000000]

def get_transactions(tx_hashes):
    PARAMS = {'txs_hashes' : tx_hashes, 'decode_as_json' : True}
    transactions = call_rpc("get_transactions", PARAMS)
    if 'txs' in transactions.json():
        return transactions.json()['txs']
    else:
        return []

def get_idx(key_offset_index, key_offsets):
    idx = 0
    i = 0
    while i <= key_offset_index:
        idx += key_offsets[i]
        i += 1
    return idx

def find_any_ring_members(transactions, outputs_to_watch):
    decoys = []
    for t in transactions:
        tx = json.loads(t['as_json'])
        inputs = tx['vin']
        for i in inputs:
            input = i['key']
            key_offsets = input['key_offsets']
            o = 0
            for o1 in key_offsets:
                idx = get_idx(o, key_offsets)
                o += 1
                if idx in outputs_to_watch:
                    decoys += [RingMember(idx, t['tx_hash'])]
    return decoys

def get_block(block_hash):
    PARAMS = { "hash": block_hash }
    block = call_json_rpc("get_block", PARAMS).json()
    return block

def get_block_by_height(block_height):
    PARAMS = { "height": block_height }
    block = call_json_rpc("get_block", PARAMS).json()
    return block

def get_height():
    PARAMS = {}
    height = call_rpc("get_height", PARAMS).json()
    return height['height'] - 1

def call_rpc(method_name, params):
    response = requests.post("http://localhost:18081/" + method_name, json = params)
    return response

def call_json_rpc(method_name, params):
    PARAMS = {'jsonrpc':'2.0', 'id':'0', 'method': method_name, 'params': params, 'decode_as_json' : True}
    response = requests.post("http://localhost:18081/json_rpc", json = PARAMS)
    return response

def record_any_transactions(block):
    tx_hashes_json = json.loads(block['result']['json'])
    tx_hashes = tx_hashes_json['tx_hashes']
    transactions = get_transactions(tx_hashes)
    ring_members = find_any_ring_members(transactions, outputs_to_watch)
    for ring_member in ring_members:
        maybe_record_ring_member(ring_member)

def maybe_record_ring_member(ring_member):
    found = False
    if ring_member.tx_hash in existing_txs:
        found = True

    if not found:
        f = open('decoys.txt', 'a')
        f.write(ring_member.idx.__str__() + ": " + ring_member.tx_hash+"\n")
        f.close()

def load_previous_txs():
    temp_txs = []
    f = open('decoys.txt', 'r')
    txs = f.readlines()
    f.close()
    for line in txs:
        tx_hash = line.split(": ")[1].rstrip()
        temp_txs += [tx_hash]
    return temp_txs

existing_txs = load_previous_txs()
