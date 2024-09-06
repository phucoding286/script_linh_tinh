from whois import whois
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
import requests 
from bs4 import BeautifulSoup
import os
import threading

class GetDomainInfo:
    def __init__(self, tlds=["net", "com"]):
        self.tlds = tlds

    def domain_information(self, domain):
        try:
            domain_infomations = whois(domain)
        except:
            return "error"
        
        keys = ["domain_name", "registrar", "whois_server", "referral_url", "updated_date", "creation_date",
                "expiration_date", "name_servers", "status", "emails", "dnssec", "name", "org", "address",
                "city", "state", "registrant_postal_code", "country"]
        update_domain_infomation = ""
        for key in keys:
            update_domain_infomation += str(f"{domain_infomations[key]}, ")
        for tld in self.tlds:
            if domain.split(".")[1] in tld:
                update_domain_infomation = update_domain_infomation+tld
                break
        return update_domain_infomation

class PredictDomain:
    def __init__(self, path_train="train_v2.txt"):
        self.path_train = path_train
    
    def read_train(self):
        X_train, y_train = [], []
        with open(self.path_train, "r", encoding="utf-8") as file:
            data = file.read().splitlines()
            for info in data:
                X_train.append(info.split(" - ")[0])
                y_train.append(info.split(" - ")[1])
        return [X_train], y_train
    
    def predict(self, domain):
        domain_info = GetDomainInfo().domain_information(domain=domain)
        X_train, y_train = self.read_train()
        bow_transformer = CountVectorizer(analyzer="char")
        X_train = bow_transformer.fit_transform(X_train[0]).toarray()
        desicion_tree = DecisionTreeClassifier()
        random_forest = RandomForestClassifier()
        bayes_model = GaussianNB()
        svm_model = SVC(probability=True)
        knn_model = KNeighborsClassifier(n_neighbors=3)
        voting_model = VotingClassifier(estimators=[("desicion tree", desicion_tree),
                                                    ("random forest", random_forest),
                                                    ("svm", svm_model),
                                                    ("knn", knn_model),
                                                    ("bayes", bayes_model)], voting="soft")
        voting_model.fit(X_train, y_train)
        X_test = bow_transformer.transform([domain_info]).toarray()
        predict = voting_model.predict(X_test)
        return predict[0]

tdls = ["net", "com"]
for file_path in ["log_v2.txt", "saved_v2.txt"]:
    if not os.path.exists(file_path):
        print(f"tệp {file_path} chưa có tiến hành tạo.")
        with open(file_path, "a", encoding='utf8') as f:
            pass

def get_domain():
    while True:
        try:
            email_request = requests.get(url="https://emailfake.com/fake_email_generator")
            break
        except:
            continue
    soup = BeautifulSoup(email_request.text, "html.parser")
    domain_html = str(soup.find_all("input"))
    domain = domain_html.split('value="')[-1].split('"/>]')[0]
    return domain

def check_log(domain: str):
    with open("log_v2.txt", "r", encoding="utf-8") as f:
        domains = f.read()
    if domain in domains.splitlines():
        print(f"tên miền {domain} có trong log!")
        return 0
    else:
        print(f"tên miền mới {domain}")
        return 1

def check_tlds(domain: str):
    if domain.split(".")[1].strip() not in tdls:
        print(f"đuôi tên miền {domain} không thuộc vùng tên miền đã train: {tdls} nên sẽ được bỏ qua")
        return 0
    else:
        print(f"đuôi tên miền {domain} nằm trong vùng hợp lệ: {tdls}")
        return 1

def check_up_time(domain: str, day_limit=7):
    url = 'https://emailfake.com/check_adres_validation3.php'
    data = {
        'usr': 'charleswhatmore',
        'dmn': domain
    }
    while True:
        try:
            response = requests.post(url, data=data)
            break
        except:
            continue
    result = response.json()
    day = result["uptime"]
    if int(day) > day_limit:
        print(f"số ngày đăng tên miền {domain} quá lớn so với mức quy định {day_limit} nên bỏ qua!")
        return 0
    else:
        print(f"tên miền {domain} có số ngày đã đúng mức quy định {day_limit}!!")
        return 1

def predict_domain():
    domain = get_domain()
    if check_log(domain) == 0:
        return 0
    if check_tlds(domain) == 0:
        return 0
    if check_up_time(domain) == 0:
        return 0
    try:
        predict = PredictDomain("train_v2.txt").predict(domain)
    except Exception as error:
        print(f"có 1 chút lỗi ở phần dự đoán nên chạy lại mã lỗi là: {error}")
        return 0
    if str(predict) in '1':
        with open("saved_v2.txt", "a", encoding='utf8') as f:
            f.write(f"{domain}\n")
        with open("log_v2.txt", "a", encoding="utf8") as f:
            f.write(f"{domain}\n")
        print(f"domain {domain} có vẻ ngon nên đã lưu lại.")
        print(f"và đã lưu domain {domain} vào log")
    else:
        print(f"đã lưu domain {domain} vào log")
        with open("log_v2.txt", "a", encoding="utf8") as f:
            f.write(f"{domain}\n")

def run_script(c=50):
    threads = []
    for _ in range(c):
        thread = threading.Thread(target=predict_domain)
        thread.start()
        threads.append(thread)
    for t in threads:
        t.join()
        
if __name__ == "__main__":
    print("*BETA version")
    print("*Công cụ AI phân tích tên miền Domain-FU thế hệ thứ 2 với các cập nhật về tốc độ tìm kiếm và dự đoán tên miền ^_+")
    print("-For CloudSigma Service-")
    c = False
    while True:
        if c is False:
            try:
                inp_t = int(input("nhập số luồng của bạn: ").strip())
                c = True
            except:
                print("vui lòng nhập số nguyên (số luồng)")
                continue
        run_script(inp_t)