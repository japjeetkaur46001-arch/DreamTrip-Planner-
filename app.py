from flask import Flask
from database import get_connection

app = Flask(__name__)

@app.route("/")
def home():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM destinations;")
        destinations = cur.fetchall()

        cur.close()
        conn.close()

        return f"<h2>Connected Successfully!</h2><pre>{destinations}</pre>"

    except Exception as e:
        return f"Database Error:<br>{e}"

if __name__ == "__main__":
    app.run(debug=True)
    