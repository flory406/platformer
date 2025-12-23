import sqlite3

def create_db():
    db = sqlite3.connect("score.db")
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS records(name TEXT, score INTEGER)")
    db.commit()
    db.close()

def add_zero():
    db = sqlite3.connect("score.db")
    cursor = db.cursor()
    cursor.execute("INSERT INTO records (name, score) VALUES ('Flory', 0)")
    db.commit()
    db.close()
    print("Нуль додано!")

def get_best_score():
    db = sqlite3.connect("score.db")
    cursor = db.cursor()
    cursor.execute("SELECT score FROM records WHERE name = 'Flory'")
    record = cursor.fetchone() 
    db.close()

    if record:
        return record[0] 
    else:
        return 0

def save_score(new_val):
    old_best = get_best_score()
    if new_val > old_best:
        db = sqlite3.connect("score.db")
        cursor = db.cursor()
        cursor.execute(f"UPDATE records SET score = {new_val} WHERE name = 'Flory'")
        db.commit()
        db.close()
        return True 
    return False

create_db() 

print("Зараз рекорд:", get_best_score())

if save_score(500):
    print("Новий рекорд встановлено!")
else:
    print("Не дотягнув до рекорду.")

print("А тепер рекорд:", get_best_score())