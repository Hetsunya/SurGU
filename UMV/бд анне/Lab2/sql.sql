-- Создание таблицы natural_person
CREATE TABLE natural_person (
    id SERIAL PRIMARY KEY,
    passport VARCHAR(255) UNIQUE,
    forename VARCHAR(255),
    phone VARCHAR(255),
    email VARCHAR(255),
    delivery_address VARCHAR(255)
);

-- Создание таблицы legal_person
CREATE TABLE legal_person (
    id SERIAL PRIMARY KEY,
    inn VARCHAR(255) UNIQUE,
    name VARCHAR(255),
    phone VARCHAR(255),
    email VARCHAR(255),
    delivery_address VARCHAR(255),
    representative_forename VARCHAR(255)
);

-- Создание таблицы provider
CREATE TABLE provider (
    id SERIAL PRIMARY KEY,
    inn VARCHAR(255) UNIQUE,
    name VARCHAR(255),
    address VARCHAR(255)
);

-- Создание таблицы product
CREATE TABLE product (
    id SERIAL PRIMARY KEY,
    place INTEGER UNIQUE,
    provider_id INTEGER REFERENCES provider(id),
    provider_name VARCHAR(255),
    name VARCHAR(255),
    receipt_date DATE,
    article VARCHAR(255) UNIQUE,
    quantity INT,
    price DECIMAL(10, 2),
    weight DECIMAL(5, 2)
);

-- Создание таблицы orders
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    order_number INTEGER UNIQUE,
    weight DECIMAL(5, 2),
    registration_date DATE,
    cost DECIMAL(10, 2),
    customer_id INTEGER,
    customer_category VARCHAR(50) CHECK (customer_category IN ('Юр. лицо', 'Физ. лицо')),
    CONSTRAINT fk_legal_person FOREIGN KEY (customer_id) REFERENCES legal_person(id) DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT fk_natural_person FOREIGN KEY (customer_id) REFERENCES natural_person(id) DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT check_customer_id CHECK (
        (customer_category = 'Юр. лицо' AND customer_id IS NOT NULL) OR
        (customer_category = 'Физ. лицо' AND customer_id IS NOT NULL)
    )
);

-- Создание таблицы waybill
CREATE TABLE waybill (
    id SERIAL PRIMARY KEY,
    article_product VARCHAR(255) REFERENCES product(article),
    product_quantity INTEGER,
    orders_number INTEGER REFERENCES orders(order_number),
    doc_number INTEGER
);

-- Создание таблицы Client для юбилеев
CREATE TABLE Client (
    client_id SERIAL PRIMARY KEY,
    second_name VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    date_of_birth DATE NOT NULL
);

-- Заполнение таблицы natural_person
INSERT INTO natural_person (passport, forename, phone, email, delivery_address)
VALUES 
('AB1234567', 'Иван Иванов', '1234567890', 'ivanov@mail.com', 'г. Москва, ул. Ленина, д. 1'),
('CD2345678', 'Петр Петров', '1234567891', 'petrov@mail.com', 'г. Казань, ул. Гагарина, д. 2'),
('EF3456789', 'Сергей Сергеев', '1234567892', 'sergeev@mail.com', 'г. Новосибирск, ул. Мира, д. 3'),
('GH4567890', 'Алексей Алексеев', '1234567893', 'alekseev@mail.com', 'г. Омск, ул. Победы, д. 4'),
('IJ5678901', 'Дмитрий Дмитриев', '1234567894', 'dmitriev@mail.com', 'г. Санкт-Петербург, ул. Звездная, д. 5'),
('KL6789012', 'Олег Олегов', '1234567895', 'olegov@mail.com', 'г. Екатеринбург, ул. Лесная, д. 6'),
('MN7890123', 'Николай Николаев', '1234567896', 'nikolaev@mail.com', 'г. Владивосток, ул. Горького, д. 7'),
('OP8901234', 'Андрей Андреев', '1234567897', 'andreev@mail.com', 'г. Хабаровск, ул. Труда, д. 8'),
('QR9012345', 'Юрий Юрьев', '1234567898', 'yuriev@mail.com', 'г. Красноярск, ул. Шоссейная, д. 9'),
('ST0123456', 'Владимир Владимиров', '1234567899', 'vladimirov@mail.com', 'г. Иркутск, ул. Свободы, д. 10');

