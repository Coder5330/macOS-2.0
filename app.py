from flask import *
import sqlite3

app = Flask(__name__)

DATABASE_LOCATION = "app.db"

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE_LOCATION)
        g.db.row_factory = sqlite3.Row

    return g.dbc


def init_db():
    db = get_db()

    db.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            data TEXT NOT NULL
        )
    """)

    db.commit()

init_db()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/new_file")
def new_file(filename, data):
    conn = get_db()

    conn.execute(
        "INSERT INTO files (filename, data) VALUES (?, ?)",
        (filename, data)
    )

    conn.commit()

app.run(port=8080, debug=True)