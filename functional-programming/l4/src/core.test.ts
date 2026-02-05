import { describe, it, expect } from 'vitest';
import { add, subtract, multiply, divide, power, sqrt, calculatorReducer, initialState } from './core';

describe('Pure Functions', () => {
    it('adds numbers', () => {
        expect(add(2, 3)).toBe(5);
    });
    it('subtracts numbers', () => {
        expect(subtract(5, 2)).toBe(3);
    });
    it('multiplies numbers', () => {
        expect(multiply(4, 3)).toBe(12);
    });
    it('divides numbers', () => {
        expect(divide(10, 2)).toBe(5);
    });
    it('throws error on division by zero', () => {
        expect(() => divide(5, 0)).toThrow();
    });
    it('powers numbers', () => {
        expect(power(2, 3)).toBe(8);
    });
    it('sqrts numbers', () => {
        expect(sqrt(9)).toBe(3);
    });
});

describe('Calculator Reducer', () => {
    it('handles adding digits', () => {
        const state = calculatorReducer(initialState, { type: 'add-digit', payload: '1' });
        expect(state.currentOperand).toBe('1');
        const state2 = calculatorReducer(state, { type: 'add-digit', payload: '2' });
        expect(state2.currentOperand).toBe('12');
    });

    it('handles operations', () => {
        let state = calculatorReducer(initialState, { type: 'add-digit', payload: '5' });
        state = calculatorReducer(state, { type: 'choose-operation', payload: 'add' });
        expect(state.operation).toBe('add');
        expect(state.previousOperand).toBe('5');
        expect(state.currentOperand).toBe('');
    });

    it('handles calculation', () => {
        let state = calculatorReducer(initialState, { type: 'add-digit', payload: '2' });
        state = calculatorReducer(state, { type: 'choose-operation', payload: 'add' });
        state = calculatorReducer(state, { type: 'add-digit', payload: '3' });
        state = calculatorReducer(state, { type: 'calculate' });
        expect(state.currentOperand).toBe('5');
    });

    it('handles sqrt immediate execution', () => {
        let state = calculatorReducer(initialState, { type: 'add-digit', payload: '16' });
        state = calculatorReducer(state, { type: 'choose-operation', payload: 'sqrt' });
        expect(state.currentOperand).toBe('4');
    });
});