-- Заполнение таблицы legal_person
INSERT INTO legal_person (inn, name, phone, email, delivery_address, representative_forename)
VALUES 
('1234567890', 'ООО Альфа', '2345678901', 'alpha@company.com', 'г. Москва, ул. Первомайская, д. 1', 'Ольга Смирнова'),
('2345678901', 'ООО Бета', '2345678902', 'beta@company.com', 'г. Казань, ул. Центральная, д. 2', 'Игорь Попов'),
('3456789012', 'ООО Гамма', '2345678903', 'gamma@company.com', 'г. Новосибирск, ул. Молодежная, д. 3', 'Екатерина Лебедева'),
('4567890123', 'ООО Дельта', '2345678904', 'delta@company.com', 'г. Омск, ул. Городская, д. 4', 'Сергей Морозов'),
('5678901234', 'ООО Эпсилон', '2345678905', 'epsilon@company.com', 'г. Санкт-Петербург, ул. Комсомольская, д. 5', 'Анна Иванова'),
('6789012345', 'ООО Зета', '2345678906', 'zeta@company.com', 'г. Екатеринбург, ул. Зеленая, д. 6', 'Алексей Петров'),
('7890123456', 'ООО Эта', '2345678907', 'eta@company.com', 'г. Владивосток, ул. Парковая, д. 7', 'Дмитрий Федоров'),
('8901234567', 'ООО Тета', '2345678908', 'theta@company.com', 'г. Хабаровск, ул. Пролетарская, д. 8', 'Юлия Кузнецова'),
('9012345678', 'ООО Иота', '2345678909', 'iota@company.com', 'г. Красноярск, ул. Академическая, д. 9', 'Артем Смирнов'),
('0123456789', 'ООО Каппа', '2345678910', 'kappa@company.com', 'г. Иркутск, ул. Северная, д. 10', 'Владимир Николаев');

-- Заполнение таблицы provider
INSERT INTO provider (inn, name, address)
VALUES 
('1111111111', 'Поставщик 1', 'г. Москва, ул. Главная, д. 1'),
('2222222222', 'Поставщик 2', 'г. Казань, ул. Южная, д. 2'),
('3333333333', 'Поставщик 3', 'г. Новосибирск, ул. Восточная, д. 3'),
('4444444444', 'Поставщик 4', 'г. Омск, ул. Северная, д. 4'),
('5555555555', 'Поставщик 5', 'г. Санкт-Петербург, ул. Западная, д. 5'),
('6666666666', 'Поставщик 6', 'г. Екатеринбург, ул. Прямая, д. 6'),
('7777777777', 'Поставщик 7', 'г. Владивосток, ул. Лунная, д. 7'),
('8888888888', 'Поставщик 8', 'г. Хабаровск, ул. Речная, д. 8'),
('9999999999', 'Поставщик 9', 'г. Красноярск, ул. Тихая, д. 9'),
('1010101010', 'Поставщик 10', 'г. Иркутск, ул. Солнечная, д. 10');

-- Заполнение таблицы product
INSERT INTO product (place, provider_id, provider_name, name, receipt_date, article, quantity, price, weight)
VALUES 
(1, 1, 'Поставщик 1', 'Товар 1', '2024-01-01', 'A001', 100, 500.00, 10.50),
(2, 2, 'Поставщик 2', 'Товар 2', '2024-01-02', 'A002', 200, 600.00, 20.50),
(3, 3, 'Поставщик 3', 'Товар 3', '2024-01-03', 'A003', 300, 700.00, 30.50),
(4, 4, 'Поставщик 4', 'Товар 4', '2024-01-04', 'A004', 400, 800.00, 40.50),
(5, 5, 'Поставщик 5', 'Товар 5', '2024-01-05', 'A005', 500, 900.00, 50.50),
(6, 6, 'Поставщик 6', 'Товар 6', '2024-01-06', 'A006', 600, 1000.00, 60.50),
(7, 7, 'Поставщик 7', 'Товар 7', '2024-01-07', 'A007', 700, 1100.00, 70.50),
(8, 8, 'Поставщик 8', 'Товар 8', '2024-01-08', 'A008', 800, 1200.00, 80.50),
(9, 9, 'Поставщик 9', 'Товар 9', '2024-01-09', 'A009', 900, 1300.00, 90.50),
(10, 10, 'Поставщик 10', 'Товар 10', '2024-01-10', 'A010', 1000, 1400.00, 100.50);

