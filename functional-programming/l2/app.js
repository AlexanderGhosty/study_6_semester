/**
 * Создаёт новую задачу (чистая функция)
 * @param {string} text - Текст задачи
 * @returns {Object} - Объект задачи
 */
const createTask = (text) => ({
    id: Date.now(),
    text: text.trim(),
    completed: false,
    createdAt: new Date().toISOString()
});

/**
 * Добавляет задачу в список (иммутабельно)
 * @param {Array} tasks - Текущий список задач
 * @param {Object} task - Новая задача
 * @returns {Array} - Новый список с добавленной задачей
 */
const addTask = (tasks, task) => [...tasks, task];

/**
 * Удаляет задачу из списка (иммутабельно, использует filter - функцию высшего порядка)
 * @param {Array} tasks - Текущий список задач
 * @param {number} id - ID задачи для удаления
 * @returns {Array} - Новый список без удалённой задачи
 */
const removeTask = (tasks, id) => tasks.filter(task => task.id !== id);

/**
 * Переключает статус выполнения задачи (иммутабельно, использует map)
 * @param {Array} tasks - Текущий список задач
 * @param {number} id - ID задачи
 * @returns {Array} - Новый список с изменённым статусом задачи
 */
const toggleTask = (tasks, id) => 
    tasks.map(task => 
        task.id === id 
            ? { ...task, completed: !task.completed }
            : task
    );

/**
 * Удаляет все выполненные задачи (иммутабельно)
 * @param {Array} tasks - Текущий список задач
 * @returns {Array} - Новый список без выполненных задач
 */
const clearCompleted = (tasks) => tasks.filter(task => !task.completed);

// ============================================================================
// ФУНКЦИИ ВЫСШЕГО ПОРЯДКА ДЛЯ ФИЛЬТРАЦИИ

/**
 * Предикаты для фильтрации (чистые функции)
 */
const predicates = {
    all: () => true,
    active: task => !task.completed,
    completed: task => task.completed
};

/**
 * Фильтрует задачи по статусу (чистая функция)
 * @param {Array} tasks - Список задач
 * @param {string} filter - Тип фильтра ('all', 'active', 'completed')
 * @returns {Array} - Отфильтрованный список
 */
const filterTasks = (tasks, filter) => {
    const predicate = predicates[filter] || predicates.all;
    return tasks.filter(predicate);
};

/**
 * Функция высшего порядка для подсчёта по условию
 * @param {Function} predicate - Функция-предикат
 * @returns {Function} - Функция, принимающая массив и возвращающая количество
 */
const countBy = (predicate) => (tasks) => tasks.filter(predicate).length;

// Производные функции подсчёта (частичное применение)
const countActive = countBy(task => !task.completed);
const countCompleted = countBy(task => task.completed);
const countAll = (tasks) => tasks.length;

// ============================================================================
// ФУНКЦИЯ КОМПОЗИЦИИ (PIPE)

/**
 * Композиция функций слева направо (функция высшего порядка)
 * @param  {...Function} fns - Функции для композиции
 * @returns {Function} - Скомпонованная функция
 */
const pipe = (...fns) => (initialValue) => 
    fns.reduce((value, fn) => fn(value), initialValue);

// ============================================================================
// РАБОТА С LOCALSTORAGE (САЙД-ЭФФЕКТЫ ИЗОЛИРОВАНЫ)

const STORAGE_KEY = 'fp-todo-tasks';

/**
 * Загружает задачи из localStorage
 * @returns {Array} - Список задач
 */
const loadTasks = () => {
    try {
        const data = localStorage.getItem(STORAGE_KEY);
        return data ? JSON.parse(data) : [];
    } catch (error) {
        console.error('Ошибка загрузки данных:', error);
        return [];
    }
};

/**
 * Сохраняет задачи в localStorage
 * @param {Array} tasks - Список задач
 */
const saveTasks = (tasks) => {
    try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks));
    } catch (error) {
        console.error('Ошибка сохранения данных:', error);
    }
};

// ============================================================================
// УПРАВЛЕНИЕ СОСТОЯНИЕМ ПРИЛОЖЕНИЯ

/**
 * Начальное состояние приложения
 */
const createInitialState = () => ({
    tasks: loadTasks(),
    filter: 'all'
});

/**
 * Глобальное состояние (единственная мутабельная переменная)
 */
let state = createInitialState();

/**
 * Обновляет состояние и перерисовывает UI
 * @param {Function} updater - Функция обновления состояния
 */
const setState = (updater) => {
    // Создаём новое состояние иммутабельно
    const newState = updater(state);
    state = { ...state, ...newState };
    
    // Сохраняем задачи
    saveTasks(state.tasks);
    
    // Перерисовываем UI
    render();
};

// ============================================================================
// РЕНДЕРИНГ UI

