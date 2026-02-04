// 1. Чистые функции для работы с массивами

/**
 * Фильтрует массив, оставляя только чётные числа
 * @param {number[]} numbers - Массив чисел
 * @returns {number[]} Новый массив с чётными числами
 */
const filterEvenNumbers = (numbers) => numbers.filter((num) => num % 2 === 0);

/**
 * Возвращает массив квадратов чисел
 * @param {number[]} numbers - Массив чисел
 * @returns {number[]} Новый массив с квадратами чисел
 */
const squareNumbers = (numbers) => numbers.map((num) => num ** 2);

/**
 * Фильтрует массив объектов по наличию определённого свойства
 * @param {Object[]} objects - Массив объектов
 * @param {string} property - Имя свойства для проверки
 * @returns {Object[]} Новый массив с объектами, содержащими указанное свойство
 */
const filterByProperty = (objects, property) =>
    objects.filter((obj) => Object.prototype.hasOwnProperty.call(obj, property));

/**
 * Вычисляет сумму всех чисел в массиве
 * @param {number[]} numbers - Массив чисел
 * @returns {number} Сумма чисел
 */
const sumArray = (numbers) => numbers.reduce((acc, num) => acc + num, 0);

// ============================================
// 2. Функция высшего порядка

/**
 * Применяет переданную функцию к каждому элементу массива
 * @param {Function} fn - Функция для применения
 * @param {Array} array - Массив элементов
 * @returns {Array} Новый массив с результатами применения функции
 */
const mapArray = (fn, array) => array.map(fn);

// ============================================
// 3. Составные математические операции

/**
 * Вычисляет сумму квадратов всех чётных чисел в массиве
 * @param {number[]} numbers - Массив чисел
 * @returns {number} Сумма квадратов чётных чисел
 */
const sumOfSquaresOfEvens = (numbers) => {
    const evens = filterEvenNumbers(numbers);
    const squares = squareNumbers(evens);
    return sumArray(squares);
};

/**
 * Альтернативная реализация через композицию функций
 * @param {number[]} numbers - Массив чисел
 * @returns {number} Сумма квадратов чётных чисел
 */
const sumOfSquaresOfEvensComposed = (numbers) =>
    sumArray(squareNumbers(filterEvenNumbers(numbers)));

/**
 * Вычисляет среднее арифметическое чисел, превышающих заданное значение,
 * в массиве объектов
 * @param {Object[]} objects - Массив объектов
 * @param {string} property - Имя числового свойства
 * @param {number} threshold - Пороговое значение
 * @returns {number} Среднее арифметическое или 0, если нет подходящих значений
 */
const averageAboveThreshold = (objects, property, threshold) => {
    const objectsWithProperty = filterByProperty(objects, property);
    const valuesAboveThreshold = objectsWithProperty
        .map((obj) => obj[property])
        .filter((value) => typeof value === "number" && value > threshold);

    if (valuesAboveThreshold.length === 0) return 0;

    return sumArray(valuesAboveThreshold) / valuesAboveThreshold.length;
};

// ============================================
// Демонстрация работы функций

// Тестовые данные
const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
const objects = [
    { name: "Алексей", age: 25, salary: 50000 },
    { name: "Мария", age: 30, salary: 60000 },
    { name: "Иван", age: 22 },
    { name: "Елена", age: 35, salary: 75000 },
    { name: "Дмитрий", salary: 45000 },
];

// 1. Демонстрация чистых функций
console.log("1. Чистые функции для работы с массивами:");
console.log("   Исходный массив:", numbers);
console.log("   Чётные числа:", filterEvenNumbers(numbers));
console.log("   Квадраты чисел:", squareNumbers(numbers));
console.log("   Сумма чисел:", sumArray(numbers));
console.log(
    '   Объекты со свойством "salary":',
    filterByProperty(objects, "salary")
);

// 2. Демонстрация функции высшего порядка
console.log("\n2. Функция высшего порядка mapArray:");
const double = (x) => x * 2;
const cube = (x) => x ** 3;
console.log("   Удвоение чисел:", mapArray(double, numbers));
console.log("   Кубы чисел:", mapArray(cube, numbers));

// 3. Демонстрация составных операций
console.log("\n3. Математические операции:");
console.log("   Сумма квадратов чётных чисел:", sumOfSquaresOfEvens(numbers));
console.log(
    "   Сумма квадратов чётных чисел (композиция):",
    sumOfSquaresOfEvensComposed(numbers)
);
console.log(
    '   Среднее значение salary > 50000:',
    averageAboveThreshold(objects, "salary", 50000)
);
console.log(
    '   Среднее значение age > 25:',
    averageAboveThreshold(objects, "age", 25)
);

// Экспорт функций для использования в других модулях
export {
    filterEvenNumbers,
    squareNumbers,
    filterByProperty,
    sumArray,
    mapArray,
    sumOfSquaresOfEvens,
    sumOfSquaresOfEvensComposed,
    averageAboveThreshold,
};
