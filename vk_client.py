import vk
from storage import Storage as S
s = S()

try:
    token = s.token()
except:
    token = input('Enter a valid token: ')
    s.update_token(token)

session = vk.Session(access_token=token)
api = vk.API(session)

def does_have_new_messages():
    dialogs = api.messages.getDialogs()
    for dialog in dialogs[1:]:
        if 'push_settings' in dialog and dialog['push_settings']['sound'] == 0:
            continue
        if not dialog['read_state'] and dialog['out'] == 0:
            return True
    return False
