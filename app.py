from flask import Flask, render_template, request, redirect
from database import get_connection

app = Flask(__name__)

# ---------------- DATABASE FUNCTIONS ---------------- #

def get_all_destinations(search="", status="", sort_by=""):
    conn = get_connection()
    cur = conn.cursor()

    query = "SELECT * FROM destinations WHERE 1=1"
    values = []

    if search:
        query += " AND destination ILIKE %s"
        values.append(f"%{search}%")

    if status:
        query += " AND status = %s"
        values.append(status)
    if sort_by == "budget_low":
        query += " ORDER BY budget ASC"

    elif sort_by == "budget_high":
        query += " ORDER BY budget DESC"

    elif sort_by == "destination":
        query += " ORDER BY destination ASC"

    else:
        query += " ORDER BY id"
    cur.execute(query, values)
    destinations = cur.fetchall()
    
    cur.close()
    conn.close()
        
    return destinations


def add_destination_db(destination, country, budget, priority, status):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO destinations
        (destination, country, budget, priority, status)
        VALUES (%s, %s, %s, %s, %s);
    """, (destination, country, budget, priority, status))

    conn.commit()

    cur.close()
    conn.close()


def update_destination_db(id, destination, country, budget, priority, status):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE destinations
        SET destination=%s,
            country=%s,
            budget=%s,
            priority=%s,
            status=%s
        WHERE id=%s;
    """, (
        destination,
        country,
        budget,
        priority,
        status,
        id
    ))

    conn.commit()

    cur.close()
    conn.close()


def delete_destination_db(id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM destinations WHERE id=%s;",
        (id,)
    )

    conn.commit()

    cur.close()
    conn.close()


def get_dashboard_stats():

    conn = get_connection()
    cur = conn.cursor()

    # Total Destinations
    cur.execute("SELECT COUNT(*) FROM destinations;")
    total = cur.fetchone()[0]

    # Visited Trips
    cur.execute("SELECT COUNT(*) FROM destinations WHERE status='Visited';")
    visited = cur.fetchone()[0]

    # High Priority Trips
    cur.execute("SELECT COUNT(*) FROM destinations WHERE priority='High';")
    high_priority = cur.fetchone()[0]

    # Total Budget
    cur.execute("SELECT COALESCE(SUM(budget),0) FROM destinations;")
    total_budget = cur.fetchone()[0]

    cur.close()
    conn.close()

    return {
        "total": total,
        "visited": visited,
        "high_priority": high_priority,
        "total_budget": total_budget
    }

def get_budget_statistics():

    conn = get_connection()
    cur = conn.cursor()

    # Average Budget
    cur.execute("""
        SELECT COALESCE(AVG(budget),0)
        FROM destinations;
    """)
    average_budget = round(cur.fetchone()[0], 2)

    # Highest Budget
    cur.execute("""
        SELECT COALESCE(MAX(budget),0)
        FROM destinations;
    """)
    highest_budget = cur.fetchone()[0]

    # Lowest Budget
    cur.execute("""
        SELECT COALESCE(MIN(budget),0)
        FROM destinations;
    """)
    lowest_budget = cur.fetchone()[0]

    cur.close()
    conn.close()

    return {
        "average_budget": average_budget,
        "highest_budget": highest_budget,
        "lowest_budget": lowest_budget
    }

# ---------------- HOME ---------------- #

@app.route("/")
def home():

    search = request.args.get("search", "")
    status = request.args.get("status", "")
    sort_by = request.args.get("sort_by", "")

    destinations = get_all_destinations(search, status, sort_by)

    stats = get_dashboard_stats()

    budget_stats = get_budget_statistics()

    return render_template(
    "index.html",
    destinations=destinations,
    search=search,
    status=status,
    stats=stats,
    budget_stats=budget_stats,
    sort_by=sort_by,
)


# ---------------- ADD DESTINATION ---------------- #

@app.route("/add", methods=["GET", "POST"])
def add_destination():

    if request.method == "POST":

        destination = request.form["destination"]
        country = request.form["country"]
        budget = request.form["budget"]
        priority = request.form["priority"]
        status = request.form["status"]

        # Validation

        if destination.strip() == "":
            return "Destination cannot be empty!"

        if country.strip() == "":
            return "Country cannot be empty!"

        if float(budget) < 0:
            return "Budget cannot be negative!"

        add_destination_db(
            destination,
            country,
            budget,
            priority,
            status
        )

        return redirect("/")

    return render_template("add_destination.html")


# ---------------- EDIT DESTINATION ---------------- #

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_destination(id):

    if request.method == "POST":

        destination = request.form["destination"]
        country = request.form["country"]
        budget = request.form["budget"]
        priority = request.form["priority"]
        status = request.form["status"]

        update_destination_db(
            id,
            destination,
            country,
            budget,
            priority,
            status
        )

        return redirect("/")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM destinations WHERE id=%s;",
        (id,)
    )

    destination = cur.fetchone()

    cur.close()
    conn.close()

    return render_template(
        "edit_destination.html",
        destination=destination
    )


# ---------------- DELETE DESTINATION ---------------- #

@app.route("/delete/<int:id>")
def delete_destination(id):

    delete_destination_db(id)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)