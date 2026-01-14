import requests
import json

BASE_URL = "http://localhost:5000" # Oder die Render-URL nach dem Deployment

def run_test(test_name, endpoint, method, payload=None, expected_status=200, expected_contains=None):
    print(f"\n--- Running Test: {test_name} ---")
    
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}")
        elif method == "POST":
            response = requests.post(f"{BASE_URL}{endpoint}", json=payload, headers={"Content-Type": "application/json"})
        else:
            print(f"  Error: Unsupported method {method}")
            return False

        print(f"  Status Code: {response.status_code}")
        print(f"  Response: {response.text}")

        assert response.status_code == expected_status, f"Expected status {expected_status}, got {response.status_code}"
        
        if expected_contains:
            assert expected_contains in response.text, f"Expected '{expected_contains}' in response, but not found."
        
        print(f"  ✅ Test '{test_name}' PASSED!")
        return True

    except requests.exceptions.ConnectionError:
        print(f"  ❌ Test '{test_name}' FAILED: Could not connect to {BASE_URL}. Is the app running?")
        return False
    except AssertionError as e:
        print(f"  ❌ Test '{test_name}' FAILED: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Test '{test_name}' FAILED with unexpected error: {e}")
        return False

if __name__ == '__main__':
    print("Starting Automated Vital Monitor Tests...")
    
    # Test 1: Home Page
    run_test("Home Page Access", "/", "GET", expected_contains="Vitaldaten-Eingabe")

    # Test 2: Normal Heart Rate
    run_test("Normal Heart Rate", "/vital-check", "POST", {"patient_id": "P001", "heart_rate": 75}, expected_contains="Normal")

    # Test 3: Tachycardia Warning
    run_test("High Heart Rate", "/vital-check", "POST", {"patient_id": "P002", "heart_rate": 110}, expected_contains="Tachycardia Warning")

    # Test 4: Bradycardia Warning
    run_test("Low Heart Rate", "/vital-check", "POST", {"patient_id": "P003", "heart_rate": 55}, expected_contains="Bradycardia Warning")
    
    print("\nAutomated Tests Completed.")