/**
 * Создаёт HTML для одной задачи (чистая функция)
 * @param {Object} task - Объект задачи
 * @returns {string} - HTML строка
 */
const createTaskHTML = (task) => `
    <li class="task-item ${task.completed ? 'completed' : ''}" data-id="${task.id}">
        <label class="task-checkbox">
            <input 
                type="checkbox" 
                ${task.completed ? 'checked' : ''} 
                aria-label="Отметить задачу как ${task.completed ? 'невыполненную' : 'выполненную'}"
            >
            <span class="checkbox-custom"></span>
        </label>
        <span class="task-text">${escapeHtml(task.text)}</span>
        <button class="delete-btn" aria-label="Удалить задачу" title="Удалить">
            ✕
        </button>
    </li>
`;

/**
 * Экранирует HTML для предотвращения XSS (чистая функция)
 * @param {string} text - Исходный текст
 * @returns {string} - Безопасный текст
 */
const escapeHtml = (text) => {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
};

/**
 * Основная функция рендеринга
 */
const render = () => {
    const { tasks, filter } = state;
    
    // Фильтруем задачи
    const filteredTasks = filterTasks(tasks, filter);
    
    // Рендерим список задач
    const taskList = document.getElementById('task-list');
    taskList.innerHTML = filteredTasks.map(createTaskHTML).join('');
    
    // Обновляем счётчик
    const activeCount = countActive(tasks);
    document.getElementById('active-count').textContent = activeCount;
    
    // Показываем/скрываем пустое состояние
    const emptyState = document.getElementById('empty-state');
    emptyState.classList.toggle('visible', filteredTasks.length === 0);
    
    // Показываем/скрываем кнопку очистки
    const completedCount = countCompleted(tasks);
    const actionsSection = document.getElementById('actions-section');
    actionsSection.classList.toggle('visible', completedCount > 0);
    
    // Обновляем активный фильтр
    updateFilterButtons(filter);
};

/**
 * Обновляет состояние кнопок фильтра
 * @param {string} activeFilter - Текущий фильтр
 */
const updateFilterButtons = (activeFilter) => {
    const buttons = document.querySelectorAll('.filter-btn');
    buttons.forEach(btn => {
        const isActive = btn.dataset.filter === activeFilter;
        btn.classList.toggle('active', isActive);
    });
};

// ============================================================================
// ОБРАБОТЧИКИ СОБЫТИЙ

/**
 * Обработчик добавления задачи
 * @param {Event} event - Событие формы
 */
const handleAddTask = (event) => {
    event.preventDefault();
    
    const input = document.getElementById('task-input');
    const text = input.value.trim();
    
    if (text) {
        const newTask = createTask(text);
        setState(state => ({
            tasks: addTask(state.tasks, newTask)
        }));
        input.value = '';
        input.focus();
    }
};

/**
 * Обработчик клика по списку задач (делегирование событий)
 * @param {Event} event - Событие клика
 */
const handleTaskListClick = (event) => {
    const taskItem = event.target.closest('.task-item');
    if (!taskItem) return;
    
    const taskId = parseInt(taskItem.dataset.id, 10);
    
    // Клик по чекбоксу - переключение статуса
    if (event.target.type === 'checkbox') {
        setState(state => ({
            tasks: toggleTask(state.tasks, taskId)
        }));
    }
    
    // Клик по кнопке удаления
    if (event.target.classList.contains('delete-btn')) {
        // Анимация удаления
        taskItem.classList.add('removing');
        setTimeout(() => {
            setState(state => ({
                tasks: removeTask(state.tasks, taskId)
            }));
        }, 300);
    }
};

/**
 * Обработчик клика по фильтрам
 * @param {Event} event - Событие клика
 */
const handleFilterClick = (event) => {
    const filterBtn = event.target.closest('.filter-btn');
    if (!filterBtn) return;
    
    const filter = filterBtn.dataset.filter;
    setState(() => ({ filter }));
};

/**
 * Обработчик очистки выполненных задач
 */
const handleClearCompleted = () => {
    setState(state => ({
        tasks: clearCompleted(state.tasks)
    }));
};

// ============================================================================
// ИНИЦИАЛИЗАЦИЯ ПРИЛОЖЕНИЯ

/**
 * Инициализирует приложение
 */
const init = () => {
    // Привязываем обработчики событий
    document.getElementById('add-task-form').addEventListener('submit', handleAddTask);
    document.getElementById('task-list').addEventListener('click', handleTaskListClick);
    document.getElementById('filters').addEventListener('click', handleFilterClick);
    document.getElementById('clear-completed-btn').addEventListener('click', handleClearCompleted);
    
    // Первоначальный рендеринг
    render();
    
    console.log('✅ Приложение "Список задач" инициализировано');
};

// Запуск приложения после загрузки DOM
document.addEventListener('DOMContentLoaded', init);
