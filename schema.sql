CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,       -- Уникальный ID отдела
    name VARCHAR(100) NOT NULL,             -- Название отдела
    description TEXT                        -- Описание
);

CREATE TABLE positions (
    position_id SERIAL PRIMARY KEY,         -- Уникальный ID должности
    title VARCHAR(100) NOT NULL,            -- Название должности (например, "Аналитик")
    salary_min NUMERIC(10,2),               -- Мин. зарплата
    salary_max NUMERIC(10,2)                -- Макс. зарплата
);

CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,         -- Уникальный ID сотрудника
    first_name VARCHAR(50) NOT NULL,        -- Имя
    last_name VARCHAR(50) NOT NULL,         -- Фамилия
    email VARCHAR(100) UNIQUE NOT NULL,     -- Почта
    phone VARCHAR(20),                      -- Телефон
    hire_date DATE NOT NULL,                -- Дата найма
    department_id INT REFERENCES departments(department_id), -- Отдел
    position_id INT REFERENCES positions(position_id)        -- Должность
);

CREATE TABLE salaries (
    salary_id SERIAL PRIMARY KEY,           -- Уникальный ID записи
    employee_id INT REFERENCES employees(employee_id), -- Сотрудник
    amount NUMERIC(10,2) NOT NULL,          -- Сумма выплаты
    date_paid DATE NOT NULL                 -- Дата выплаты
);

CREATE TABLE projects (
    project_id SERIAL PRIMARY KEY,          -- Уникальный ID проекта
    name VARCHAR(200) NOT NULL,             -- Название проекта
    description TEXT,                       -- Описание проекта
    start_date DATE NOT NULL,               -- Дата начала
    end_date DATE                           -- Дата окончания
);

CREATE TABLE employee_projects (
    employee_id INT REFERENCES employees(employee_id),
    project_id INT REFERENCES projects(project_id),
    role VARCHAR(100),                      -- Роль сотрудника в проекте
    PRIMARY KEY (employee_id, project_id)   -- Составной ключ
);

CREATE TABLE work_logs (
    log_id SERIAL PRIMARY KEY,              -- ID записи
    employee_id INT REFERENCES employees(employee_id),
    project_id INT REFERENCES projects(project_id),
    work_date DATE NOT NULL,                -- Дата работы
    hours_worked NUMERIC(5,2) NOT NULL,     -- Отработанное время (часы)
    description TEXT                        -- Что делал сотрудник
);