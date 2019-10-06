import os

splash = '''
████████▄     ▄████████     ███        ▄████████    ▄█    █▄     ▄██████▄  ███    █▄  ███▄▄▄▄   ████████▄  
███   ▀███   ███    ███ ▀█████████▄   ███    ███   ███    ███   ███    ███ ███    ███ ███▀▀▀██▄ ███   ▀███ 
███    ███   ███    ███    ▀███▀▀██   ███    ███   ███    ███   ███    ███ ███    ███ ███   ███ ███    ███ 
███    ███   ███    ███     ███   ▀   ███    ███  ▄███▄▄▄▄███▄▄ ███    ███ ███    ███ ███   ███ ███    ███ 
███    ███ ▀███████████     ███     ▀███████████ ▀▀███▀▀▀▀███▀  ███    ███ ███    ███ ███   ███ ███    ███ 
███    ███   ███    ███     ███       ███    ███   ███    ███   ███    ███ ███    ███ ███   ███ ███    ███ 
███   ▄███   ███    ███     ███       ███    ███   ███    ███   ███    ███ ███    ███ ███   ███ ███   ▄███ 
████████▀    ███    █▀     ▄████▀     ███    █▀    ███    █▀     ▀██████▀  ████████▀   ▀█   █▀  ████████▀                                                                                                                                                                                                                       ███▀   ▀█   █▀  ████████▀                                                                                                                                                                    
'''

def PrintTitle():
        if os.name == 'nt':
                print(splash)
        else:
                print('\033[1;32m[+]\033[1;m ' + splash)
def PrintSuccess(Msg):
        if os.name == 'nt':
                print('[+] ' + Msg)
        else:
                print('\033[1;32m[+]\033[1;m ' + Msg)

def PrintStatus(Msg):
        if os.name == 'nt':
                print('[*] ' + Msg)
        else:
                print('\033[1;34m[*]\033[1;m ' + Msg)

def PrintFailure(Msg):
        if os.name == 'nt':
                print('[-] ' + Msg)
        else:
                print('\033[1;31m[-]\033[1;m ' + Msg)

def PrintError(Msg):
        if os.name == 'nt':
                print('[!] ' + Msg)
        else:
                print('\033[1;31m[!]\033[1;m ' + Msg)

def PrintFileMatch(Msg):
        if os.name == 'nt':
                print('[$] ' + Msg)
        else:
                print('\033[1;33m[!]\033[1;m ' + Msg)

def DoNothing():
        pass                                    
