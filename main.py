import json
# Начало работы с данными об операциях
with open("operations/operations.json", "rb") as read_file:
    translations = json.load(read_file)


# Функция по выводу даты последних пяти операций
def lust_translations(data):
    dictionary = []
    for operation in data:
        if operation:
            if operation["state"] == "EXECUTED":
                dictionary.append((operation.get("date", 0).split('T')))
    dictionary = dict(dictionary)
    date = sorted(dictionary)[:-6:-1]
    return date


# Функция по нахождению данных об операции по дате её проведения
def find_translation(data):
    for operation in translations:
        if operation["date"][:10] == data:
            return operation


# Функция шифрования данных карт и счетов
def private(account_details, action):
    if account_details.get(action, 0):
        oper = account_details[action].split()
        card, card_number = " ".join(oper[:-1]), oper[-1]
        if account_details[action].split()[0] != "Счет":
            private_number = card_number[:6] + (len(card_number[6:-4]) * '*') + card_number[-4:]
            chunks, chunk_size = len(private_number), len(private_number) // 4
            private_number = " ".join([private_number[i:i + chunk_size] for i in range(0, chunks, chunk_size)])
        else:
            private_number = '**' + card_number[-4:]
    else:
        return ""
    if action == "from": return f"{card} {private_number} -> "
    else: return f"{card} {private_number}"


# Функция для вывода данных об операциях
def return_translation(data):
    posts = lust_translations(data)
    for post in posts:
        date = post
        operation = find_translation(date)
        post = operation["operationAmount"]
        currency = post["currency"]
        print(f"{(".").join(str(date).split("-")[::-1])} {operation["description"]} \n"
              f"{private(operation, "from")}{private(operation, "to")} \n"
              f"{post["amount"]} {currency["name"]} \n")


return_translation(translations)
