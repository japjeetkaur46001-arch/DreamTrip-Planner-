# Project Setup

## Step 1

Install Python 3

## Step 2

Install PostgreSQL

## Step 3

Create Database

Database Name

```
DreamTrip Planner
```

## Step 4

Install Python Libraries

```bash
pip install flask
pip install psycopg2-binary
```

or

```bash
pip install -r requirements.txt
```

## Step 5

Update database.py

```python
host="localhost"
database="DreamTrip Planner"
user="postgres"
password="YOUR_PASSWORD"
port="YOUR_PORT"
```

## Step 6

Run

```bash
python app.py
```

Open

```
http://127.0.0.1:5000
```