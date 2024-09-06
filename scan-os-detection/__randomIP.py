import random
from ping3 import ping

def randomIP(log_path='log.txt'):
    with open(log_path, 'r', encoding='utf8') as f:
        logs = f.read().splitlines()
    while True:
        g1 = str(random.choice([i for i in range(253)]))
        g2 = str(random.choice([i for i in range(253)]))
        g3 = str(random.choice([i for i in range(253)]))
        g4 = str(random.choice([i for i in range(253)]))
        if g1 in "127": g1 = "128"
        ip = f"{g1}.{g2}.{g3}.{g4}"
        try:
            if ping(ip, timeout=1) is None: continue
        except: continue
        if ip not in logs: break
    return ip
