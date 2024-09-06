import requests

class ProxyFinding:

    def __init__(self, url="https://gimmeproxy.com/api/getProxy"):
        self.url = url
    

    def get_proxy(self):
        while True:
            try:
                response = requests.get(self.url)
                proxy = response.json()['curl']

                break
            except Exception as e:
                print("lỗi ở phần get proxy:", e)
                continue
        return proxy