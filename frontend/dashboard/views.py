from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json

# FastAPI backend URL
FASTAPI_URL = "http://localhost:8000"

def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

@csrf_exempt
def users(request):
    """
    Unified view to handle all user operations based on request method
    """
    # Handle GET request (list users)
    if request.method == "GET":
        try:
            response = requests.get(f"{FASTAPI_URL}/agents/")
            response.raise_for_status()
            return JsonResponse(response.json(), safe=False)
        except requests.RequestException as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    # Handle POST request (create user)
    elif request.method == "POST":
        try:
            # Parse JSON from request body
            data = json.loads(request.body)
            response = requests.post(f"{FASTAPI_URL}/agents/", json=data)
            response.raise_for_status()
            return JsonResponse(response.json(), status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except requests.RequestException as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    # Handle DELETE request (delete user)
    elif request.method == "DELETE":
        try:
            # Get user ID from request body
            data = json.loads(request.body)
            user_id = data.get("id")
            if not user_id:
                return JsonResponse({"error": "User ID is required"}, status=400)
                
            response = requests.delete(f"{FASTAPI_URL}/agents/{user_id}/")
            response.raise_for_status()
            return JsonResponse(response.json())
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except requests.RequestException as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    # Handle other methods
    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def user_detail(request, user_id):
    """
    Unified view to handle user-specific operations based on request method
    """
    # Handle GET request (get user details)
    if request.method == "GET":
        try:
            response = requests.get(f"{FASTAPI_URL}/agents/{user_id}")
            response.raise_for_status()
            return JsonResponse(response.json())
        except requests.RequestException as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    # Handle PUT request (update user)
    elif request.method == "PUT":
        try:
            # Parse JSON from request body
            data = json.loads(request.body)
            response = requests.put(f"{FASTAPI_URL}/agents/{user_id}", json=data)
            response.raise_for_status()
            return JsonResponse(response.json())
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except requests.RequestException as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    # Handle DELETE request (delete user)
    elif request.method == "DELETE":
        try:
            response = requests.delete(f"{FASTAPI_URL}/agents/{user_id}/")
            response.raise_for_status()
            return JsonResponse(response.json())
        except requests.RequestException as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    # Handle other methods
    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def user_actions(request, user_id, action=None):
    """
    Unified view to handle user-specific actions
    """
    if request.method == "POST":
        try:
            # Start/stop agent actions
            if action in ["start_agent", "stop_agent"]:
                response = requests.post(f"{FASTAPI_URL}/agents/{user_id}/{action}")
                response.raise_for_status()
                return JsonResponse(response.json())
            
            # Add activity action
            elif action == "add_activity":
                # Get activity ID from request body
                data = json.loads(request.body)
                activity_id = data.get("activity_id")
                if not activity_id:
                    return JsonResponse({"error": "Activity ID is required"}, status=400)
                    
                response = requests.post(
                    f"{FASTAPI_URL}/agents/{user_id}/add_activity/{activity_id}"
                )
                response.raise_for_status()
                return JsonResponse(response.json())
            
            # Assign activities action
            elif action == "assign_activities":
                # Get activity IDs from request body
                data = json.loads(request.body)
                activity_ids = data.get("activity_ids")
                if not activity_ids or not isinstance(activity_ids, list):
                    return JsonResponse({"error": "Activity IDs array is required"}, status=400)
                    
                response = requests.post(
                    f"{FASTAPI_URL}/agents/{user_id}/assign_activities",
                    json={"activity_ids": activity_ids}
                )
                response.raise_for_status()
                return JsonResponse(response.json())
            
            return JsonResponse({"error": "Invalid action"}, status=400)
            
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except requests.RequestException as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    # Handle other methods
    return JsonResponse({"error": "Method not allowed"}, status=405)