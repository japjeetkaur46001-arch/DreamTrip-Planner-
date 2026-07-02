from flask import Flask, render_template
from database import get_connection

app = Flask(__name__)

@app.route("/")
def home():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM destinations")
    destinations = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "index.html",
        destinations=destinations
    )

if __name__ == "__main__":
    app.run(debug=True)