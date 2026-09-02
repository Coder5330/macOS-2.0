from flask import *
import os
import sqlite3

app = Flask(__name__)

DATABASE_LOCATION = "app.db"

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE_LOCATION)
        g.db.row_factory = sqlite3.Row

    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)

    if db is not None:
        db.close()


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

with app.app_context():
    init_db()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/new_file", methods=["POST"])
def new_file():
    payload = request.get_json(silent=True) or request.form

    filename = payload.get("filename")
    data = payload.get("data")

    if not filename or data is None:
        return jsonify(error="filename and data are required"), 400

    conn = get_db()

    cursor = conn.execute(
        "INSERT INTO files (filename, data) VALUES (?, ?)",
        (filename, data)
    )

    conn.commit()

    return jsonify(id=cursor.lastrowid, filename=filename), 201

if __name__ == "__main__":
    app.run(port=8080, debug=os.environ.get("FLASK_DEBUG") == "1")
