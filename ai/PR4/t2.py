import random

list_of_words = [
    'яблоко', 'победа', 'программирование', 'терминал', 'ноутбук','интеллект', 'золото', 'компьютер'
]

random_word = random.choice(list_of_words)
set_of_symbols = set(random_word)
discovered_symbols = set()

player_health = 5
computer_health = 5

print('_ ' * len(random_word))

alphabet = set('абвгдеёжзийклмнопрстуфхцчшщьыъэюя')

while discovered_symbols != set_of_symbols and player_health > 0 and computer_health > 0:
    user_symbol = input("Ваш ход. Введите букву: ").lower()

    if len(user_symbol) != 1 or user_symbol not in alphabet:
        print("Введите ОДНУ букву русского алфавита.")
        continue

    if user_symbol in discovered_symbols:
        print("Вы уже вводили эту букву, попробуйте другую.")
        continue

    if user_symbol not in set_of_symbols:
        player_health -= 1
        print(f"Этой буквы нет в слове. Ваши жизни: {player_health}")
    else:
        print("Буква есть в слове!")
        discovered_symbols.add(user_symbol)

    if discovered_symbols == set_of_symbols:
        print(f"Поздравляем! Вы угадали слово: {random_word}")
        break

    available_letters = list(alphabet - discovered_symbols)
    computer_symbol = random.choice(available_letters)
    print(f"Компьютер выбирает: {computer_symbol}")

    if computer_symbol in set_of_symbols:
        print("Компьютер угадал букву!")
        discovered_symbols.add(computer_symbol)
    else:
        computer_health -= 1
        print(f"Компьютер ошибся. Осталось жизней: {computer_health}")

    if discovered_symbols == set_of_symbols:
        print(f"Компьютер победил! Загаданное слово: {random_word}")
        break

    current_word_progress = ' '.join(ch if ch in discovered_symbols else '_' for ch in random_word)
    print(current_word_progress)

if player_health == 0:
    print(f"Вы проиграли. Победил компьютер! Загаданное слово: {random_word}")
elif computer_health == 0:
    print(f"Компьютер проиграл. Поздравляю, вы правильно набрали слово {random_word}")