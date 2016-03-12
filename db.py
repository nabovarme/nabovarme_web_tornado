import rethinkdb as r

db_name = "nabovarme"
table_names = ["samples", "meters"]
r.connect("localhost", 32768).repl()
try:
    print r.db_create(db_name).run()
except Exception:
    pass

for t_n in table_names:
    try:
        print r.db(db_name).table_create(t_n).run()
    except Exception:
        pass
