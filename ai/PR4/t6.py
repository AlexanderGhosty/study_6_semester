def is_prime(x):
    if x < 2:
        return False
    if x == 2:
        return True
    if x % 2 == 0:
        return False
    for i in range(3, int(x ** 0.5) + 1, 2):
        if x % i == 0:
            return False
    return True


def find_nearest_prime(n):
    if is_prime(n):
        return n
    up = n + 1
    down = n - 1
    while True:
        if is_prime(up):
            return up
        if down > 1 and is_prime(down):
            return down
        up += 1
        down -= 1


while True:
    try:
        number = int(input("Введите число (или 'q' для выхода): "))
        if is_prime(number):
            print(f"{number} - это простое число!")
        else:
            nearest_prime = find_nearest_prime(number)
            print(f"{number} - не является простым. Ближайшее простое число: {nearest_prime}")
    except ValueError:
        break
