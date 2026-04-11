def fibRecurse(n):
    assert n > 0, "n > 0"
    if n == 1 or n == 2: return 1
    return fibRecurse(n - 1) + fibRecurse(n - 2)


n = int(input('Сколько чисел? '))
assert n > 0, "Количество чисел должно быть больше 0"

fib_numbers = [str(fibRecurse(i)) for i in range(1, n + 1)]

print(', '.join(fib_numbers))
