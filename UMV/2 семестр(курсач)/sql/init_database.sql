PRAGMA foreign_keys = ON;

CREATE TABLE Поставщик (
    ID_Поставщика INTEGER PRIMARY KEY AUTOINCREMENT,
    ИНН TEXT UNIQUE NOT NULL,
    Название TEXT NOT NULL,
    Адрес TEXT NOT NULL,
    Контактное_Лицо TEXT,
    Банковские_Реквизиты TEXT
);

CREATE TABLE Место_Хранения (
    ID_Места INTEGER PRIMARY KEY AUTOINCREMENT,
    Зона TEXT NOT NULL,
    Стеллаж TEXT NOT NULL,
    Ячейка TEXT NOT NULL
);

CREATE TABLE Заказчик (
    ID_Заказчика INTEGER PRIMARY KEY AUTOINCREMENT,
    Тип_Заказчика TEXT NOT NULL CHECK(Тип_Заказчика IN ('Физическое', 'Юридическое')),
    ФИО TEXT NOT NULL,
    Email TEXT,
    Номер_Телефона TEXT,
    Адрес_Доставки TEXT NOT NULL,
    Серия_Номер_Паспорта TEXT,
    ИНН TEXT,
    Название TEXT,
    КПП TEXT,
    CONSTRAINT unique_inn UNIQUE (ИНН),
    CONSTRAINT unique_passport UNIQUE (Серия_Номер_Паспорта)
);

CREATE TABLE Пользователь (
    ID_Пользователя INTEGER PRIMARY KEY AUTOINCREMENT,
    ФИО TEXT NOT NULL,
    Роль TEXT NOT NULL CHECK(Роль IN ('Кладовщик', 'Менеджер', 'Администратор')),
    Логин TEXT UNIQUE NOT NULL,
    Пароль TEXT NOT NULL,
    Email TEXT
);

CREATE TABLE Товар (
    ID_Товара INTEGER PRIMARY KEY AUTOINCREMENT,
    Артикул TEXT UNIQUE NOT NULL,
    Наименование TEXT NOT NULL,
    ID_Поставщика INTEGER NOT NULL,
    ID_Места INTEGER NOT NULL,
    Цена_За_Единицу DECIMAL(10,2) NOT NULL,
    Дата_Поступления DATE NOT NULL,
    Количество_На_Складе INTEGER NOT NULL,
    Масса_Единицы DECIMAL(10,2) NOT NULL,
    Единица_Измерения TEXT,
    Категория_Товара TEXT,
    FOREIGN KEY (ID_Поставщика) REFERENCES Поставщик(ID_Поставщика),
    FOREIGN KEY (ID_Места) REFERENCES Место_Хранения(ID_Места)
);

CREATE TABLE Заказ (
    ID_Заказа INTEGER PRIMARY KEY AUTOINCREMENT,
    Номер_Заказа TEXT UNIQUE NOT NULL,
    Дата_Оформления DATE NOT NULL,
    ID_Заказчика INTEGER NOT NULL,
    ID_Пользователя INTEGER NOT NULL,
    Статус_Заказа TEXT,
    Дата_Доставки DATE,
    FOREIGN KEY (ID_Заказчика) REFERENCES Заказчик(ID_Заказчика),
    FOREIGN KEY (ID_Пользователя) REFERENCES Пользователь(ID_Пользователя)
);

CREATE TABLE Детали_Заказа (
    ID_Детали INTEGER PRIMARY KEY AUTOINCREMENT,
    ID_Заказа INTEGER NOT NULL,
    ID_Товара INTEGER NOT NULL,
    Количество INTEGER NOT NULL,
    Цена_За_Единицу DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (ID_Заказа) REFERENCES Заказ(ID_Заказа),
    FOREIGN KEY (ID_Товара) REFERENCES Товар(ID_Товара)
);

CREATE TABLE Накладная (
    ID_Накладной INTEGER PRIMARY KEY AUTOINCREMENT,
    Номер_Документа TEXT UNIQUE NOT NULL,
    Дата_Составления DATE NOT NULL,
    ID_Заказа INTEGER NOT NULL,
    ID_Пользователя INTEGER NOT NULL,
    Статус_Накладной TEXT,
    FOREIGN KEY (ID_Заказа) REFERENCES Заказ(ID_Заказа),
    FOREIGN KEY (ID_Пользователя) REFERENCES Пользователь(ID_Пользователя)
);

CREATE TABLE Детали_Накладной (
    ID_Детали INTEGER PRIMARY KEY AUTOINCREMENT,
    ID_Накладной INTEGER NOT NULL,
    ID_Товара INTEGER NOT NULL,
    Количество INTEGER NOT NULL,
    FOREIGN KEY (ID_Накладной) REFERENCES Накладная(ID_Накладной),
    FOREIGN KEY (ID_Товара) REFERENCES Товар(ID_Товара)
);