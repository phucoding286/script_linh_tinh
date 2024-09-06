from __addDataTrain import add_dataTrain
from __checkCard import CardPredict
import threading
import time
from credit_card_info_generator import generate_credit_card


cardpredict = CardPredict()

def add_datatrain(card):
    try:
        card_process = card.split("|")
    except:
        print('''error! attention this punction "|"''')
        return 0
    if int(card_process[1]) < 1 or int(card_process[1]) > 12:
        print("error month!")
        return 0
    elif int(card_process[2]) < 24 or int(card_process[2]) > 2000 and int(card_process[2]) < 2024:
        print("error year!")
        return 0
    if int(card_process[2]) < 100:
        card_process[2] = str(int(card_process[2]) + 2000)
        card = "|".join(card_process)
    label = int(input("enter label: "))
    if label == 1:
        add_dataTrain(card, "1")
    else:
        add_dataTrain(card, "0")


def predictcard(card):
    return cardpredict.predict(card)


def predictcards(path_file="cards.txt"):
    with open("cards.txt", "w") as f:
        f.write("")
    with open("valid_cc.txt", "w") as f:
        f.write("")
    for _ in range(10):
        while True:
            card = generate_credit_card('Visa')
            if len(card['card_number']) < 15:
                continue
            else:
                break
        card['expiry_date'] = card['expiry_date'].replace('/', "|")
        card = f"{card['card_number']}|{card['expiry_date']}|{card["cvv"]}"
        with open("cards.txt", "a", encoding='utf8') as f:
            f.write(f"{card}\n")
    def checkcard(card: str):
        card_predict = cardpredict.predict(card)
        print(f"card: {card} result: {card_predict}")
        if int(card_predict) == 1:
            with open("valid_cc.txt", "a", encoding="utf-8") as f:
                f.write(f"{card}\n")
    try:
        with open(path_file, "r", encoding='utf8') as f:
            cards = f.read().splitlines()
    except:
        print("error file name")
        return 0

    threads = []
    for c in cards:
        thread = threading.Thread(target=checkcard, args=[c])
        threads.append(thread)
        thread.start()
        time.sleep(0.2)
    for t in threads:
        t.join()
    
    print("listing valid cards...")
    with open("valid_cc.txt", "r", encoding='utf8') as f:
        [print(i) for i in f.read().splitlines()]


if __name__ == "__main__":
    print("1. /add <card number>")
    print("2. /pred <card number>")
    print("3. /check <file path of cars>")
    print("/help")
    while True:
        try:
            command_inp = input("enter the command: ")

            if command_inp in "1":
                card_inp = input("enter your card: ").strip()
                add_datatrain(card_inp)
            elif command_inp.split()[0] == "/add":
                add_datatrain(command_inp.split()[1])
        
            elif command_inp in "2":
                card = input("enter your card: ")
                print(predictcard(card))
            elif command_inp.split()[0] == "/pred":
                print(predictcard(command_inp.split()[1]))
        
            elif command_inp in "3":
                file_path_inp = input("enter your cards file path: ")
                predictcards(file_path_inp)
            elif command_inp.split()[0] == "/check" or command_inp.split()[0] == "/chk":
                predictcards(command_inp.split()[1])

            elif command_inp == "/help":
                print("1. /add <card number>")
                print("2. /pred <card number>")
                print("3. /check <file path of cars>")
        except:
            print("program had error! please check your data form if its wrong!")
            continue