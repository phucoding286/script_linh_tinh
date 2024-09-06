from __checkLiveProxy import CheckLiveProxy
from __proxiesFinding import ProxyFinding
import threading
import time

class FindCheckProxy(CheckLiveProxy, ProxyFinding):

    def __init__(self, path_saveProxy="./proxiesLive.txt", verbose=True, protocol='http',
                url="https://gimmeproxy.com/api/getProxy"):
        CheckLiveProxy.__init__(self, path_saveProxy=path_saveProxy, verbose=verbose, protocol=protocol)
        ProxyFinding.__init__(self, url=url)

    def find_proxiesLive(self):
        proxy_finded = self.get_proxy()
        self.check_liveProxy(proxy_finded)
    
    def multi_process(self, thr=10):
        while True:

            threads = []
            for _ in range(thr):
                thread = threading.Thread(target=self.find_proxiesLive)
                threads.append(thread)
                thread.start()
                time.sleep(0.01)
            
            for t in threads:
                t.join()

if __name__ == "__main__":
    fpy = FindCheckProxy()
    while True:
        try:
            inp_thr = int(input("nhập số luồng: "))
            break
        except:
            print("vui lòng nhập số luồng")
            continue
    fpy.multi_process(inp_thr)