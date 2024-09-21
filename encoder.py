import sqlite3
import pickle

a = []
new_con = sqlite3.connect("data/bd.sqlite")
new_cur = new_con.cursor()
res = new_cur.execute(
    "SELECT id, tip, question, answer_one, answer_two, answer_three, answer_four FROM Task").fetchall()
for i in res:
    state = {
        'id': str(i[0]).encode(),
        'tip': str(i[1]).encode(),
        'question': i[2].encode(),
        'answer_one': i[3].encode(),
        'answer_two': i[4].encode(),
        'answer_three': i[5].encode(),
        'answer_four': i[6].encode()
    }
    a.append(state)

new_con.close()

print(a)
with open('data/game_db.pkl', 'wb') as f:
    pickle.dump(a, f)
