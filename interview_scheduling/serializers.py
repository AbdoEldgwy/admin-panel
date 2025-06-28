
import requests
def fetch_interview_data(session_slug):
    url = f"http://localhost:8000/admin_dashboard/interview_scheduling/api/interview/{session_slug}/"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an error for non-200 responses
        data = response.json()
        return data
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching interview data: {e}")
        return None
data = fetch_interview_data("duwcrhmfmw") 
print(data) 