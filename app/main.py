from fastapi import FastAPI
import os
import psycopg2

app = FastAPI()

@app.get("/")
def read_root():
    return {"msg": "FastAPI working inside Docker!"}

@app.get("/db")
def db_check():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            dbname=os.getenv("DB_NAME")
        )
        return {"status": "Connected to PostgreSQL"}
    except:
        return {"status": "DB Connection Failed"}

