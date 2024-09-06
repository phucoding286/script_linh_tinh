def add_dataTrain(card_info: str, label: str):
    with open("train.txt", "a", encoding="utf-8") as f:
        f.write(f"{card_info} </split> {label}\n")