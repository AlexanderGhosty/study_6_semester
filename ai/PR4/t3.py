import random

FILENAME = "passwords.txt"

def generate_password():
    password = []
    for _ in range(random.randint(2, 4)):
        password.append(chr(random.randint(65, 90)))
    for _ in range(random.randint(2, 4)):
        password.append(chr(random.randint(97, 122)))
    for _ in range(random.randint(2, 4)):
        password.append(chr(random.randint(48, 57)))
    for _ in range(random.randint(2, 4)):
        password.append(chr(random.randint(33, 47)))
    random.shuffle(password)
    return ''.join(password)


with open(FILENAME, "a", encoding="utf-8") as file:
    while True:
        site = input("Введите сайт (или 'q' для выхода): ").strip()
        if site.lower() == 'q':
            break
        login = input("Введите логин: ").strip()
        password = generate_password()
        print(f"Сгенерированный пароль: {password}")
        file.write(f"{site}-{login}-{password}\n")

print(f"Пароли сохранены в файл {FILENAME}")