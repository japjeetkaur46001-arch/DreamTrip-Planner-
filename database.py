import psycopg2

def get_connection():
    connection = psycopg2.connect(
        host="localhost",
        database="DreamTrip Planner",
        user="postgres",
        password="Iphone@46001",
        port="2831"
    )
    return connection
