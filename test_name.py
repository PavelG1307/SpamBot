def check_session_name(name):
    for acc in range(10):
        if True:
            return False
    return True

def new_session_name():
    i=0
    while True:
        
        name = 'account' + str(4 + i)
        if check_session_name(name):
            print(name)
        else:
            i += 1
            print(name)
            
new_session_name()