import sqlite3

conn = sqlite3.connect('media.db')
c = conn.cursor()


c.execute("DELETE FROM books")
c.execute("DELETE FROM manga")
c.execute("DELETE FROM comics")

books = [
    ("фэнтези", "Властелин колец – Дж.Р.Р. Толкин", "https://upload.wikimedia.org/wikipedia/ru/thumb/9/92/The_Lord_of_the_Rings_%282021%29.jpg/500px-The_Lord_of_the_Rings_%282021%29.jpg"),
    ("детектив", "Шерлок Холмс – Артур Конан Дойл", "https://upload.wikimedia.org/wikipedia/commons/c/cd/Sherlock_Holmes_Portrait_Paget.jpg"),
    ("романтика", "Анна Каренина – Лев Толстой", "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/AnnaKareninaTitle.jpg/375px-AnnaKareninaTitle.jpg"),
]

manga = [
    ("боевик", "Attack on Titan – Hajime Isayama", "https://upload.wikimedia.org/wikipedia/ru/d/d2/Shingeki_no_Kyojin.jpg"),
    ("романтика", "Your Lie in April – Naoshi Arakawa", "https://upload.wikimedia.org/wikipedia/en/d/de/Your_Lie_in_April_Manga_cover.png"),
]

comics = [
    ("супергерои", "Batman: Year One – Frank Miller", "https://upload.wikimedia.org/wikipedia/en/b/b1/Batman_vol._1-404_%28January_1987%29.jpg"),
    ("драма", "Maus – Art Spiegelman", "https://upload.wikimedia.org/wikipedia/ru/9/98/Maus.jpg"),
]

audiobooks = [
    ("фэнтези", "Гарри Поттер и философский камень – Дж. К. Роулинг",
     "https://www.sample-videos.com/audio/mp3/crowd-cheering.mp3", 
     "C:/Users/админ/Desktop/daddy/game/Bot/123"),

    ("детектив", "Шерлок Холмс – Артур Конан Дойл",
     "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
     "C:/Users/админ/Desktop/daddy/game/Bot/456")
]

c.executemany("INSERT INTO audiobooks (genre, title, audio_url, image_url) VALUES (?, ?, ?, ?)", audiobooks)

# Запись данных
for genre, title, img in books:
    c.execute("INSERT INTO books (genre, title, image_url) VALUES (?, ?, ?)", (genre.lower(), title, img))

for genre, title, img in manga:
    c.execute("INSERT INTO manga (genre, title, image_url) VALUES (?, ?, ?)", (genre.lower(), title, img))

for genre, title, img in comics:
    c.execute("INSERT INTO comics (genre, title, image_url) VALUES (?, ?, ?)", (genre.lower(), title, img))

conn.commit()
conn.close()

print("✅ Данные с изображениями добавлены.")
