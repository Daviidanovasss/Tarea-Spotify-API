from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import mysql.connector
from configuration.conections import DatabaseConnection
from service.spotify import get_user_data


app = FastAPI()

@app.get("/")
def root():
    return {"Hello world"}

@app.get("/users")
async def get_users():
    mydb  = DatabaseConnection(host="localhost", user="root", password="Daviidcanovasss_300", database="spotifyProject")
    mydb_conn = await mydb.get_connection()
    mycursor = mydb_conn.cursor()
    mycursor.execute("SELECT * FROM users")
    data = mycursor.fetchall()
    return data

@app.post("/users")
async def post_users(request: Request):
    mydb  = DatabaseConnection(host="localhost", user="root", password="Daviidcanovasss_300", database="spotifyProject")
    mydb_conn = await mydb.get_connection()
    request = await request.json()
    username = request.get('username')
    favouriteArtist = request.get('favourite_artist')
    mycursor = mydb_conn.cursor()
    mycursor.execute(f"INSERT INTO users (username, favourite_artist) VALUES ('{username}', '{favouriteArtist}')")
    mydb_conn.commit()
    return JSONResponse(content={"message": "User added susccesfully"}, status_code = 201)
   

@app.delete("/users")
async def delete_user(id_user: int):
    mydb  = DatabaseConnection(host="localhost", user="root", password="Daviidcanovasss_300", database="spotifyProject")
    mydb_conn = await mydb.get_connection()
    mycursor = mydb_conn.cursor()
    mycursor.execute(f"SELECT id FROM users WHERE id = {id_user}")
    data = mycursor.fetchall()
    if data is None:
        return JSONResponse(content={"message": "User not found"})
    else:
        mycursor.execute(f"DELETE FROM users WHERE id = {id_user}")
        mydb_conn.commit()
        return JSONResponse(content={"message": "User deleted susccesfully"})
    

@app.put("/users/{user_id}")
async def put_user(user_id: int, request: Request):
    mydb  = DatabaseConnection(host="localhost", user="root", password="Daviidcanovasss_300", database="spotifyProject")
    mydb_conn = await mydb.get_connection()
    mycursor =  mydb_conn.cursor()
    user_data = await request.json()
    username = user_data.get("username")
    favourite_artist = user_data.get("favourite_artist")
    mycursor.execute(f"SELECT id FROM users WHERE id = {user_id}")
    data = mycursor.fetchall()
    if data is None:
        return JSONResponse(content={"message": "User not found"})
    else:
        mycursor.execute(f"UPDATE users SET username = '{username}', favourite_artist = '{favourite_artist}' WHERE id = {user_id}")
        mydb_conn.commit()
        return JSONResponse(content={"message": "User updated susccesfully"})

@app.get("/users/{user_id}")
async def get_data(user_id: str):
    user_data = get_user_data(user_id)
    if "error" in user_data:
        raise HTTPException(status_code=404, detail="User not found")
    return JSONResponse(content=user_data, status_code=200)