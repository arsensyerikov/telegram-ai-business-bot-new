import sqlite3

# Підключення до БД
conn = sqlite3.connect("appointments.db")
cursor = conn.cursor()

# Створення таблиці
cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    service TEXT,
    datetime TEXT,
    phone TEXT
)
""")
conn.commit()

# Додавання запису
def add_appointment(name, service, datetime, phone):
    cursor.execute("INSERT INTO appointments (name, service, datetime, phone) VALUES (?, ?, ?, ?)",
                   (name, service, datetime, phone))
    conn.commit()

# Отримання всіх записів
def get_all_appointments():
    cursor.execute("SELECT * FROM appointments")
    return cursor.fetchall()

def clear_appointments():
    cursor.execute("DELETE FROM appointments")
    conn.commit()



# Створити таблицю, якщо не існує
cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY,
    telegram TEXT,
    whatsapp TEXT,
    instagram TEXT
)
""")
conn.commit()

# Оновити контакти
def update_contacts(telegram, whatsapp, instagram):
    cursor.execute("DELETE FROM contacts")
    cursor.execute("INSERT INTO contacts (id, telegram, whatsapp, instagram) VALUES (1, ?, ?, ?)",
                   (telegram, whatsapp, instagram))
    conn.commit()

# Отримати контакти
def get_contacts():
    cursor.execute("SELECT telegram, whatsapp, instagram FROM contacts WHERE id = 1")
    return cursor.fetchone()