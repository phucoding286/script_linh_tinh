from llm_module.memories_and_llm_system import predict, short_context
from chat_mes_module.chat_mes import MesChat
import random
import time

email = "smskherson@futuresoulrecords.com" # input("nhập email hoặc số điện thoại facebook: ")
passwd = "abcabc123" # input("nhập mật khẩu: ")
conv = "https://www.messenger.com/t/6309501179173926" # input("nhập link cuộc trò chuyện cá nhân hoặc group: ")
mes = MesChat(email, passwd, conv)

def bot_mes():
    off = False
    while True:
        time.sleep(0.2)
        if mes.current_inp == mes.his_inp:
            continue
        
        elif mes.current_inp.split()[0] in "/s":
            mes.send_message("hệ thống đã tạm tắt, để bật lại, hãy dùng /e")
            off = True

        elif mes.current_inp.split()[0] in "/e":
            mes.send_message("hệ thống đã bật trở lại, để tắt, hãy dùng /s")
            off = False

        elif off:
            continue

        elif mes.current_inp.split()[0] in "/info":
            bio = [
            "youtube: https://www.youtube.com/@phucoding286",
            "facebook: https://www.facebook.com/profile.php?id=61562099241369",
            "github: https://github.com/phucoding286",
            "trang web: "
            ]
            mes.send_message(inp_down_line=bio)

        elif mes.current_inp.split()[0] in "/c":
            print(f"tin nhắn từ người dùng: {mes.current_inp}")
            output = predict(mes.current_inp)
            mes.send_message(output)
            print(f"tin nhắn từ bot: {output}")

        elif mes.current_inp.split()[0] in "/d":
            with open("saved_v2.txt", 'r', encoding="utf-8") as f:
                domains = f.read().splitlines()

            if str(domains) == "[]":
                mes.send_message("chưa có tên miền nào đã được thu thập!")
                continue

            domain_says = random.choice([
                "xin chào dưới đây là những tên miền mà tool domain fu đã lấy được",
                "dưới đây là các tên miền đã lấy",
                "nè",
                "ok đây nè b",
                "đây hãy dùng nó để đk cloudsigma"
            ])

            domains = [domain_says]+domains
            mes.send_message(inp_down_line=domains)

            short_context.storage_short_context(mes.current_inp, "\n".join(domains))
        
        else:
            mes.send_message("dùng /c để chat, dùng /s để tạm tắt hệ thống, dùng /d để yêu cầu tên miền đăng ký cloudsigma, dùng /info để xem thông tin người sáng tạo")

bot_mes()