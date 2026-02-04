
// ============================================================================
// 1. Функция фильтрации чисел, кратных заданному числу

/**
 * Чистая функция, которая принимает массив чисел и возвращает новый массив,
 * содержащий только числа, кратные заданному числу.
 * 
 * @param numbers - исходный массив чисел
 * @param divisor - делитель для проверки кратности
 * @returns новый массив с числами, кратными divisor
 */
const filterMultiples = (numbers: number[], divisor: number): number[] => {
    if (divisor === 0) {
        throw new Error("Делитель не может быть равен нулю");
    }
    return numbers.filter((num: number): boolean => num % divisor === 0);
};

// ============================================================================
// 2. Функция объединения строк с разделителем

/**
 * Чистая функция, которая принимает массив строк и возвращает новую строку,
 * содержащую все строки, объединённые заданным разделителем.
 * 
 * @param strings - массив строк для объединения
 * @param separator - разделитель между строками
 * @returns объединённая строка
 */
const joinStrings = (strings: string[], separator: string): string => {
    return strings.reduce(
        (acc: string, current: string, index: number): string =>
            index === 0 ? current : `${acc}${separator}${current}`,
        ""
    );
};

// ============================================================================
// 3. Функция сортировки массива объектов по значению свойства (с generics)

/**
 * Тип для объекта с произвольным ключом, значение которого можно сравнивать
 */
type ComparableValue = string | number | boolean | Date;

/**
 * Порядок сортировки
 */
type SortOrder = "asc" | "desc";

/**
 * Чистая generic-функция, которая принимает массив объектов и возвращает
 * новый массив, отсортированный по значению определённого свойства.
 * 
 * @param items - массив объектов для сортировки
 * @param key - ключ свойства, по которому производится сортировка
 * @param order - порядок сортировки: "asc" (по возрастанию) или "desc" (по убыванию)
 * @returns новый отсортированный массив (исходный массив не изменяется)
 */
const sortByProperty = <T extends Record<K, ComparableValue>, K extends keyof T>(
    items: T[],
    key: K,
    order: SortOrder = "asc"
): T[] => {
    // Создаём копию массива для сохранения иммутабельности
    const sortedArray = [...items];

    return sortedArray.sort((a: T, b: T): number => {
        const valueA = a[key];
        const valueB = b[key];

        let comparison: number;

        // Обработка различных типов данных
        if (typeof valueA === "string" && typeof valueB === "string") {
            comparison = valueA.localeCompare(valueB);
        } else if (valueA instanceof Date && valueB instanceof Date) {
            comparison = valueA.getTime() - valueB.getTime();
        } else {
            comparison = valueA < valueB ? -1 : valueA > valueB ? 1 : 0;
        }

        return order === "desc" ? -comparison : comparison;
    });
};

// ============================================================================
// 4. Функция высшего порядка для логирования

/**
 * Тип для любой функции
 */
type AnyFunction<TArgs extends unknown[], TReturn> = (...args: TArgs) => TReturn;

/**
 * Интерфейс конфигурации логирования
 */
interface LogConfig {
    prefix?: string;
    logArgs?: boolean;
    logResult?: boolean;
    timestamp?: boolean;
}

/**
 * Функция высшего порядка, которая принимает другую функцию в качестве аргумента
 * и возвращает новую функцию, выполняющую логирование перед вызовом исходной функции.
 * 
 * @param fn - исходная функция для оборачивания
 * @param config - конфигурация логирования (опционально)
 * @returns новая функция с логированием
 */
const withLogging = <TArgs extends unknown[], TReturn>(
    fn: AnyFunction<TArgs, TReturn>,
    config: LogConfig = {}
): AnyFunction<TArgs, TReturn> => {
    const {
        prefix = "LOG",
        logArgs = true,
        logResult = true,
        timestamp = true
    } = config;

    return (...args: TArgs): TReturn => {
        const time = timestamp ? `[${new Date().toISOString()}]` : "";
        const functionName = fn.name || "anonymous";

        // Логирование перед вызовом
        console.log(`${time} [${prefix}] Вызов функции: ${functionName}`);

        if (logArgs && args.length > 0) {
            console.log(`${time} [${prefix}] Аргументы:`, JSON.stringify(args, null, 2));
        }

        // Вызов оригинальной функции
        const result = fn(...args);

        // Логирование результата
        if (logResult) {
            console.log(`${time} [${prefix}] Результат:`, JSON.stringify(result, null, 2));
        }

        return result;
    };
};

// ============================================================================
// Дополнительные utility-функции с generics

/**
 * Generic-функция для применения преобразования к массиву
 * (аналог map с явной типизацией)
 */
const mapArray = <TInput, TOutput>(
    arr: TInput[],
    transformer: (item: TInput, index: number) => TOutput
): TOutput[] => {
    return arr.map(transformer);
};

/**
 * Generic-функция для фильтрации массива с предикатом
 */
