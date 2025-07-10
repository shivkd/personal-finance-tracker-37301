import os
import time
import httpx

"""
Script: test_backend_api_connectivity.py

Verifies:
- backend_api is running and serving requests
- can connect to PostgreSQL (by registering/logging in user and executing a transaction list call)
- basic endpoint health
Prints status and error diagnostics.

Usage: python test_backend_api_connectivity.py
"""

API_URL = os.environ.get("API_URL", "http://localhost:8000")

TEST_USER_EMAIL = "testuser1@example.com"
TEST_USER_PASSWORD = "strongpassword"

def wait_for_api_start(timeout=15):
    """Wait for FastAPI docs endpoint to be up"""
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = httpx.get(f"{API_URL}/docs")
            if r.status_code in (200, 401):
                print("✅ backend_api server is running.")
                return True
        except httpx.RequestError:
            pass
        print("Waiting for backend_api to start...")
        time.sleep(1)
    print("ERROR: backend_api server did not start in time.")
    return False

def register_user(email, password):
    r = httpx.post(f"{API_URL}/auth/register", json={
        "email": email,
        "password": password,
    })
    if r.status_code == 200 and "id" in r.json():
        print("✅ Registration endpoint works, user registered.")
        return r.json()
    elif r.status_code == 400 and "already registered" in r.text:
        print("ℹ️  User already registered, proceed.")
        return None
    else:
        print("❌ Registration error:", r.status_code, r.text)
        return None

def login_user(email, password):
    r = httpx.post(f"{API_URL}/auth/login", json={
        "email": email,
        "password": password,
    })
    if r.status_code == 200 and "access_token" in r.json():
        print("✅ Login endpoint works.")
        return r.json()["access_token"]
    else:
        print("❌ Login error:", r.status_code, r.text)
        return None

def test_transactions(token):
    headers = {"Authorization": f"Bearer {token}"}
    r = httpx.get(f"{API_URL}/transactions/", headers=headers)
    if r.status_code == 200:
        print("✅ Transactions endpoint returned:", r.json())
    else:
        print("❌ Transactions endpoint error:", r.status_code, r.text)

def main():
    print("\n--- BACKEND API & DB INTEGRATION CHECK ---")
    if not wait_for_api_start():
        return

    reg = register_user(TEST_USER_EMAIL, TEST_USER_PASSWORD)
    token = login_user(TEST_USER_EMAIL, TEST_USER_PASSWORD)
    if token:
        test_transactions(token)
    else:
        print("Failed to login, so skipping transaction test!")
    print("\n--- CHECK COMPLETE ---")
    print("If any ❌ errors above indicate DB/connection/startup issues, check backend_api logs and .env DB config.\n")

if __name__ == "__main__":
    main()
