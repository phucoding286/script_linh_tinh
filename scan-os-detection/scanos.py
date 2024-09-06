import threading
from __autoScan import autoScan
import time

for file_path in ['ip_analysis.txt', 'log.txt', 'targets.txt']:
    with open(file_path, "a"): pass

def autoScanMultiprocess(num_threads=5, os_detect_list=['windows'], osgen_list=['2000', '2003', 'xp', '7'],
    file_path='targets.txt', analysis_path="ip_analysis.txt", log_path='log.txt', timeout='120s'):
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=autoScan, args=[os_detect_list, osgen_list, file_path, analysis_path, log_path, timeout])
        threads.append(thread)
        thread.start()
        time.sleep(0.1)
    for t in threads:
        t.join()
    
if __name__ == "__main__":
    while True:
        autoScanMultiprocess(100, osgen_list=['2000', '2003', 'xp', '7', '2008'])
