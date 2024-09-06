from nmap import PortScanner


nmp = PortScanner()

def osScanner(ip, timeout="10s"):
    try:
        scanning = nmp.scan(ip, arguments=f'-O --host-timeout {timeout}')
        result = scanning['scan'][ip]['osmatch'][0]['osclass'][0]
        os_detect = result['osfamily']
        osgen = result['osgen']
        print("đã tìm thấy một IP")
        return os_detect.strip().lower(), osgen.strip().lower()
    except Exception as e:
        return 0, 0