-- Заполнение таблицы orders
INSERT INTO orders (order_number, weight, registration_date, cost, customer_id, customer_category)
VALUES 
(1001, 50.00, '2024-11-01', 15000.00, 1, 'Физ. лицо'),
(1002, 30.00, '2024-11-02', 9000.00, 2, 'Физ. лицо'),
(1003, 70.00, '2024-11-03', 21000.00, 3, 'Физ. лицо'),
(1004, 45.00, '2024-11-04', 13500.00, 4, 'Физ. лицо'),
(1005, 25.00, '2024-11-05', 7500.00, 5, 'Физ. лицо'),
(1006, 60.00, '2024-11-06', 18000.00, 6, 'Юр. лицо'),
(1007, 80.00, '2024-11-07', 24000.00, 7, 'Юр. лицо'),
(1008, 55.00, '2024-11-08', 16500.00, 8, 'Юр. лицо'),
(1009, 35.00, '2024-11-09', 10500.00, 9, 'Юр. лицо'),
(1010, 65.00, '2024-11-10', 19500.00, 10, 'Юр. лицо');

-- Заполнение таблицы waybill
INSERT INTO waybill (article_product, product_quantity, orders_number, doc_number)
VALUES 
('A001', 10, 1001, 501),
('A002', 5, 1002, 502),
('A003', 7, 1003, 503),
('A004', 9, 1004, 504),
('A005', 4, 1005, 505),
('A006', 12, 1006, 506),
('A007', 8, 1007, 507),
('A008', 6, 1008, 508),
('A009', 11, 1009, 509),
('A010', 3, 1010, 510);

-- Заполнение таблицы Client
INSERT INTO Client (second_name, name, date_of_birth) VALUES
('Иванов', 'Иван', '1955-12-19'),
('Петров', 'Петр', '1956-12-23'),
('Сидоров', 'Николай', '1957-12-09'),
('Кузнецов', 'Сергей', '1958-12-02'),
('Смирнов', 'Алексей', '1962-12-02'),
('Васильев', 'Василий', '1964-12-28'),
('Павлов', 'Павел', '1965-12-17'),
('Семенов', 'Семен', '1966-12-14'),
('Голубев', 'Глеб', '1967-12-11'),
('Виноградов', 'Виктор', '1968-12-24'),
('Богданов', 'Борис', '1970-12-05'),
('Воробьев', 'Валерий', '1971-12-21'),
('Федоров', 'Федор', '1972-12-18'),
('Михайлов', 'Михаил', '1973-12-07'),
('Беляев', 'Белла', '1974-12-20'),
('Тарасов', 'Тарас', '1976-12-13'),
('Белов', 'Борислав', '1977-12-03'),
('Комаров', 'Константин', '1978-12-22'),
('Орлов', 'Орест', '1980-12-01'),
('Киселев', 'Кирилл', '1981-12-26'),
('Макаров', 'Макар', '1982-12-15'),
('Андреев', 'Андрей', '1984-12-09'),
('Ковалев', 'Константин', '1985-12-02'),
('Ильин', 'Илья', '1986-12-25'),
('Гусев', 'Геннадий', '1988-12-19'),
('Титов', 'Тимофей', '1989-12-12'),
('Кузьмин', 'Кузьма', '1990-12-06'),
('Кудрявцев', 'Кузьма', '1993-12-18'),
('Баранов', 'Борис', '1995-12-21'),
('Куликов', 'Кирилл', '1998-12-24');

-- 1. Запрос на полную выборку данных
SELECT * FROM provider;

-- 2. Запрос на выборку данных без повторений
SELECT DISTINCT inn, name, address FROM provider;

-- 3. Запрос на выборку первых 10 записей
SELECT * FROM provider LIMIT 10;

