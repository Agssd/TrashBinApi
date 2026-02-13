from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
import sqlite3
from app.db import get_db

router = APIRouter(prefix="/trash-bins", tags=["trash-bins"])

@router.get("/nearby-trash-bins")
async def get_nearby_trash_bins(
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude"), 
    radius: float = Query(2000, description="Search radius")
):
    db = sqlite3.connect("app/database.db")
    cursor = db.cursor()
    
    # ✅ rowid вместо id (всегда работает!)
    cursor.execute("""
        SELECT rowid, name, latitude, longitude, district 
        FROM trash_bins 
        WHERE latitude BETWEEN ?-0.01 AND ?+0.01 
          AND longitude BETWEEN ?-0.01 AND ?+0.01
        ORDER BY 
            (6371000 * acos(cos(radians(?)) * cos(radians(latitude)) * 
                           cos(radians(longitude) - radians(?)) + 
                           sin(radians(?)) * sin(radians(latitude))))
        LIMIT 20
    """, (lat, lat, lng, lng, lat, lng, lat))
    
    result = [
        {
            "id": r[0],           # rowid → id
            "name": r[1] or "Без названия",
            "lat": float(r[2]),   # latitude
            "lng": float(r[3]),   # longitude  
            "district": r[4] or "Неизвестно"
        }
        for r in cursor.fetchall()
    ]
    
    print(f"Вернули {len(result)} мусорок для {lat}, {lng}")
    db.close()
    return result
 
class BinRequest(BaseModel):
    bin_id: int

@router.post("/bins/can-scan")
async def can_scan_bin(request: BinRequest):
    db = sqlite3.connect("app/database.db")
    cursor = db.cursor()
    
    # Тестовый user_id = 1
    user_id = 1
    cursor.execute("""
        SELECT scanned_at FROM scanned_bins 
        WHERE bin_id = ? AND user_id = ? 
        AND scanned_at > datetime('now', '-1 day')
    """, (request.bin_id, user_id))
    
    result = cursor.fetchone()
    db.close()
    
    if result:
        return {"can_scan": False, "message": "🔒 Уже сфоткал сегодня!"}
    return {"can_scan": True, "message": "📸 Можно сфоткать!"}

@router.post("/bins/mark-scanned")
async def mark_bin_scanned(request: BinRequest):
    db = sqlite3.connect("app/database.db")
    cursor = db.cursor()
    
    # Тестовый user_id = 1
    user_id = 1
    cursor.execute("""
        INSERT OR REPLACE INTO scanned_bins (bin_id, user_id, scanned_at)
        VALUES (?, ?, CURRENT_TIMESTAMP)
    """, (request.bin_id, user_id))
    
    db.commit()
    db.close()
    print(f"✅ Мусорка {request.bin_id} помечена!")
    return {"success": True}

    
    