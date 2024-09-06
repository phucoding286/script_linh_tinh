from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import threading
from selenium.webdriver.common.keys import Keys
import emoji

print("module created by Phu Tech")
print("my youtube channel: https://www.youtube.com/@phucoding286")
print("my facebook page: https://www.facebook.com/profile.php?id=61562099241369")
print("my github page: https://github.com/phucoding286")

class MesChat:
    def __init__(self, email_or_phone, password, group_or_chat):
        options = webdriver.ChromeOptions()

        options.add_argument("--log-level=3")
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--remote-debugging-port=9222")

        self.browser = webdriver.Chrome(options=options)
        self.email_or_phone = email_or_phone
        self.password = password
        self.group_or_chat = group_or_chat
        self.his_inp = ""
        self.current_inp = ""

        self.get_to_mes()
        self.login()
        self.check_verify()
        self.pass_notify()
        self.to_group_or_chat()
        threading.Thread(target=self.listening).start()
    
    def remove_emoji(self, text):
        return emoji.replace_emoji(text, replace="")

    def get_to_mes(self):
        self.browser.get("https://www.messenger.com/login/")
    
    def login(self):
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, "email"))) \
        .send_keys(self.email_or_phone)
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, "pass"))) \
        .send_keys(self.password)
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, "loginbutton"))) \
        .click()

    def check_verify(self):
        input("please verify acess (if have) and press enter to next: ")
        time.sleep(5)
        self.browser.get("https://www.messenger.com/login/")
        try:
            continue_with_acc = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class, '_2hyt')]")))
            continue_with_acc.click()
        except:
            print("haven't verify, will continue pass")
        input("press enter to next: ")

    def pass_notify(self):
        try:
            x1 = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Đóng']")))
            x1.click()
            x2 = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'x1lliihq') and text()='Không đồng bộ']")))
            x2.click()
        except:
            pass

    def to_group_or_chat(self):
        self.browser.get(self.group_or_chat)

    def listening(self):
        print("listening...")
        while True:
            try:
                time.sleep(0.5)
                message = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '(//div[@class="html-div xexx8yu x4uap5 x18d9i69 xkhd6sd x1gslohp x11i5rnm x12nagc x1mh8g0r x1yc453h x126k92a x18lvrbx"])[last()]')))
                message = message.text
                if message == self.his_inp:
                    continue
                else:
                    self.current_inp = message
            except:
                continue
    
    def send_message(self, inp=None, inp_down_line=None):
        try:

            send_msg = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, "//p[@class='xat24cr xdj266r']")))

            if inp is not None:
                inp = " ".join(inp.split())
                send_msg.send_keys( self.remove_emoji(inp+" ") )
                send_msg.send_keys(Keys.ENTER)

            elif inp_down_line is not None:
                for inp in inp_down_line:
                    send_msg.send_keys( self.remove_emoji(inp+" ") )
                    send_msg.send_keys(Keys.SHIFT, Keys.ENTER)
                    time.sleep(0.2)
                send_msg.send_keys(Keys.ENTER)

        except:
            print("đã có lỗi khi gửi tin nhắn!")
        self.his_inp = self.current_inp

"""
thank you for visit my open source!
lets follow my github to view more than interesting product
in the future!
"""
