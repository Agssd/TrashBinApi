from ..db import get_db
from fastapi import HTTPException

def get_user_by_login(login: str):
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "SELECT id, username, login, points FROM users WHERE login = ?",
        (login,),
    )
    row = c.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "username": row[1], "login": row[2], "points": row[3]}
    raise HTTPException(status_code=404, detail="User not found")

def update_user_points(login: str, points: int):
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "UPDATE users SET points = points + ? WHERE login = ?",
        (points, login),
    )
    if c.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    conn.commit()
    conn.close()
