import './style.css' // Импорт стилей для обработки Vite
import {
    initialState,
    calculatorReducer,
    CalculatorState,
    Operation
} from './core'

// --- Побочные эффекты / Взаимодействие с DOM ---

// Функция высшего порядка для логирования (требование ТЗ)
const withLogging = <T extends unknown[], R>(fn: (...args: T) => R) => {
    return (...args: T): R => {
        // console.log('Действие отправлено:', args);
        return fn(...args);
    }
}

// Выбор элементов DOM
const previousOperandTextElement = document.querySelector('[id="previous-operand"]') as HTMLElement;
const currentOperandTextElement = document.querySelector('[id="current-operand"]') as HTMLElement;

// Чистая функция отрисовки
const updateDisplay = (state: CalculatorState): void => {
    currentOperandTextElement.innerText = state.currentOperand;
    if (state.operation != null) {
        previousOperandTextElement.innerText = `${state.previousOperand} ${formatOperation(state.operation)}`;
    } else {
        previousOperandTextElement.innerText = '';
    }
}

const formatOperation = (op: Operation): string => {
    switch (op) {
        case 'add': return '+';
        case 'subtract': return '-';
        case 'multiply': return '*';
        case 'divide': return '/';
        case 'pow': return '^';
        default: return op;
    }
}

// Основной цикл приложения
let currentState = initialState;

const dispatch = withLogging((action: any) => {
    currentState = calculatorReducer(currentState, action);
    updateDisplay(currentState);
});

// Генератор обработчиков событий (ФВП)
const createClickListener = (actionType: string, payload?: any) => () => {
    dispatch({ type: actionType, payload });
};

// Привязка событий
document.querySelectorAll('[data-number]').forEach(button => {
    const btn = button as HTMLElement;
    btn.addEventListener('click', createClickListener('add-digit', btn.innerText));
});

document.querySelectorAll('[data-action]').forEach(button => {
    const btn = button as HTMLElement;
    const action = btn.dataset.action;

    // Маппинг UI-действий на действия редьюсера
    if (action === 'clear') {
        btn.addEventListener('click', createClickListener('clear'));
    } else if (action === 'calculate') {
        btn.addEventListener('click', createClickListener('calculate'));
    } else {
        // Операции
        btn.addEventListener('click', createClickListener('choose-operation', action));
    }
});

// Начальная отрисовка
updateDisplay(currentState);
