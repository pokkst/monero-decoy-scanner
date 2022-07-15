#!/usr/bin/python3

import glob, os, requests, json
from bs4 import BeautifulSoup

get_in = True
get_out = True
explorer = "https://xmrchain.net"
history = []

def get_tor_session():
    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http':  'socks5h://127.0.0.1:9050',
                       'https': 'socks5h://127.0.0.1:9050'}
    return session

def get_history():
    for file in glob.glob("*.csv"):
        with open(file,"r") as f:
            lines = f.read().splitlines()
        for line in lines:
            direction = line.split(",")[3]
            txid = line.split(",")[7]
            if direction == "in" and get_in == True:
                history.append(txid)
                continue
            if direction == "out" and get_out == True:
                history.append(txid)
    if history:
        print(f"number of txids found: {len(history)}")
        return history
    else:
        print("no txids / .csv file found")

def dump_output_list(history):
    global explorer
    outputs = []
    r = get_tor_session()
    counter = 1
    print("Getting Amount idx for outputs")
    for tx_id in history:
        try:
            data = r.get(f"{explorer}/search?value={tx_id}")
            soup = BeautifulSoup(data.content, 'html.parser')
            tables = soup.findAll("table")

            for table in tables[1].findAll("td"):
                if "of" in table.text:
                    output = table.text.split("of")[0].strip()
                    outputs.append(output)
            print(f"{counter}/{len(history)}")
            counter += 1
        except:
            print("Error: is tor running? (start tor browser)")

    if outputs:
        with open('output_list.json', 'w+') as f:
            json.dump(outputs, f)

def main():
    dump_output_list(get_history())

if __name__ == "__main__":
    main()
