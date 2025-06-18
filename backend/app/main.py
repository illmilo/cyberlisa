import time
import json
import subprocess
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from typing import Optional
from backend.utils import json_to_dict_list

from backend.models import EmployeeModel


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

@app.get("/employees")
def get_all_employees(role: Optional[str] = None) -> list[EmployeeModel]:
    employees = json_to_dict_list(path_to_json)
    filtered_employees = []
    if role is None:
        for employee in employees:
            filtered_employees.append(employee)
        return filtered_employees
    else:
        for employee in employees:
            if employee["role"] == role:
                filtered_employees.append(employee)
        return filtered_employees
    
@app.get("/employee")
def get_employee_from_param_id(eid: str) -> EmployeeModel:
    employees = json_to_dict_list(path_to_json)
    for employee in employees:
        if employee["id"] == eid:
            return employee

# data = {
#         'id' : '1',
#         'role': 'dev',  
#         'timebegin': '11:27:20',
#         'timeend': '11:27:30' 
#         }

# class LinuxAgent:

#     def time_to_seconds(self, tstr):
#         t = time.strptime(tstr, "%H:%M:%S")
#         return t.tm_hour * 3600 + t.tm_min * 60 + t.tm_sec

#     def __init__(self, data):
#         self.id = data['id']
#         self.role = data['role']
#         print(self.id)

#     def startActivity(self):
#         self.workingCycle(True)

#     def stopActivity(self):
#         self.workingCycle(False)

#     async def update(self, data):
#         timebegin_sec = self.time_to_seconds(data['timebegin'])
#         timeend_sec = self.time_to_seconds(data['timeend'])
#         working = False

#         while True:
#             now = time.localtime()
#             now_sec = now.tm_hour * 3600 + now.tm_min * 60 + now.tm_sec

#             if timebegin_sec <= now_sec <= timeend_sec and not working:
#                 print(f"Employee {self.id} started working at {time.strftime('%H:%M:%S', now)}")
#                 self.startActivity()
#                 working = True
#             elif now_sec > timeend_sec and working:
#                 print(f"Employee {self.id} stopped working at {time.strftime('%H:%M:%S', now)}")
#                 self.stopActivity()
#                 working = False

#     def workingCycle(self, flag):
#         if flag:
#             subprocess.run(["firefox"])

# class __main__:
#     LinuxAgent(data).update(data);
