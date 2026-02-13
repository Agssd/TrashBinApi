from ..db import get_db
from ..security import hash_password, verify_password, create_access_token, create_refresh_token
from fastapi import HTTPException

def register_user(username: str, login: str, password: str):
    conn = get_db()
    c = conn.cursor()
    try:
        password_hash = hash_password(password)
        c.execute(
            "INSERT INTO users (username, login, password) VALUES (?, ?, ?)",
            (username, login, password_hash)
        )
        conn.commit()
    except Exception as e:  # ← ТОЧНО 4 пробела отступ!
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Ошибка регистрации: {str(e)}")
    finally:
        conn.close()

def login_user(login: str, password: str) -> tuple[str, str]:
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE login = ?", (login,))
    result = c.fetchone()
    conn.close()
    if not result or not verify_password(password, result[0]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access = create_access_token(login)
    refresh = create_refresh_token(login)
    return access, refresh
