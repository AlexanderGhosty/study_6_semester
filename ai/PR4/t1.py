import random

user_guess = 0
computer_guess = 0

low = 1
high = 100

random_number = random.randint(low, high)

print(f'Я загадал число от {low} до {high}. Посмотрим, кто угадает первым — ты или компьютер!')

while True:
    user_guess = int(input('Твой ход, введи число: '))
    if user_guess < random_number:
        print(f'Больше, чем {user_guess}')
    elif user_guess > random_number:
        print(f'Меньше, чем {user_guess}')
    else:
        print(f'Поздравляю! Ты угадал число {random_number} и выиграл!')
        break

    computer_guess = random.randint(low, high)
    if computer_guess < random_number:
        print(f'Ход компьютера: Больше, чем {computer_guess}')
        low = computer_guess + 1
    elif computer_guess > random_number:
        print(f'Ход компьютера: Меньше, чем {computer_guess}')
        high = computer_guess - 1
    else:
        print(f'Компьютер угадал число {random_number} и выиграл!')
        break
