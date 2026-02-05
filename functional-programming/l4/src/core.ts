export type Operation = 'add' | 'subtract' | 'multiply' | 'divide' | 'pow' | 'sqrt';

export interface CalculatorState {
    readonly currentOperand: string;
    readonly previousOperand: string | null;
    readonly operation: Operation | null;
    readonly overwrite: boolean; // Флаг перезаписи текущего операнда после вычисления
    readonly error: string | null;
}

export const initialState: CalculatorState = {
    currentOperand: '0',
    previousOperand: null,
    operation: null,
    overwrite: false,
    error: null,
};

// --- Чистые функции ---

export const add = (a: number, b: number): number => a + b;
export const subtract = (a: number, b: number): number => a - b;
export const multiply = (a: number, b: number): number => a * b;
export const divide = (a: number, b: number): number => {
    if (b === 0) throw new Error("Division by zero");
    return a / b;
};
export const power = (a: number, b: number): number => Math.pow(a, b);
export const sqrt = (a: number): number => {
    if (a < 0) throw new Error("Invalid Input");
    return Math.sqrt(a);
}

export const formatOperand = (operand: string): string => {
    // Базовое форматирование при необходимости
    return operand;
}


// --- Редьюсер состояния (чистая функция) ---

type Action =
    | { type: 'add-digit', payload: string }
    | { type: 'choose-operation', payload: Operation }
    | { type: 'clear' }
    | { type: 'delete-digit' }
    | { type: 'calculate' };

const calculateResult = (state: CalculatorState): string | number => {
    const prev = parseFloat(state.previousOperand || '0');
    const current = parseFloat(state.currentOperand);

    if (isNaN(prev) || isNaN(current)) return "";

    try {
        switch (state.operation) {
            case 'add': return add(prev, current);
            case 'subtract': return subtract(prev, current);
            case 'multiply': return multiply(prev, current);
            case 'divide': return divide(prev, current);
            case 'pow': return power(prev, current);
            default: return "";
        }
    } catch (e) {
        return "Error";
    }
}

export const calculatorReducer = (state: CalculatorState, action: Action): CalculatorState => {
    switch (action.type) {
        case 'add-digit':
            if (state.overwrite) {
                return {
                    ...state,
                    currentOperand: action.payload,
                    overwrite: false,
                    error: null
                };
            }
            if (action.payload === '0' && state.currentOperand === '0') return state;
            if (action.payload === '.' && state.currentOperand.includes('.')) return state;

            return {
                ...state,
                currentOperand: state.currentOperand === '0' && action.payload !== '.'
                    ? action.payload
                    : state.currentOperand + action.payload,
                error: null
            };

        case 'choose-operation':
            // Обработка унарной операции сразу
            if (action.payload === 'sqrt') {
                try {
                    const result = sqrt(parseFloat(state.currentOperand));
                    return {
                        ...state,
                        currentOperand: result.toString(),
                        operation: null,
                        previousOperand: null,
                        overwrite: true,
                        error: null
                    }
                } catch (e) {
                    return { ...state, error: "Invalid Input", currentOperand: "Error", overwrite: true };
                }
            }

            if (state.currentOperand === '' && state.previousOperand == null) return state;

            if (state.currentOperand === '') {
                return {
                    ...state,
                    operation: action.payload
                }
            }

            if (state.previousOperand == null) {
                return {
                    ...state,
                    operation: action.payload,
                    previousOperand: state.currentOperand,
                    currentOperand: ''
                }
            }

            // Цепочка операций
            const result = calculateResult(state);
            return {
                ...state,
                previousOperand: result.toString(),
                operation: action.payload,
                currentOperand: '',
                error: result === "Error" ? "Error" : null
            };

        case 'clear':
            return initialState;

        case 'calculate':
            if (state.operation == null || state.currentOperand == '' || state.previousOperand == null) {
                return state;
            }

            const finalResult = calculateResult(state);

            return {
                ...state,
                overwrite: true,
                previousOperand: null,
                operation: null,
                currentOperand: finalResult.toString(),
                error: finalResult === "Error" ? "Error" : null
            };

        default:
            return state;
    }
};
