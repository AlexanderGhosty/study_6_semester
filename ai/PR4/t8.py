import random
import os
import shutil
import subprocess
import time


def clear_screen():
    if os.name == "nt":
        subprocess.run(["cmd", "/c", "cls"], check=False)
        return

    clear_cmd = shutil.which("clear")
    if clear_cmd:
        subprocess.run([clear_cmd], check=False)


difficulty = 0.7
score_player = 0
score_bot = 0
all_cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
print("Поиграем в 21? \nЕсли хотите играть, нажмите Enter, если хотите выйти, то нажмите Ctrl+C")
input()
while True:
    if score_player == 21:
        print("Больше карт не надо, у вас 21")
        print("Вы автоматически победили бота, так как у вас 21.")
        input("Нажмите Enter, чтобы закрыть.")
        break
    if score_player > 21:
        print("Вы проиграли, так как набрали больше 21")
        print("Попробуйте ещё раз.")
        input("Нажмите Enter, чтобы закрыть.")
        break
    yes_or_no = input("Будете ли вы брать карту? (yes/no): ").lower()
    clear_screen()
    if yes_or_no == 'yes':
        clear_screen()
        drawn_card = random.choice(all_cards)
        print(f"Вы взяли карту: {drawn_card}")
        score_player += drawn_card
        print(f"Сейчас у вас {score_player} очков.")
    if yes_or_no == 'no':
        print(f"У вас {score_player} очков.")
        print("Ход бота...")
        time.sleep(2)
        clear_screen()
        while True:
            if score_bot < 15:
                print("Бот берет карту.")
                drawn_card = random.choice(all_cards)
                print(f"Боту выпало {drawn_card} очков.")
                score_bot += drawn_card
                print(f"У бота {score_bot} очков.")
                time.sleep(2)
            clear_screen()
            if score_bot > 21:
                print(f"Бот проиграл! У него {score_bot} очков, а у вас {score_player}.")
                input("Нажмите Enter, чтобы закрыть.")
                exit(0)
            if score_bot >= 15:
                # Последний ход бота с учетом сложности
                if random.random() > difficulty:
                    drawn_card = random.choice(all_cards)
                    print("Бот взял случайную карту.")
                else:
                    # Бот пытается подобрать оптимальную карту
                    possible_cards = [card for card in all_cards if score_bot + card <= 21]
                    drawn_card = max(possible_cards, default=random.choice(all_cards))
                    print("Бот выбрал карту с учетом стратегии.")

                print(f"Боту выпало {drawn_card} очков.")
                score_bot += drawn_card
                print(f"У бота {score_bot} очков.")
                time.sleep(2)
                clear_screen()

                if score_bot > 21:
                    print(f"Бот проиграл - {score_bot} очков, а у вас {score_player}.")
                    input("Нажмите Enter, чтобы закрыть.")
                    exit(0)

                if score_bot > score_player:
                    print(f"Бот победил! У него {score_bot} очков, а у вас {score_player}. Попробуйте снова.")
                    input("Нажмите Enter, чтобы закрыть.")
                    exit(0)

                if score_bot == score_player:
                    print(f"Ничья! У обоих {score_player} очков.")
                    input("Нажмите Enter, чтобы закрыть.")
                    exit(0)
