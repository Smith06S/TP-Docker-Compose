import mysql.connector
import pymongo
import os
import time  # Ajouté pour gérer les délais
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_mysql_conn():
    """Tente de se connecter à MySQL avec plusieurs essais en cas d'échec."""
    attempts = 0
    while attempts < 5:
        try:
            connection = mysql.connector.connect(
                database=os.getenv("MYSQL_DATABASE"),
                user=os.getenv("MYSQL_USER"),
                password=os.getenv("MYSQL_PASSWORD"),
                port=3306,
                host=os.getenv("MYSQL_HOST")
            )
            if connection.is_connected():
                return connection
        except mysql.connector.Error as err:
            print(f"Erreur de connexion MySQL: {err}. Nouvel essai dans 2s...")
            time.sleep(2)
            attempts += 1
    return None

mongo_client = pymongo.MongoClient(
    host=os.getenv("MONGO_HOST"),
    username=os.getenv("MONGO_INITDB_ROOT_USERNAME"),
    password=os.getenv("MONGO_INITDB_ROOT_PASSWORD"),
    port=27017
)
DATABASE_NAME = os.getenv("MONGO_INITDB_DATABASE", "blog_db")
mongo_db = mongo_client[DATABASE_NAME]


@app.get("/users")
async def get_users():
    conn = get_mysql_conn()
    if not conn:
        return JSONResponse(content={"error": "MySQL indisponible"}, status_code=503)
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM utilisateurs")
        records = cursor.fetchall()
        return {'utilisateurs': records}
    finally:
        cursor.close()
        conn.close() 

@app.get("/posts")
async def get_posts():
    posts = list(mongo_db.posts.find({}, {"_id": 0}))
    return {"posts": posts}

@app.get("/health")
async def health():
    # Vérification MySQL
    conn = get_mysql_conn()
    mysql_status = "OK" if conn and conn.is_connected() else "DOWN"
    if conn: conn.close()

    # Vérification MongoDB
    try:
        mongo_client.admin.command('ping')
        mongo_status = "OK"
    except:
        mongo_status = "DOWN"

    status_code = 200 if mysql_status == "OK" and mongo_status == "OK" else 500
    return JSONResponse(
        content={"mysql": mysql_status, "mongodb": mongo_status},
        status_code=status_code
    )