-- 4. Запрос на выборку последних 15 записей
SELECT * FROM Client ORDER BY date_of_birth DESC LIMIT 15;

-- 5. Запросы на выполнение функций Average, Max, Min
SELECT 
    AVG(price) AS average_price,
    MAX(quantity) AS max_quantity,
    MIN(weight) AS min_weight
FROM product;

-- 6.1 Запрос на возвращение кортежа по первичному ключу
SELECT * FROM natural_person WHERE id = 1;

-- 6.2 Запросы на возвращение значений по условиям больше, меньше и между
SELECT * FROM product WHERE quantity > 500;
SELECT * FROM product WHERE price < 1000;
SELECT * FROM product WHERE weight BETWEEN 10 AND 50;

-- 6.3 Запросы с использованием оператора LIKE и ESCAPE
SELECT * FROM natural_person WHERE forename LIKE '%ов%';
SELECT * FROM natural_person WHERE delivery_address LIKE '%ул/.__о%' ESCAPE '/';

-- 6.4 Запросы со сложным условием (И, ИЛИ, НЕ, EXISTS)
SELECT * 
FROM product 
WHERE (weight > 50 OR receipt_date > '2024-01-05') AND quantity > 500;

SELECT * 
FROM waybill 
WHERE product_quantity != 0;

SELECT * 
FROM product p 
WHERE EXISTS (
    SELECT 1 
    FROM waybill w 
    WHERE w.article_product = p.article
);

-- 6.5 Запрос с использованием NOT NULL
SELECT * FROM natural_person WHERE phone IS NOT NULL;

-- 7. Запрос с условиями IN или BETWEEN
SELECT * FROM product WHERE price IN (550.00, 770.00, 990.00);
SELECT * FROM product WHERE price BETWEEN 600.00 AND 1000.00;

-- 8. Запросы с сортировкой по нескольким полям
SELECT * FROM product ORDER BY name ASC, price DESC;

-- 9. Запросы с групповыми операциями
SELECT 
    provider_id, 
    SUM(price * quantity) AS total_value
FROM product 
GROUP BY provider_id;

SELECT 
    provider_id, 
    SUM(price * quantity) AS total_value
FROM product 
GROUP BY provider_id 
HAVING SUM(price * quantity) > 200000;

-- 10. Запрос с операцией над множествами
SELECT email 
FROM natural_person 
UNION 
SELECT email 
FROM legal_person 
ORDER BY email ASC;

-- 11. Запросы на обновление
UPDATE natural_person 
SET email = 'new_email@example.com' 
WHERE id = 1;

UPDATE provider 
SET address = 'New Address' 
WHERE id = 1;

-- 12. Запросы на удаление
-- Удаляем связанные заказы перед удалением физ. лица
DELETE FROM orders 
WHERE customer_id = 1 AND customer_category = 'Физ. лицо';
DELETE FROM natural_person 
WHERE id = 1;

-- Удаляем связанные товары перед удалением поставщика
DELETE FROM product 
WHERE provider_id IN (SELECT id FROM provider WHERE id IN (1, 2, 3));
DELETE FROM provider 
WHERE id IN (1, 2, 3);

-- 13. Запросы на вставку
INSERT INTO legal_person (inn, name, phone, email, delivery_address, representative_forename) 
VALUES ('789456123', 'OOO SNG', '79095273752', 'email@email.com', 'surgut', 'Ivanov');

INSERT INTO natural_person (passport, forename, phone, email, delivery_address) 
VALUES ('4894165', 'Komarov', '79084893526', 'email@email.com', 'minsk');

-- 14. Запрос на отображение юбилеев в декабре 2025
SELECT 
    CONCAT(second_name, ' ', LEFT(name, 1), '.') AS "ФИО",
    EXTRACT(YEAR FROM AGE('2025-12-01', date_of_birth)) AS "Возраст",
    date_of_birth AS "Дата рождения",
    MAKE_DATE(
        2025,
        12,
        EXTRACT(DAY FROM date_of_birth)::INTEGER
    ) AS "Дата юбилея"
FROM Client
WHERE EXTRACT(YEAR FROM AGE('2025-12-01', date_of_birth)) % 5 = 0
AND EXTRACT(MONTH FROM date_of_birth) = 12;