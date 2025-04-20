import sqlite3

conn = sqlite3.connect('media.db')
c = conn.cursor()

# Таблица книг
c.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        genre TEXT NOT NULL,
        title TEXT NOT NULL,
        image_url TEXT
    )
''')

# Таблица манги
c.execute('''
    CREATE TABLE IF NOT EXISTS manga (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        genre TEXT NOT NULL,
        title TEXT NOT NULL,
        image_url TEXT
    )
''')

# Таблица комиксов
c.execute('''
    CREATE TABLE IF NOT EXISTS comics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        genre TEXT NOT NULL,
        title TEXT NOT NULL,
        image_url TEXT
    )
''')

# Таблица аудиокниг
c.execute('''
    CREATE TABLE IF NOT EXISTS audiobooks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        genre TEXT NOT NULL,
        title TEXT NOT NULL,
        audio_url TEXT,
        image_url TEXT
    )
''')

conn.commit()
conn.close()
