from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from app.employees.router import router_employees
from app.activities.router import router_activities

# Импорты моделей для правильной настройки SQLAlchemy relationship
from app.employees.models import Employee
from app.activities.models import Activity

path_to_json = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'employees.json')

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "MM"}

app.include_router(router_employees)
app.include_router(router_activities)