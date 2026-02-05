import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_hash_route():
    print("--- Starting HashRoute Verification ---")
    
    # 1. Health check
    try:
        resp = requests.get(f"{BASE_URL}/")
        print(f"Health Check: {resp.status_code} - {resp.json()}")
    except requests.exceptions.ConnectionError:
        print("ERROR: Server is not running. Please run 'uvicorn app.main:app' in another terminal.")
        return

    # 2. Shorten a URL
    long_url = "https://www.google.com/search?q=fastapi+layered+architecture"
    payload = {"original_url": long_url}
    resp = requests.post(f"{BASE_URL}/shorten", json=payload)
    print(f"Shorten URL: {resp.status_code}")
    if resp.status_code == 201:
        data = resp.json()
        short_code = data["short_code"]
        short_url = data["short_url"]
        print(f"  Short Code: {short_code}")
        print(f"  Short URL: {short_url}")
        
        # 3. Test Redirection
        # Note: requests follow redirects by default, we can check history
        print(f"Testing Redirection for {short_code}...")
        redirect_resp = requests.get(f"{BASE_URL}/{short_code}", allow_redirects=False)
        print(f"  Redirect Status: {redirect_resp.status_code}")
        print(f"  Location: {redirect_resp.headers.get('Location')}")
        
        if redirect_resp.status_code == 307 or redirect_resp.status_code == 302:
             print("  ✅ Redirection Success")
        
        # 4. Test Idempotency (same URL should give same code)
        resp_again = requests.post(f"{BASE_URL}/shorten", json=payload)
        if resp_again.json()["short_code"] == short_code:
            print("  ✅ Idempotency Success")

    # 5. Test 404
    resp_404 = requests.get(f"{BASE_URL}/nonexistent")
    print(f"Test 404: {resp_404.status_code} - {resp_404.json()['detail']}")

if __name__ == "__main__":
    test_hash_route()
