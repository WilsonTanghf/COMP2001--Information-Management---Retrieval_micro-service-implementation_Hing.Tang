# TrailService API

**COMP2001HK Information Management and Retrieval - Assessment 2**  
Trail CRUD API for managing hiking trail data. Built with Flask + Connexion + SQL Server.

## What You Can Do

This API provides full CRUD operations for hiking trails:

- GET /trails - List all trails
- POST /trails - Create new trail  
- GET /trails/{Trail_Number} - Read specific trail
- PUT /trails/{Trail_Number} - Update trail
- DELETE /trails/{Trail_Number} - Delete trail

**Authentication required** for create/update/delete using `email`/`password` validated against Plymouth COMP2001 auth service.

## 1. Prerequisites

**Python**: 3.11.4

**Required packages** (exact versions):
1. Flask==2.2.2, 
2. connexion[swagger-ui]==2.14.1, 
3. pyodbc==5.3.0, 
4. requests==2.31.0, 
5. Database Driver: ODBC Driver 17 for SQL Server

## 2. Setup
Step 1: **Install Dependencies**
1. Install python
2. Install ODBC Driver
3. pip install Flask==2.2.2 
4. pip install connexion[swagger-ui]==2.14.1 pyodbc==5.3.0 requests==2.31.0,

Step 2: **Project Structure**
```
TrailService/
├── app.py          (Connexion app entry point)
├── openapi.yaml    (OpenAPI 3.0 specification)
└── trail_api.py    (API handler functions)
```

Step 3: **Run API**
1. cd TrailService (in this case)
2. python app.py

## 3. Access Points
Swagger UI (interactive docs): http://localhost:8000/ui

## 4. How to Use the API (Swagger UI Instructions)

4.1 **GET /trails - List all trails (No auth needed)**

1. Click "Try it out"
2. Click "Execute"
3. Response: 200 - Lists all trails

4.2 **POST /trails - Create new trail**

Example JSON:
```json
{
  "Trail_Number": "T0155",
  "Trail_Name": "Raven Crag",
  "Distance_km": 1.9,
  "Duration_hr": 1.5,
  "Difficulty": "Moderate",
  "Elevation_gain_m": 226,
  "Route_Type": "out & back",
  "Location_Number": "L001",
  "email": "grace@plymouth.ac.uk",
  "password": "ISAD123!"
}
```

1. Click "Try it out"
2. Click "Execute"
3. Response: 201 - "Trail T0155 created by grace@plymouth.ac.uk"

4.3 **GET /trails/{Trail_Number} - Get single trail**

1. Click "Try it out"
2. Enter Trail_Number: T0001 or T0049 or T0076
3. Click "Execute"
4. Response: 200 - Single trail details

4.4 **PUT /trails/{Trail_Number} - Update trail**

Example JSON (Valid owner):
```json
{
  "Trail_Number": "T0155",
  "Trail_Name": "Buttermere Circular",
  "Distance_km": 7.4,
  "Duration_hr": 2.5,
  "Difficulty": "Easy",
  "Elevation_gain_m": 117,
  "Route_Type": "Loop",
  "Location_Number": "L002",
  "email": "grace@plymouth.ac.uk",
  "password": "ISAD123!"
}
```

1. Click "Try it out"
2. Enter Trail_Number: T0155"
3. Execute → 200: "Trail updated"

**Test Access Denied (Wrong credentials):**
```json
{
  "email": "timgplysouth.ac.uk",
  "password": "COMP2001!"
}
```

Result: 500 - "Access denied"

4.5 **DELETE /trails/{Trail_Number}**
1. Click "Try it out"
2. Trail_Number: T0155
3. Email: grace@plymouth.ac.uk
4. password: ISAD123!
5. Execute → 200: "Trail deleted"


