import math
from whois import whois
import requests
from bs4 import BeautifulSoup
import os
import threading


class GetDomainInfo:
    def __init__(self, tlds=["net", "com"]):
        self.tlds = tlds

    def domain_information(self, domain):
        try:
            domain_infomations = whois(domain.strip())
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

# Dữ liệu
with open("train_v2.txt", "r", encoding="utf-8") as file:
    batch = file.read().splitlines()
data = []
labels = []  # Nhãn tương ứng: 0 - negative, 1 - positive
for lines in batch:
    data.append(lines.split(' - ')[0])
    labels.append(int(lines.split(' - ')[-1]))

# Hàm tạo Bag of Words và từ điển
def create_bow(data):
    bow = []
    vocab = {}
    for sentence in data:
        words = sentence.split()
        bow_sentence = {}
        for word in words:
            if word not in vocab:
                vocab[word] = len(vocab)
            word_idx = vocab[word]
            if word_idx in bow_sentence:
                bow_sentence[word_idx] += 1
            else:
                bow_sentence[word_idx] = 1
        bow.append(bow_sentence)
    return bow, vocab

# Tạo Bag of Words và từ điển từ dữ liệu
bow, vocab = create_bow(data)

# Huấn luyện mô hình Logistic Regression
def train_logistic_regression(bow, labels, vocab):
    vocab_size = len(vocab)
    num_sentences = len(bow)
    weights = [0.0] * vocab_size
    bias = 0.0
    learning_rate = 0.01
    epochs = 100

    for epoch in range(epochs):
        for i in range(num_sentences):
            # Tính toán đầu ra dự đoán
            score = 0.0
            for word_idx, count in bow[i].items():
                score += weights[word_idx] * count
            score += bias

            # Áp dụng hàm sigmoid
            predicted = 1.0 / (1.0 + math.exp(-score))

            # Tính gradient dựa trên cross-entropy loss
            error = predicted - labels[i]
            for word_idx, count in bow[i].items():
                gradient = error * count
                weights[word_idx] -= learning_rate * gradient
            bias -= learning_rate * error

    return weights, bias

# Huấn luyện mô hình
weights, bias = train_logistic_regression(bow, labels, vocab)

# Dự đoán trên dữ liệu mới
def predict_new_data(new_data, weights, bias, vocab):
    predictions = []
    for sentence in new_data:
        bow_sentence = {}
        words = sentence.split()
        for word in words:
            if word in vocab:
                word_idx = vocab[word]
                if word_idx in bow_sentence:
                    bow_sentence[word_idx] += 1
                else:
                    bow_sentence[word_idx] = 1
        score = 0.0
        for word_idx, count in bow_sentence.items():
            score += weights[word_idx] * count
        score += bias
        predicted = 1.0 / (1.0 + math.exp(-score))
        if predicted >= 0.5:
            predictions.append(1)
        else:
            predictions.append(0)
    return predictions

get_domain_info = GetDomainInfo()
def predict(domain: list):
    data = [get_domain_info.domain_information(domain)]
    return predict_new_data(data, weights, bias, vocab)[0]

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
        pred = predict(domain)
    except Exception as error:
        print(f"có 1 chút lỗi ở phần dự đoán nên chạy lại mã lỗi là: {error}")
        return 0
    if str(pred) in '1':
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

def run_script(c=10):
    threads = []
    for _ in range(c):
        thread = threading.Thread(target=predict_domain)
        thread.start()
        threads.append(thread)
    for t in threads:
        t.join()
        
if __name__ == "__main__":
    print("*BETA mobile version")
    print("*Công cụ AI phân tích tên miền Domain-FU (mobile)")
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