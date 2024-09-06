from __randomIP import randomIP
from __osScanner import osScanner

def autoScan(os_detect_list=['windows'], osgen_list=['2000', '2003', 'xp', '7'],
    file_path='targets.txt', analysis_path="ip_analysis.txt", log_path='log.txt', timeout='120s'):
    ip = randomIP()
    os_detect, osgen = osScanner(ip, timeout)
    if os_detect in os_detect_list and osgen in osgen_list:
        print(f"hệ điều hành: {os_detect} phiên bản: {osgen} IP {ip} hợp lệ")
        with open(analysis_path, 'a', encoding='utf8') as f:
            f.write(f"ip: {ip} os: {os_detect} osgen: {osgen}\n")
        with open(file_path, 'a', encoding='utf8') as f:
            f.write(f"{ip}\n")
        with open(log_path, 'a', encoding='utf8') as f:
            f.write(ip+"\n")

    else:
        print(f"IP {ip} không hợp lệ")
        with open(log_path, 'a', encoding='utf8') as f:
            f.write(ip+"\n")
