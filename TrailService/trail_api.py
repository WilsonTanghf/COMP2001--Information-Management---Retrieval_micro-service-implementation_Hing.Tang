from flask import request, jsonify
import pyodbc
import requests

AUTH_URL = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

def get_db():
    """Database connection factory"""
    return pyodbc.connect("""
    DRIVER={ODBC Driver 17 for SQL Server};
    SERVER=tcp:dist-6-505.uopnet.plymouth.ac.uk,1433;
    DATABASE=COMP2001_HK_HTang;
    UID=HK_HTang;
    PWD=i8acRQd3;
    Encrypt=yes;
    TrustServerCertificate=yes;
    Connection Timeout=30;
    """)

def convert_sql_types(obj):
    """Convert SQL types for JSON serialization"""
    if hasattr(obj, "total_seconds"):
        return str(obj)
    if str(type(obj)).startswith("<class 'decimal.Decimal'>"):
        return float(obj)
    return obj if obj is not None else None

def get_user_email(req):
    """Authenticate user via external Plymouth auth API"""
    if req.is_json:
        data = req.get_json()
        email, password = data.get("email"), data.get("password")
        if email and password:
            try:
                resp = requests.post(AUTH_URL, json={"email": email, "password": password}, timeout=5)
                if resp.status_code == 200:
                    return email
            except:
                pass
    return None

def get_trail_owner(Trail_Number):
    """Get owner email of a trail"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT TOP 1 u.Email
        FROM CW2.Trail t
        JOIN CW2.TrailOwnership trail_own ON t.Trail_Number = trail_own.Trail_Number
        JOIN CW2.[User] u ON trail_own.User_Number = u.User_Number
        WHERE t.Trail_Number = ?
        """, (Trail_Number,))
        owner = cursor.fetchone()
        conn.close()
        return owner[0] if owner else None
    except:
        return None

def get_trails():
    """GET /trails"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CW2.Trail")
        columns = [c[0] for c in cursor.description]
        results = []
        for row in cursor.fetchall():
            item = {k: convert_sql_types(v) for k, v in dict(zip(columns, row)).items()}
            if item.get("Trail_Name"):
                results.append(item)
        conn.close()
        return results, 200
    except Exception as e:
        return {"error": str(e)}, 500

def create_trail():
    """POST /trails"""
    data = request.get_json()
    user_email = get_user_email(request)
    if not user_email:
        return {"error": "Authentication failed"}, 401

    trail_number = data.get("Trail_Number")
    if not trail_number:
        return {"error": "Trail_Number is required"}, 400

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
        EXEC CW2.sp_CreateTrail ?, ?, ?, ?, ?, ?, ?, ?, ?
        """, (
            trail_number,
            data["Trail_Name"],
            data["Distance_km"],
            data["Duration_hr"],
            data.get("Difficulty"),
            data.get("Elevation_gain_m"),
            data.get("Route_Type"),
            data["Location_Number"],
            user_email
        ))
        conn.commit()
        conn.close()
        return {"message": f"Trail {trail_number} created by {user_email}"}, 201
    except Exception as e:
        return {"error": str(e)}, 500

def get_trail(Trail_Number):
    """GET /trails/{Trail_Number}"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CW2.Trail WHERE Trail_Number = ?", (Trail_Number,))
        row = cursor.fetchone()
        if row:
            columns = [c[0] for c in cursor.description]
            conn.close()
            return {k: convert_sql_types(v) for k, v in dict(zip(columns, row)).items()}, 200
        conn.close()
        return {"error": "Trail not found"}, 404
    except Exception as e:
        return {"error": str(e)}, 500

def update_trail(Trail_Number):
    """PUT /trails/{Trail_Number}"""
    data = request.get_json()
    user_email = get_user_email(request)
    if not user_email:
        return {"error": "Authentication failed"}, 401

    owner_email = get_trail_owner(Trail_Number)
    if not owner_email:
        return {"error": "Trail not found"}, 404

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
        EXEC CW2.sp_UpdateTrail ?, ?, ?, ?, ?, ?, ?, ?, ?
        """, (
            Trail_Number,
            data["Trail_Name"],
            data["Distance_km"],
            data["Duration_hr"],
            data.get("Difficulty"),
            data.get("Elevation_gain_m"),
            data.get("Route_Type"),
            data["Location_Number"],
            user_email
        ))
        conn.commit()
        conn.close()
        return {"message": f"Trail {Trail_Number} updated by {user_email}"}, 200
    except Exception as e:
        return {"error": str(e)}, 500

def delete_trail(Trail_Number):
    """DELETE /trails/{Trail_Number}"""
    user_email = get_user_email(request)

    # Try Swagger UI params
    if not user_email and not request.is_json:
        email = request.args.get('email')
        password = request.args.get('password')
        if email and password:
            try:
                resp = requests.post(AUTH_URL, json={"email": email, "password": password}, timeout=5)
                if resp.status_code == 200:
                    user_email = email
            except:
                pass

    if not user_email:
        return {"error": "Authentication failed"}, 401

    owner_email = get_trail_owner(Trail_Number)
    if not owner_email:
        return {"error": "Trail not found"}, 404

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("EXEC CW2.sp_DeleteTrail ?, ?", (Trail_Number, user_email))
        conn.commit()
        conn.close()
        return {"message": f"Trail {Trail_Number} deleted by {user_email}"}, 200
    except Exception as e:
        return {"error": str(e)}, 500