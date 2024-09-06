import requests


class CheckLiveProxy:

    def __init__(self, path_saveProxy="./proxiesLive.txt", verbose=True, protocol='http'):
        self.google_url = "https://www.google.com"
        self.proxies = {"http:": ""}
        self.path_saveProxy = path_saveProxy
        self.verbose = verbose
        self.protocol = protocol
    
    def check_liveProxy(self, proxy: str):
        if proxy.split(":")[0] == self.protocol:
            self.proxies['http'] = proxy
        else:
            return 0
        
        try:

            response = requests.get(url=self.google_url, proxies=self.proxies)

            if response.status_code == 200:
                with open(self.path_saveProxy, "a", encoding='utf-8') as f:
                    f.write(proxy+"\n")

                if self.verbose:
                    print("Proxy "+proxy+" sống")
            
            else:
                if self.verbose:
                    print("Proxy "+proxy+" không hoạt động")
        
        except requests.exceptions.RequestException as e:
            print("Proxy đã chết:", e)