import math


def calc(a, b, op):
    if op not in ['+', '-', '*', '/', '^', '%', 'sqrt']:
        return 'Выберите операцию: +, -, *, /, ^, %, sqrt!'

    if op == '+':
        return f'{a} {op} {b} = {a + b}'
    if op == '-':
        return f'{a} {op} {b} = {a - b}'
    if op == '*':
        return f'{a} {op} {b} = {a * b}'
    if op == '/':
        return f'{a} {op} {b} = {a / b}' if b != 0 else 'Ошибка: невозможно поделить на 0'
    if op == '^':
        return f'{a} ^ {b} = {a ** b}'
    if op == '%':
        return f'{b}% от {a} = {(a * b) / 100}'
    if op == 'sqrt':
        return f'√{a} = {math.sqrt(a)}' if a >= 0 else 'Ошибка: корень отрицательный'


def main():
    while True:
        try:
            a = input('Введите первое число (или "q" для выхода): ')
            if a.lower() == 'q':
                print("Выход из программы.")
                break
            a = float(a)
            op = input('Выберите операцию (+, -, *, /, ^, %, sqrt): ')
            if op == 'sqrt':
                print(calc(a, None, op))
            else:
                b = float(input('Введите второе число: '))
                print(calc(a, b, op))
        except ValueError:
            print("Ошибка ввода. Попробуйте снова.")


if __name__ == '__main__':
    main()
