from random import choice

t = ["Камень", "Бумага", "Ножницы", "Колодец"]
player = False

while not player:
    computer = choice(t)
    player = input("Камень, Ножницы, Бумага, Колодец? > ").strip().capitalize()

    if player not in t:
        print("Некорректный ход! Попробуйте снова.")
        continue

    if player == computer:
        print("Ничья!")
    elif (player == "Камень" and computer in ["Ножницы"]) or \
            (player == "Бумага" and computer in ["Камень", "Колодец"]) or \
            (player == "Ножницы" and computer in ["Бумага"]) or \
            (player == "Колодец" and computer in ["Камень", "Ножницы"]):
        print(f"Ты выиграл! {player} побеждает {computer}.")
    else:
        print(f"Ты проиграл! {computer} побеждает {player}.")

    player = False
