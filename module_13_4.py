import sqlite3

# Подключение к базе данных
connection = sqlite3.connect("babax.db")
cursor = connection.cursor()

# Создание таблицы Users
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER,
    balance INTEGER NOT NULL
)
''')

# Очистка таблицы (для тестов)
cursor.execute("DELETE FROM Users")

# Заполнение таблицы 10 записями
users = [
    (f"User{i}", f"example{i}@gmail.com", i * 10, 1000) for i in range(1, 11)
]
cursor.executemany("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)", users)

# Обновление balance у каждой 2-й записи начиная с 1-й на 500
cursor.execute("UPDATE Users SET balance = 500 WHERE id % 2 = 1")

# Удаление каждой 3-й записи начиная с 1-й
ids_to_delete = [row[0] for row in cursor.execute("SELECT id FROM Users").fetchall() if (row[0] - 1) % 3 == 0]
cursor.executemany("DELETE FROM Users WHERE id = ?", [(id_,) for id_ in ids_to_delete])

# Выборка всех записей, где возраст не равен 60
result = cursor.execute("SELECT username, email, age, balance FROM Users WHERE age != 60").fetchall()

# Вывод данных в заданном формате
for user in result:
    print(f"Имя: {user[0]} | Почта: {user[1]} | Возраст: {user[2]} | Баланс: {user[3]}")

# Закрытие соединения
connection.commit()
connection.close()
