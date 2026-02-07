module MathFunctions

// Базовые математические операции
// Чистые функции, использующие неизменяемые данные по умолчанию в F#

/// Функция сложения двух чисел
let add x y = x + y

/// Функция вычитания двух чисел
let subtract x y = x - y

/// Функция умножения двух чисел
let multiply x y = x * y

/// Функция деления двух чисел
let divide x y = 
    if y = 0.0 then infinity 
    else x / y

// Рекурсивная функция факториала
let rec factorial n =
    if n < 0 then failwith "Факториал не определен для отрицательных чисел"
    elif n = 0 then 1
    else n * factorial (n - 1)

// Примеры каррирования

/// Прибавляет 5 к числу
let add5 = add 5

/// Вычитает число из 10
// Примечание: subtract выполняет x - y. subtract 10 создает функцию (10 - y)
let subtractFrom10 = subtract 10

/// Умножает число на 2
let double = multiply 2

/// Делит число на 2.0
// Примечание: Частичное применение (divide 2.0) означало бы 2.0 делить на x.
// Чтобы получить x / 2.0, мы можем явно указать аргумент или использовать инвертированный делитель.
let half x = divide x 2.0

[<EntryPoint>]
let main argv =
    printfn "Базовые математические операции"
    printfn "Сложение 10 + 5 = %d" (add 10 5)
    printfn "Вычитание 10 - 5 = %d" (subtract 10 5)
    printfn "Умножение 10 * 5 = %d" (multiply 10 5)
    printfn "Деление 10.0 / 4.0 = %f" (divide 10.0 4.0)

    printfn "\nРекурсивный факториал"
    printfn "Факториал 5 = %d" (factorial 5)
    printfn "Факториал 0 = %d" (factorial 0)
    try
        printfn "Факториал -1 = %d" (factorial -1)
    with
        | Failure msg -> printfn "Факториал -1 ожидаемо не удался: %s" msg

    printfn "\nКаррированные функции"
    printfn "add5 10 (10 + 5) = %d" (add5 10)
    printfn "subtractFrom10 4 (10 - 4) = %d" (subtractFrom10 4)
    printfn "double 5 (5 * 2) = %d" (double 5)
    printfn "half 10.0 (10.0 / 2.0) = %f" (half 10.0)

    0
