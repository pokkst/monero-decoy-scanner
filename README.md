# WARNING
This repository is no longer maintained. Please see the latest changes here:
http://4hsesnr6mjb4qrflgf5gezjaszzoqnnisin7ywzbsv6pgcxysiaq.b32.i2p/pokkst/monero-decoy-scanner

To access, please install I2P: https://geti2p.net and configure your browser's proxy settings to use an HTTP proxy at 127.0.0.1:4444.

# monero-decoy-scanner
Listens to the chain for transactions that use certain outputs as decoy ring members.

## Setup

Setup is quite simple. You will need Python 3 and a monerod instance.

It should be noted that not all transactions found with an output as a ring member mean the output was a decoy. Some transactions for a list of outputs could very much be real spends, but due to the untraceable nature of XMR, it is extremely difficult to determine whether or not any given transaction is a real spend, if it has even been spent at all.

Run monerod with `block-notify` set. As per Monero documentation, the argument needs full paths.

```./monerod --block-notify="/usr/bin/python /path/to/onblock.py %s"```

The list of outputs to watch for can be configured in utils.py by changing the following line:

```outputs_to_watch = [00000000, 00000000, 00000000, 00000000, 00000000]```

The integers are the output indices. If you need to get the index of an output, look up the transaction on https://xmrchain.net and copy the "amount idx" number before the "of xxxxxxx" text.

Transactions detected are stored in decoys.txt in your monerod install location with the following format:

```output_index: transaction_hash```

The repository also comes with `fullscan.py`. This script starts at a configured block height (by default it is the height where RingCT started, but it can be changed) and iterates through all blocks until it reaches the chain height. It can be executed with:

```python fullscan.py```

It is not recommended to use this as the script to run for --block-notify.