const filterArray = <T>(
    arr: T[],
    predicate: (item: T, index: number) => boolean
): T[] => {
    return arr.filter(predicate);
};

/**
 * Generic-функция для свёртки массива
 */
const reduceArray = <T, TAccumulator>(
    arr: T[],
    reducer: (acc: TAccumulator, item: T, index: number) => TAccumulator,
    initialValue: TAccumulator
): TAccumulator => {
    return arr.reduce(reducer, initialValue);
};

/**
 * Функция композиции двух функций
 */
const compose = <A, B, C>(
    f: (arg: A) => B,
    g: (arg: B) => C
): ((arg: A) => C) => {
    return (x: A): C => g(f(x));
};

/**
 * Функция частичного применения (каррирование)
 */
const curry2 = <A, B, C>(
    fn: (a: A, b: B) => C
): ((a: A) => (b: B) => C) => {
    return (a: A) => (b: B) => fn(a, b);
};

// ============================================================================
// Демонстрация работы функций

// 1. Демонстрация filterMultiples
console.log("\n--- 1. Фильтрация чисел, кратных заданному числу ---");
const numbers: number[] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 18, 20, 25, 30];
const multiplesOf3: number[] = filterMultiples(numbers, 3);
const multiplesOf5: number[] = filterMultiples(numbers, 5);

console.log(`Исходный массив: [${numbers.join(", ")}]`);
console.log(`Числа, кратные 3: [${multiplesOf3.join(", ")}]`);
console.log(`Числа, кратные 5: [${multiplesOf5.join(", ")}]`);

// 2. Демонстрация joinStrings
console.log("\n--- 2. Объединение строк с разделителем ---");
const words: string[] = ["TypeScript", "JavaScript", "Функции", "Generics"];
const withComma: string = joinStrings(words, ", ");
const withDash: string = joinStrings(words, " - ");
const withPipe: string = joinStrings(words, " | ");

console.log(`Исходный массив: [${words.map(w => `"${w}"`).join(", ")}]`);
console.log(`С разделителем ", ": "${withComma}"`);
console.log(`С разделителем " - ": "${withDash}"`);
console.log(`С разделителем " | ": "${withPipe}"`);

// 3. Демонстрация sortByProperty
console.log("\n--- 3. Сортировка массива объектов по свойству ---");

interface Person {
    name: string;
    age: number;
    city: string;
}

const people: Person[] = [
    { name: "Алексей", age: 25, city: "Москва" },
    { name: "Мария", age: 30, city: "Санкт-Петербург" },
    { name: "Дмитрий", age: 22, city: "Казань" },
    { name: "Анна", age: 28, city: "Новосибирск" },
    { name: "Борис", age: 35, city: "Екатеринбург" }
];

console.log("Исходный массив:");
console.table(people);

const sortedByAge = sortByProperty(people, "age", "asc");
console.log("\nОтсортировано по возрасту (по возрастанию):");
console.table(sortedByAge);

const sortedByName = sortByProperty(people, "name", "desc");
console.log("\nОтсортировано по имени (по убыванию):");
console.table(sortedByName);

// 4. Демонстрация withLogging
console.log("\n--- 4. Функция высшего порядка с логированием ---");

// Создаём простую функцию для демонстрации
const calculateSum = (a: number, b: number): number => a + b;

// Оборачиваем её в логирование
const loggedSum = withLogging(calculateSum, {
    prefix: "MATH",
    logArgs: true,
    logResult: true,
    timestamp: true
});

console.log("\nВызов функции с логированием:");
const sumResult = loggedSum(5, 3);

// Демонстрация с другой функцией
const processArray = (arr: number[]): number[] => arr.map(x => x * 2);
const loggedProcess = withLogging(processArray, { prefix: "ARRAY" });

console.log("\nОбработка массива с логированием:");
const processedResult = loggedProcess([1, 2, 3, 4, 5]);

// 5. Демонстрация дополнительных generic-функций
console.log("\n--- 5. Дополнительные generic-функции ---");

// mapArray
const squaredNumbers = mapArray(numbers.slice(0, 5), (n: number): number => n * n);
console.log(`Квадраты чисел [1-5]: [${squaredNumbers.join(", ")}]`);

// filterArray с предикатом
const evenNumbers = filterArray(numbers, (n: number): boolean => n % 2 === 0);
console.log(`Чётные числа: [${evenNumbers.join(", ")}]`);

// reduceArray
const sum = reduceArray(numbers.slice(0, 5), (acc: number, n: number): number => acc + n, 0);
console.log(`Сумма чисел [1-5]: ${sum}`);

// compose
const double = (x: number): number => x * 2;
const addTen = (x: number): number => x + 10;
const doubleAndAddTen = compose(double, addTen);
console.log(`compose(double, addTen)(5) = ${doubleAndAddTen(5)}`);

// curry
const curriedSum = curry2((a: number, b: number): number => a + b);
const add5 = curriedSum(5);
console.log(`curry: add5(3) = ${add5(3)}`);